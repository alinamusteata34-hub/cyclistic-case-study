import duckdb

# Connect to a local DuckDB database file (creates it if it doesn't exist)
con = duckdb.connect("cyclistic.duckdb")

# Load and combine all 12 CSVs into one raw table
con.execute("""
    CREATE OR REPLACE TABLE raw_trips AS
    SELECT * FROM read_csv_auto('data/*.csv', union_by_name=True)
""")

row_count = con.execute("SELECT COUNT(*) FROM raw_trips").fetchone()[0]
print(f"Loaded {row_count:,} total rows from 12 months of data")

# --- Data quality checks ---

# Check for duplicate ride_ids
dupes = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT ride_id, COUNT(*) as cnt
        FROM raw_trips
        GROUP BY ride_id
        HAVING cnt > 1
    )
""").fetchone()[0]
print(f"Duplicate ride_ids: {dupes:,}")

# Check for nulls in key columns
nulls = con.execute("""
    SELECT
        SUM(CASE WHEN ride_id IS NULL THEN 1 ELSE 0 END) AS null_ride_id,
        SUM(CASE WHEN started_at IS NULL THEN 1 ELSE 0 END) AS null_started_at,
        SUM(CASE WHEN ended_at IS NULL THEN 1 ELSE 0 END) AS null_ended_at,
        SUM(CASE WHEN member_casual IS NULL THEN 1 ELSE 0 END) AS null_member_casual
    FROM raw_trips
""").fetchdf()
print("\nNull counts in key columns:")
print(nulls)

# Check for negative or zero-length rides
bad_durations = con.execute("""
    SELECT COUNT(*) FROM raw_trips
    WHERE ended_at <= started_at
""").fetchone()[0]
print(f"\nRides with zero/negative duration: {bad_durations:,}")

# --- Build cleaned table ---
con.execute("""
   CREATE OR REPLACE TABLE cleaned_trips AS
    SELECT DISTINCT ON (ride_id)
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        DATEDIFF('minute', started_at, ended_at) AS ride_length_min,
        DAYNAME(started_at) AS day_of_week,
        MONTHNAME(started_at) AS month,
        start_station_name,
        end_station_name,
        member_casual
    FROM raw_trips
    WHERE ride_id IS NOT NULL
      AND ended_at > started_at
    ORDER BY ride_id, started_at
""")

cleaned_count = con.execute("SELECT COUNT(*) FROM cleaned_trips").fetchone()[0]
print(f"\nCleaned dataset row count: {cleaned_count:,}")

con.close()
print("\nDone. Data saved in cyclistic.duckdb (tables: raw_trips, cleaned_trips)")
