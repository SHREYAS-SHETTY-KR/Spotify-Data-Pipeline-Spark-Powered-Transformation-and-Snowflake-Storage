import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
from pyspark.sql.functions import explode, col, to_date
from datetime import datetime
from awsglue.dynamicframe import DynamicFrame
s3_path = 's3://spotify-project-spark/raw_data/to_processed/'
source_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_path]},
    format="json",
)
spotify_df = source_df.toDF()


def process_albums(df):
    df = df.withColumn("items", explode("items")).select(
        col("items.track.album.id").alias("album_id"),
        col("items.track.album.name").alias("album_name"),
        col("items.track.album.release_date").alias("release_date"),
        col("items.track.album.total_tracks").alias("total_tracks"),
        col("items.track.album.external_urls.spotify").alias("url")
    ).drop_duplicates(["album_id"])
    return df


def process_artists(df):
    # First, explode the items to get individual tracks
    df_items_exploded = df.select(explode(col("items")).alias("item"))
    
    # Then, explode the artists array within each item to create a row for each artist
    df_artists_exploded = df_items_exploded.select(explode(col("item.track.artists")).alias("artist"))
    
    # Now, select the artist attributes, ensuring each artist is in its own row
    df_artists = df_artists_exploded.select(
        col("artist.id").alias("artist_id"),
        col("artist.name").alias("artist_name"),
        col("artist.external_urls.spotify").alias("external_url")
    ).drop_duplicates(["artist_id"])
    
    return df_artists


def process_songs(df):
    # Explode the items array to create a row for each song
    df_exploded = df.select(explode(col("items")).alias("item"))
    
    # Extract song information from the exploded DataFrame
    df_songs = df_exploded.select(
        col("item.track.id").alias("song_id"),
        col("item.track.name").alias("song_name"),
        col("item.track.duration_ms").alias("duration_ms"),
        col("item.track.external_urls.spotify").alias("url"),
        col("item.track.popularity").alias("popularity"),
        col("item.added_at").alias("song_added"),
        col("item.track.album.id").alias("album_id"),
        col("item.track.artists")[0]["id"].alias("artist_id")
    ).drop_duplicates(["song_id"])
    
    # Convert string dates in 'song_added' to actual date types
    df_songs = df_songs.withColumn("song_added", to_date(col("song_added")))
    
    return df_songs
album_df = process_albums(spotify_df)
album_df.show(5)
artist_df = process_artists(spotify_df)
artist_df.show(5)
song_df = process_songs(spotify_df)
song_df.show(5)
def write_to_s3(df, path_suffix, format_type="csv"):
    # Convert back to DynamicFrame
    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")
    
    glueContext.write_dynamic_frame.from_options(
        frame = dynamic_frame,
        connection_type = "s3",
        connection_options = {"path": f"s3://spotify-project-spark/transformed_data/{path_suffix}/"},
        format = format_type
    )
write_to_s3(album_df, "album/album_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")
write_to_s3(artist_df, "artist/artist_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")
write_to_s3(song_df, "songs/songs_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")

def list_s3_objects(bucket, prefix):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket = bucket, Prefix = prefix)
    keys = [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.json')]
    return keys
    
bucket_name = 'spotify-project-spark'
prefix = 'raw_data/to_processed/'
spotify_keys = list_s3_objects(bucket_name, prefix)

def move_and_delete_files(spotify_keys, Bucket):
    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source = {
            'Bucket' : Bucket,
            'Key' : key
        }
        
        destination_key = 'raw_data/processed/' + key.split('/')[-1]
        s3_resource.meta.client.copy(copy_source, Bucket, destination_key)    
        s3_resource.Object(Bucket, key).delete()
        
move_and_delete_files(spotify_keys, bucket_name)

job.commit()
