import sqlite3


def connect_to_db(connection_string):
    return sqlite3.connect(connection_string)


def create_rss_feed_table(conn) -> None:
    conn.cursor().execute(
        """
        CREATE TABLE IF NOT EXISTS rss_feeds (
            id INTEGER PRIMARY KEY,
            feed_url TEXT UNIQUE,
            date_added TEXT,
            title TEXT UNIQUE,
            rss_version TEXT
        )
        """
    )
    conn.commit()


def insert_rss_feed(conn, feed_url, title, rss_version) -> None:
    conn.cursor().execute(
        """
        INSERT OR IGNORE INTO rss_feeds (feed_url, date_added, title, rss_version)
        VALUES (:feed_url, CURRENT_TIMESTAMP, :title, :rss_version)
        """,
        {"feed_url": feed_url, "title": title, "rss_version": rss_version}
    )
    conn.commit()


def read_rss_feed(conn) -> list:
    cur = conn.cursor()
    cur.execute("""SELECT * FROM rss_feeds""")
    results = cur.fetchall()
    cur.close()
    return results


def create_article_table(conn) -> None:
    conn.cursor().execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER primary key,
            base_url TEXT,
            url TEXT UNIQUE,
            date_added TEXT, 
            title TEXT UNIQUE,
            FOREIGN KEY(base_url) REFERENCES rss_feeds(feed_url)
        )
        """
    )
    conn.commit()


def insert_article(conn, base_url, url, title) -> None:
    conn.cursor().execute(
        """
        INSERT OR IGNORE INTO articles (base_url, url, date_added, title)
        VALUES (:base_url, :url, CURRENT_TIMESTAMP, :title)
        """,
        {"base_url": base_url, "url": url, "title": title}
    )
    conn.commit()


def read_article(conn) -> list:
    cur = conn.cursor()
    cur.execute("""SELECT * FROM articles""")
    results = cur.fetchall()
    cur.close()
    return results


def create_weaviate_table(conn) -> None:
    conn.cursor().execute(
        """
        CREATE TABLE IF NOT EXISTS weaviate (
            id INTEGER primary key,
            url TEXT UNIQUE,
            date_added TEXT, 
            uuid TEXT UNIQUE,
            FOREIGN KEY(url) REFERENCES articles(url)
        )
        """
    )
    conn.commit()


def insert_weaviate(conn, url, uuid) -> None:
    conn.cursor().execute(
        """
        INSERT OR IGNORE INTO weaviate (url, date_added, uuid)
        VALUES (:url, CURRENT_TIMESTAMP, :uuid)
        """,
        {"url": url, "uuid": uuid}
    )
    conn.commit()


def get_registry_article(conn):
    cur = conn.cursor()
    cur.execute(
        """     
        SELECT
            rss_feeds.title,
            articles.url,
            articles.title,
            weaviate.uuid
        FROM weaviate
        INNER JOIN articles ON weaviate.url = articles.url
        INNER JOIN rss_feeds ON articles.base_url = rss_feeds.feed_url
        """
    )
    results = cur.fetchall()
    cur.close()
    return results


# def create_parser_table(self):
#     self.connection.cursor().execute(
#         """
#         CREATE TABLE IF NOT EXISTS parsers (
#             base_url TEXT primary key,
#             date_added TEXT,
#             title TEXT,
#             summary TEXT,
#             paragraphs TEXT,
#             source TEXT
#         )
#         """
#     )
#     self.connection.commit()
#
#
# def insert_parser(self, base_url, title, summary, paragraphs, source):
#     self.connection.cursor().execute(
#         """
#         INSERT INTO parsers (base_url, date_added, title, summary, paragraphs, source)
#         VALUES (:base_url, CURRENT_TIMESTAMP, :title, :summary, :paragraphs, :source)
#         """,
#         {"base_url": base_url, "title": title, "summary": summary, "paragraphs": paragraphs, "source": source}
#     )
#     self.connection.commit()
#
#
# def get_parser(self, base_url):
#     return self.connection.cursor().execute(
#         """
#         SELECT *
#         FROM parsers
#         WHERE base_url = ?
#         ORDER BY date_added ASC
#         """,
#         (base_url,)
#     ).fetchall()
