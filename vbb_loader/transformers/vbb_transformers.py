from typing import Sequence, List, Tuple

from vbb_loader.schema.init import SCHEMA_PREFIX


class VbbTransformer:
    def column_names(self, fields: Sequence[str]) -> List[str]:
        return [f for f in fields]

    def column_values(self, row: dict) -> Tuple:
        return tuple(row.values())

    def typed_value(self, column_name, value):
        if column_name in self.int_columns():
            return int(value)
        if column_name in self.bool_columns():
            return bool(value)
        return value

    def bool_columns(self):
        return []

    def int_columns(self):
        return []


class StopTransformer(VbbTransformer):

    @staticmethod
    def supports_table(name):
        return name == f"{SCHEMA_PREFIX}_stops"

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
    @staticmethod
    def supports_table(name):
        return name == f"{SCHEMA_PREFIX}_agency"

    def int_columns(self):
        return ['agency_id']


TRANSFORMERS = {
    f'{SCHEMA_PREFIX}_agency': AgencyTransformer,
    f'{SCHEMA_PREFIX}_stops': StopTransformer
}


def get_transformer(table) -> VbbTransformer:
    if table in TRANSFORMERS.keys():
        return TRANSFORMERS[table]()
    return VbbTransformer()
