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
