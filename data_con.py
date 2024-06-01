import mysql.connector
from mysql.connector import Error


def check_database_availability(mysql_hostname, mysql_port, mysql_username, mysql_password, mysql_database):
    try:
        connection = mysql.connector.connect(
            host=mysql_hostname,
            user=mysql_username,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port
        )
        if connection.is_connected():
            print(f"Successfully connected to the database '{mysql_database}' on the MySQL server '{mysql_hostname}'")
            connection.close()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False


from datetime import datetime


def convert_to_sql_format(iso_datetime_str):
    # Parse the ISO 8601 datetime string
    parsed_datetime = datetime.strptime(iso_datetime_str, '%Y-%m-%dT%H:%M:%SZ')

    # Format the datetime in SQL format
    sql_datetime_str = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return sql_datetime_str


# Example usage
iso_datetime_str = '2023-09-14T16:25:39Z'
sql_datetime_str = convert_to_sql_format(iso_datetime_str)
print(sql_datetime_str)  # Output: 2023-09-14 16:25:39


class Custom_sql_connector:
    def __init__(self, host, host_port, con_username, con_password, database_name="Utube_DHW4"):
        self.connection = None
        self.cursor = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=con_username,
                password=con_password,
                database=database_name,
                port=host_port
            )
        except Error as e:
            print(f"Error: {e}")

    def create_tables(self):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()

            # Create Channel table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Channel (
                    channel_id VARCHAR(255) PRIMARY KEY,
                    channel_name VARCHAR(255),
                    channel_type VARCHAR(255),
                    channel_views INT,
                    channel_description TEXT,
                    channel_status VARCHAR(255)
                )
            """)

            # Create Playlist table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Playlist (
                    playlist_id VARCHAR(255) PRIMARY KEY,
                    playlist_name VARCHAR(255),
                    channel_id VARCHAR(255)
                )
            """)

            # Create Comment table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Comment (
                    comment_id VARCHAR(255) PRIMARY KEY,
                    video_id VARCHAR(255),
                    comment_text TEXT,
                    comment_author VARCHAR(255),
                    comment_published_date DATETIME
                )
            """)

            # Create Video table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Video (
                    video_id VARCHAR(255) PRIMARY KEY,
                    playlist_id VARCHAR(255),
                    video_name VARCHAR(255),
                    video_description TEXT,
                    publish_date DATETIME,
                    view_count INT,
                    like_count INT,
                    dislike_count INT,
                    favourite_count INT,
                    comment_count INT,
                    duration INT,
                    thumbnail VARCHAR(255),
                    caption_status VARCHAR(255)
                )
            """)

            self.connection.commit()
            print("Tables created successfully")
        else:
            print("Database connection is not established")

    def upload_channel_data(self, channel_id, name, channel_type, views, description, status):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Channel table
            query = "INSERT INTO Channel (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (channel_id, name, channel_type, views, description, status))
            self.connection.commit()
            print("Data uploaded to Channel table successfully")
        else:
            print("Database connection is not established")

    def upload_playlist_data(self, playlist_name, playlist_id, channel_id):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Playlist table
            query = "INSERT INTO Playlist (playlist_name, playlist_id, channel_id) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (playlist_name, playlist_id, channel_id))
            self.connection.commit()
            print("Data uploaded to Playlist table successfully")
        else:
            print("Database connection is not established")

    def upload_video_data(self, video_id, playlist_id, video_name, video_description, publish_date, view_count,
                          like_count, dislike_count, favourite_count, comment_count, duration, thumbnail,
                          caption_status):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Video table
            query = "INSERT INTO Video (video_id, playlist_id, video_name, video_description, publish_date, view_count, like_count, dislike_count, favourite_count, comment_count, duration, thumbnail, caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (video_id, playlist_id, video_name, video_description, publish_date, view_count,
                                        like_count, dislike_count, favourite_count, comment_count, duration, thumbnail,
                                        caption_status))
            self.connection.commit()
            print("Data uploaded to Video table successfully")
        else:
            print("Database connection is not established")

    def upload_comment_data(self, comment_id, video_id, comment_text, comment_author, comment_published_date):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Comment table
            query = "INSERT INTO Comment (comment_id, video_id, comment_text, comment_author, comment_published_date) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (comment_id, video_id, comment_text, comment_author, comment_published_date))
            self.connection.commit()
            print("Data uploaded to Comment table successfully")
        else:
            print("Database connection is not established")


