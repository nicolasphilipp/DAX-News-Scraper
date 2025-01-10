import psycopg2
from crawler.items import ContentItem
from urllib.parse import urlparse

def open_cursor():
    connection = psycopg2.connect(user="user",
                                  password="password",
                                  host="host",
                                  port="port",
                                  database="database")
    return connection.cursor()

def close_cursor(cursor):
    cursor.close()

def add_Content(content: ContentItem):
    cursor = open_cursor()

    x = content.__str__().split(";;")
    domain = urlparse(x[0]).netloc

    postgres_insert_query = """INSERT INTO content (link, text, date, time, website_url) VALUES (%s,%s,%s,%s,%s)"""
    record_to_insert = (x[0], x[1], x[2], x[3], domain)
    cursor.execute(postgres_insert_query, record_to_insert)

    cursor.connection.commit()

    close_cursor(cursor)

def get_ContentByLink(link: str):
    cursor = open_cursor()

    query = """SELECT link, text, date, time, website_url FROM content WHERE link = %s"""

    cursor.execute(query, (link,))    
    return cursor.fetchall()

def get_Content():
    cursor.execute("""SELECT link, text, date, time, website_url FROM content""")
    return  cursor.fetchall()
