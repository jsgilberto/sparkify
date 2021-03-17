""" src/etl.py
    This module extracts data from json files, transforms the data into pandas DataFrames
    and loads the data into the sparkifydb database.
"""
import os
import glob
from typing import Text, Any, Callable
import pandas as pd
from sql_queries import *
from create_tables import connect_to_database
import constants


def process_song_file(cursor: Any, filepath: Text) -> None:
    """ Process a single song file and store its data in the database.

    Args:
        cursor (Any): Cursor object returned by the Connection.cursor method
        filepath (Text): path to json file
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = df.song_id, df.title, df.artist_id, df.year, df.duration
    cursor.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.artist_id, df.artist_name, df.artist_location, df.artist_latitude, \
        df.artist_longitude
    cursor.execute(artist_table_insert, artist_data)


def process_log_file(cursor: Any, filepath: Text) -> None:
    """ Process a single log file and store its data in the database.

    Args:
        cursor (Any): Cursor object returned by the Connection.cursor method
        filepath (Text): path to json file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")
    
    # insert time data records
    time_data = [
        t.values.astype(str),
        t.dt.hour.values.astype(str),
        t.dt.day.values.astype(str),
        t.dt.isocalendar().week.values.astype(str),
        t.dt.month.values.astype(str),
        t.dt.year.values.astype(str),
        t.dt.weekday.values.astype(str)
    ]
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame(time_data).transpose()
    time_df.columns = column_labels

    for i, row in time_df.iterrows():
        cursor.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cursor.execute(user_table_insert, row)

    

    df.reset_index(drop=True, inplace=True)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cursor.execute(song_select, (row.song, row.artist, row.length))
        results = cursor.fetchone()
        
        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        # insert songplay record
        songplay_data = (
            time_df.at[index, "start_time"],
            row.userId,
            song_id,
            artist_id,
            row.sessionId,
            row.level,
            row.location,
            row.userAgent
        )
        # print(songplay_data)
        cursor.execute(songplay_table_insert, songplay_data)


def process_data(cursor: Any, connection: Any, filepath: Text, func: Callable[[Any, Text], None]):
    """ Finds all *.json files inside the specified filepath. It then applies a
    function to each file.

    Args:
        cursor (Any): Cursor object returned by the Connection.cursor method
        connection (Any): Connection object returned by the psycopg2.connect method
        filepath (Text): path to json files
        func (Callable[[Any, Text], None]): function used to process all the data.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cursor, datafile)
        connection.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ Main function:
    - connects to sparkifydb database
    - creates a cursor
    - processes each song/log file of data
    """
    _, connection = connect_to_database(
        'sparkifydb', 
        constants.POSTGRES_USER, 
        constants.POSTGRES_PASSWORD
    )
    cursor = connection.cursor()

    process_data(cursor, connection, filepath='data/song_data', func=process_song_file)
    process_data(cursor, connection, filepath='data/log_data', func=process_log_file)

    connection.close()


if __name__ == "__main__":
    main()