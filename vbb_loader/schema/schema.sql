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

CREATE TABLE vbb_calendar_dates
(
    service_id INTEGER NOT NULL,
    "date" TIMESTAMP,
    exception_type INTEGER
);
