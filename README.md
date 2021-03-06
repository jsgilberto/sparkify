# Sparkify

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Datasets

### Song Dataset

The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```json
{
  "num_songs": 1,
  "artist_id": "ARJIE2Y1187B994AB7",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "",
  "artist_name": "Line Renaud",
  "song_id": "SOUPIRU12A6D4FA1E1",
  "title": "Der Kleine Dompfaff",
  "duration": 152.92036,
  "year": 0
}
```

### Log Dataset

The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```

And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

```json
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
{"artist":null,"auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":0,"lastName":"Summers","length":null,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"GET","page":"Home","registration":1540344794796.0,"sessionId":139,"song":null,"status":200,"ts":1541106106796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}
```

## Sparkify analytical goals

The team is particularly interested in what songs the users listen.

They want to answer questions like the following:
- What songs are users listening to?
- What is the behaviour of the user depending on the time of the year/week/day?
- What songs do paid vs free users listens to?

## Schema for Song Play Analysis

I created a star schema optimized for queries on song play analysis. This includes
the following tables:

### Fact table

1. songplays - records in log data associated with song plays i.e. records with page `NextSong`

### Dimension tables

2. users - users in the app
3. songs - songs in music database
4. artists - artists in music database
5. time - timestamps of records in songplays broken down into specific units

### ER Diagram

The following Entity Relationship Diagram explains part of the implementation details of
the schema explained before:

![ER Diagram](https://github.com/jsgilberto/sparkify/blob/main/sparkifydb_erd.png)

## ETL Pipeline

Inside `src/etl.py` is the ETL pipeline used in this project.

### Extract:

Basically, in this step, we extract all the data of song and log json files
one at a time.

### Transform:

Next, we create pandas DataFrames to temporarily store the data in memory and apply
transformations and temporal columns to get ready to the next step.

### Load:

Finally, we load the data to a Postgres database called sparkifydb. This database
holds all the data using the star schema previously mentioned.