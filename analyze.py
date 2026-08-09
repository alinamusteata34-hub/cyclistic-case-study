import duckdb

con = duckdb.connect("cyclistic.duckdb")

print("=" * 60)
print("1. AVERAGE RIDE LENGTH: MEMBER vs CASUAL")
print("=" * 60)
avg_length = con.execute("""
    SELECT
        member_casual,
        ROUND(AVG(ride_length_min), 2) AS avg_ride_length_min,
        ROUND(MEDIAN(ride_length_min), 2) AS median_ride_length_min,
        COUNT(*) AS total_rides
    FROM cleaned_trips
    GROUP BY member_casual
    ORDER BY member_casual
""").fetchdf()
print(avg_length)

print("\n" + "=" * 60)
print("2. RIDES BY DAY OF WEEK: MEMBER vs CASUAL")
print("=" * 60)
by_day = con.execute("""
    SELECT
        member_casual,
        day_of_week,
        COUNT(*) AS ride_count,
        ROUND(AVG(ride_length_min), 2) AS avg_ride_length_min
    FROM cleaned_trips
    GROUP BY member_casual, day_of_week
    ORDER BY member_casual,
        CASE day_of_week
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
            WHEN 'Sunday' THEN 7
        END
""").fetchdf()
print(by_day.to_string(index=False))

print("\n" + "=" * 60)
print("3. RIDES BY MONTH: MEMBER vs CASUAL (seasonality)")
print("=" * 60)
by_month = con.execute("""
    SELECT
        member_casual,
        month,
        COUNT(*) AS ride_count
    FROM cleaned_trips
    GROUP BY member_casual, month
    ORDER BY member_casual,
        CASE month
            WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
            WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
            WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
            WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12
        END
""").fetchdf()
print(by_month.to_string(index=False))

print("\n" + "=" * 60)
print("4. TOP 10 START STATIONS: MEMBERS")
print("=" * 60)
top_stations_member = con.execute("""
    SELECT start_station_name, COUNT(*) AS ride_count
    FROM cleaned_trips
    WHERE member_casual = 'member' AND start_station_name IS NOT NULL
    GROUP BY start_station_name
    ORDER BY ride_count DESC
    LIMIT 10
""").fetchdf()
print(top_stations_member.to_string(index=False))

print("=" * 60)
print("5. TOP 10 START STATIONS: CASUAL RIDERS")
print("=" * 60)
top_stations_casual = con.execute("""
    SELECT start_station_name, COUNT(*) AS ride_count
    FROM cleaned_trips
    WHERE member_casual = 'casual' AND start_station_name IS NOT NULL
    GROUP BY start_station_name
    ORDER BY ride_count DESC
    LIMIT 10
""").fetchdf()
print(top_stations_casual.to_string(index=False))

print("=" * 60)
print("6. BIKE TYPE PREFERENCE: MEMBER vs CASUAL")
print("=" * 60)
bike_type = con.execute("""
    SELECT
        member_casual,
        rideable_type,
        COUNT(*) AS ride_count
    FROM cleaned_trips
    GROUP BY member_casual, rideable_type
    ORDER BY member_casual, ride_count DESC
""").fetchdf()
print(bike_type.to_string(index=False))

# --- Export summary tables to CSV for later visualization ---
avg_length.to_csv("summary_avg_length.csv", index=False)
by_day.to_csv("summary_by_day.csv", index=False)
by_month.to_csv("summary_by_month.csv", index=False)
top_stations_member.to_csv("summary_top_stations_member.csv", index=False)
top_stations_casual.to_csv("summary_top_stations_casual.csv", index=False)
bike_type.to_csv("summary_bike_type.csv", index=False)

con.close()
print("\n\nAll summary tables exported as CSVs for visualization.")
