import sqlite3
from weaviate import Client


def _get_objects_class(client: Client, class_name: str):
    return client.data_object.get(class_name=class_name)


def get_articles(client: Client):
    return _get_objects_class(client, class_name="Article")


def get_paragraphs(client: Client):
    return _get_objects_class(client, class_name="Paragraph")


def get_contextionary_concept_vector(client: Client, concept: str):
    return client.contextionary.get_concept_vector(concept=concept)


def post_contextionary_concept(client, concept, definition, weight) -> None:
    client.contextionary.extend(concept=concept, definition=definition, weight=weight)


def connect_to_db(connection_string):
    return sqlite3.connect(connection_string)


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


def gql_search_summary_dual(client, keywords: str, concepts: str, limit: int = 10) -> dict:
    where_filter = {
        "path": ["summary"],
        "operator": "Equal",
        "valueText": keywords
    }

    near_text = {
        "concepts": concepts.split(" "),
    }

    if not concepts:
        return client.query \
            .get("Article", ["title", "summary", "link"]) \
            .with_where(where_filter) \
            .with_limit(10) \
            .do()

    elif not keywords:
        return client.query \
            .get("Article", ["title", "summary", "link"]) \
            .with_near_text(near_text) \
            .with_limit(10) \
            .do()

    elif keywords and concepts:
        return client.query\
            .get("Article", ["title", "summary", "link"]) \
            .with_where(where_filter) \
            .with_near_text(near_text) \
            .with_limit(10)\
            .do()
