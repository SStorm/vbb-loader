DROP TABLE IF EXISTS vbb_stops;

CREATE TABLE vbb_stops
(
    stop_id VARCHAR (32) NOT NULL,
    stop_code VARCHAR (128),
    stop_name VARCHAR (128),
    stop_desc TEXT,
    location geo_point,
    location_type INTEGER,
    parent_station VARCHAR (128),
    wheelchair_boarding BOOLEAN,
    platform_code VARCHAR (128),
    zone_id VARCHAR (128)
);

DROP TABLE IF EXISTS vbb_agency;

CREATE TABLE vbb_agency
(
    agency_id INTEGER NOT NULL,
    agency_name VARCHAR (64),
    agency_url VARCHAR (128),
    agency_timezone VARCHAR (32),
    agency_lang VARCHAR(2),
    agency_phone VARCHAR(32)
);

DROP TABLE IF EXISTS vbb_calendar_dates;

CREATE TABLE vbb_calendar_dates
(
    service_id INTEGER NOT NULL,
    "date" TIMESTAMP,
    exception_type INTEGER
);

DROP TABLE IF EXISTS vbb_calendar;

CREATE TABLE vbb_calendar
(
    service_id INTEGER NOT NULL,
    monday BOOLEAN,
    tuesday BOOLEAN,
    wednesday BOOLEAN,
    thursday BOOLEAN,
    friday BOOLEAN,
    saturday BOOLEAN,
    sunday BOOLEAN,
    "start_date" TIMESTAMP,
    "end_date" TIMESTAMP
);

DROP TABLE IF EXISTS vbb_routes;

CREATE TABLE vbb_routes
(
    route_id VARCHAR (32) NOT NULL,
    agency_id INTEGER,
    route_short_name VARCHAR (32),
    route_long_name VARCHAR (64),
    route_type INTEGER,
    route_color VARCHAR (32),
    route_text_color VARCHAR (32),
    route_desc VARCHAR (128)
);

DROP TABLE IF EXISTS vbb_stop_times;

CREATE TABLE vbb_stop_times
(
    trip_id INTEGER NOT NULL,
    arrival_time VARCHAR (16),
    departure_time VARCHAR (16),
    stop_id VARCHAR (32),
    stop_sequence INTEGER,
    pickup_type INTEGER,
    drop_off_type INTEGER,
    stop_headsign VARCHAR (64)
);

DROP TABLE IF EXISTS vbb_transfers;

CREATE TABLE vbb_transfers
(
    from_stop_id VARCHAR (32),
    to_stop_id VARCHAR (32),
    transfer_type INTEGER,
    min_transfer_time INTEGER,
    from_route_id VARCHAR (32),
    to_route_id VARCHAR (32),
    from_trip_id INTEGER,
    to_trip_id INTEGER
);

DROP TABLE IF EXISTS vbb_trips;

CREATE TABLE vbb_trips
(
    route_id VARCHAR (32),
    service_id INTEGER,
    trip_id INTEGER,
    trip_headsign VARCHAR (64),
    trip_short_name VARCHAR (64),
    direction_id INTEGER,
    block_id INTEGER,
    shape_id INTEGER,
    wheelchair_accessible BOOLEAN,
    bikes_allowed BOOLEAN
);

DROP TABLE IF EXISTS vbb_shapes;

CREATE TABLE vbb_shapes
(
    shape_id INTEGER NOT NULL,
    shape geo_shape
);
