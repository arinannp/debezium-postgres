create table covid_api (
   id                 BIGINT NOT NULL PRIMARY KEY,
   date               VARCHAR NOT NULL,
   death              INTEGER,
   recover            INTEGER,
   positive           INTEGER,
   recovery           INTEGER,
   death_cumulatif    INTEGER,
   recover_cumulatif  INTEGER,
   positive_cumulatif INTEGER,
   recovery_cumulatif INTEGER,
   scraping_id        INTEGER
);

ALTER SYSTEM SET wal_level TO 'logical';
ALTER TABLE public.covid_api REPLICA IDENTITY FULL;