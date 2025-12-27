from datetime import datetime, timezone

import os

from elasticsearch import Elasticsearch


def main():
    es_url = os.getenv("ES_URL", "http://localhost:9200")
    es_user = os.getenv("ES_USER")
    es_password = os.getenv("ES_PASSWORD")
    es_api_key = os.getenv("ES_API_KEY")

    if es_api_key:
        es = Elasticsearch(es_url, api_key=es_api_key)
    elif es_user and es_password:
        es = Elasticsearch(es_url, basic_auth=(es_user, es_password))
    else:
        es = Elasticsearch(es_url)
    index_name = "books"

    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    "title": {"type": "text"},
                    "author": {"type": "keyword"},
                    "price": {"type": "float"},
                    "published_at": {"type": "date"},
                    "tags": {"type": "keyword"},
                }
            },
        )

    # Use a fixed ID so re-runs update instead of creating duplicates.
    es.index(
        index=index_name,
        id="book-1",
        document={
            "title": "Elasticsearch in Action",
            "author": "Radu Gheorghe",
            "price": 59.9,
            "published_at": datetime.now(timezone.utc),
            "tags": ["search", "es", "backend"],
        },
    )

    es.index(
        index=index_name,
        id="book-2",
        document={
            "title": "Designing Data-Intensive Applications",
            "author": "Martin Kleppmann",
            "price": 79.0,
            "published_at": datetime.now(timezone.utc),
            "tags": ["data", "distributed", "backend"],
        },
    )

    es.index(
        index=index_name,
        id="book-3",
        document={
            "title": "Learning Elasticsearch",
            "author": "Prabhakaran",
            "price": 45.0,
            "published_at": datetime.now(timezone.utc),
            "tags": ["search", "es"],
        },
    )

    es.indices.refresh(index=index_name)

    print("== Match query: title contains 'elasticsearch' ==")
    resp = es.search(
        index=index_name,
        query={"match": {"title": "elasticsearch"}},
    )

    for hit in resp["hits"]["hits"]:
        src = hit["_source"]
        print(src["title"], src["author"], "score=", hit["_score"])

    print("== Term query: author equals 'Radu Gheorghe' ==")
    resp = es.search(
        index=index_name,
        query={"term": {"author": "Radu Gheorghe"}},
    )
    for hit in resp["hits"]["hits"]:
        src = hit["_source"]
        print(src["title"], src["author"])

    print("== Aggregation: price stats ==")
    resp = es.search(
        index=index_name,
        size=0,
        aggs={"price_stats": {"stats": {"field": "price"}}},
    )
    print(resp["aggregations"]["price_stats"])


if __name__ == "__main__":
    main()
