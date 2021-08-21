create table last_scratch (
   id       SERIAL PRIMARY KEY,
   last_get VARCHAR(20) NOT NULL,
   active   VARCHAR(10) NOT NULL
);

ALTER SYSTEM SET wal_level TO 'logical';
ALTER TABLE public.last_scratch REPLICA IDENTITY FULL;