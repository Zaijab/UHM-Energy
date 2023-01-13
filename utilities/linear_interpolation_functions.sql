CREATE OR REPLACE FUNCTION aurora_api.linear_interpolate(x_i DOUBLE PRECISION, 
    x_0 DOUBLE PRECISION, 
    y_0 DOUBLE PRECISION, 
    x_1 DOUBLE PRECISION, 
    y_1 DOUBLE PRECISION)
RETURNS DOUBLE PRECISION AS $$
    SELECT (($5 - $3) / ($4 - $2)) * ($1 - $2) + $3;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION aurora_api.timestamp_to_seconds(timestamp_t TIMESTAMP)
RETURNS DOUBLE PRECISION AS $$
    SELECT EXTRACT(epoch from timestamp_t)
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION aurora_api.linear_interpolate(x_i TIMESTAMP, x_0 TIMESTAMP, y_0 DOUBLE PRECISION, x_1 TIMESTAMP, y_1 DOUBLE PRECISION)
RETURNS DOUBLE PRECISION AS $$
    SELECT aurora_api.linear_interpolate(aurora_api.timestamp_to_seconds($1), 
        aurora_api.timestamp_to_seconds($2), 
        $3, 
        aurora_api.timestamp_to_seconds($4),
        $5);
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION last_known_t(prev float8, current float8)
  returns float8
  as $$return current or prev$$
  language plpython3u;

create OR REPLACE aggregate last_known(float8) (
  stype =float8,
  sfunc = last_known_t,
  combinefunc = last_known_t
);

CREATE OR REPLACE FUNCTION last_known_t(prev timestamp, current timestamp)
  returns timestamp
  as $$return current or prev$$
  language plpython3u;

CREATE OR REPLACE AGGREGATE last_known(timestamp) (
  stype = timestamp,
  sfunc = last_known_t,
  combinefunc = last_known_t
);
