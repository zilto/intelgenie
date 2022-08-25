import sqlite3


class Registry:
    def __init__(self, dbname):
        self.connection = sqlite3.connect(dbname)

    @property
    def cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def create_article_table(self):
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS articles (
                uuid TEXT primary key,
                date_added TEXT, 
                url TEXT,
                filepath TEXT
            )
            """
        )

    def insert_article(self, uuid, url, filepath):
        self.connection.execute(
            """INSERT INTO articles (uuid, date_added, url, filepath)
            VALUES (:uuid, CURRENT_TIMESTAMP, :url, :filepath)
            """,
            {"uuid": uuid, "url": url, "filepath": str(filepath)}
        )
