import datetime

from typing import Sequence, List, Tuple

from vbb_loader.schema.init import SCHEMA_PREFIX


class TableNotSupportedException(Exception):
    pass


class VbbTransformer:
    def column_names(self, fields: Sequence[str]) -> List[str]:
        return [f for f in fields]

    def column_values(self, row: dict) -> Tuple:
        return tuple([self.typed_value(v[0], v[1]) for v in row.items()])

    def typed_value(self, column_name, value):
        if len(value) == 0:
            return None

        if column_name in self.int_columns():
            return int(value)
        if column_name in self.bool_columns():
            return bool(value)
        if column_name in self.date_columns():
            return datetime.datetime.strptime(value, '%Y%m%d')
        return value

    def bool_columns(self):
        return []

    def int_columns(self):
        return []

    def date_columns(self):
        return []

    def eof(self):
        pass


class StopTransformer(VbbTransformer):
    def column_names(self, fields: Sequence[str]) -> List[str]:
        ret = []
        ignore = ['stop_lat', 'stop_lon']
        for f in fields:
            if f in ignore:
                continue
            ret.append(f)
        ret.append('location')
        return ret

    def column_values(self, row: dict) -> Tuple:
        cols = self.column_names(row.keys())
        ret = []
        for col in cols:
            if col in row:
                ret.append(self.typed_value(col, row[col]))
        # Now transform and append the location
        ret.append([float(row['stop_lat']), float(row['stop_lon'])])
        return tuple(ret)

    def bool_columns(self):
        return ['wheelchair_boarding']

    def int_columns(self):
        return ['location_type']


class AgencyTransformer(VbbTransformer):
    def int_columns(self):
        return ['agency_id']


class CalendarDatesTransformer(VbbTransformer):
    def int_columns(self):
        return ['service_id', 'exception_type']

    def date_columns(self):
        return ['date']


class CalendarTransformer(VbbTransformer):
    def int_columns(self):
        return ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def bool_columns(self):
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def date_columns(self):
        return ['start_date', 'end_date']


class RoutesTransformer(VbbTransformer):
    def int_columns(self):
        return ['agency_id', 'route_type']


class StopTimesTransformer(VbbTransformer):
    def int_columns(self):
        return ['trip_id', 'stop_sequence', 'pickup_type', 'drop_off_type']


class TransfersTransformer(VbbTransformer):
    def int_columns(self):
        return ['transfer_type', 'min_transfer_time', 'from_trip_id', 'to_trip_id']


class TripsTransformer(VbbTransformer):
    def int_columns(self):
        return ['service_id', 'trip_id', 'direction_id', 'block_id', 'shape_id']

    def bool_columns(self):
        return ['wheelchair_accessible', 'bikes_allowed']


class ShapesTransformer(VbbTransformer):
    def __init__(self):
        self.shape_id = None
        self.points = []
        self.to_return = None

    def column_names(self, fields: Sequence[str]) -> List[str]:
        return ['shape_id', 'shape']

    def column_values(self, row: dict) -> Tuple:
        self.to_return = None

        if self.shape_id is None:
            self.shape_id = row['shape_id']

        if self.shape_id != row['shape_id']:
            # new shape!
            if len(set(self.points)) == 1:
                # all the points are the same, invalid geometry - will ignore
                self.shape_id = row['shape_id']
                self.points.clear()
            else:
                linestring = ','.join(self.points)
                self.to_return = (
                    int(self.shape_id),
                    f'LINESTRING ({linestring})'
                )
                self.shape_id = row['shape_id']
                self.points.clear()
        self.points.append("{p1} {p2}".format(p1=row['shape_pt_lon'], p2=row['shape_pt_lat']))
        return self.to_return

    def eof(self):
        if len(set(self.points)) == 1:
            return None
        linestring = ','.join(self.points)
        return (
            int(self.shape_id),
            f'LINESTRING ({linestring})'
        )


TRANSFORMERS = {
    f'{SCHEMA_PREFIX}_agency': AgencyTransformer,
    f'{SCHEMA_PREFIX}_stops': StopTransformer,
    f'{SCHEMA_PREFIX}_calendar_dates': CalendarDatesTransformer,
    f'{SCHEMA_PREFIX}_calendar': CalendarTransformer,
    f'{SCHEMA_PREFIX}_routes': RoutesTransformer,
    f'{SCHEMA_PREFIX}_stop_times': StopTimesTransformer,
    f'{SCHEMA_PREFIX}_transfers': TransfersTransformer,
    f'{SCHEMA_PREFIX}_trips': TripsTransformer,
    f'{SCHEMA_PREFIX}_shapes': ShapesTransformer
}


def get_transformer(table) -> VbbTransformer:
    if table in TRANSFORMERS.keys():
        return TRANSFORMERS[table]()
    raise TableNotSupportedException(f'No transformer for table {table}')
