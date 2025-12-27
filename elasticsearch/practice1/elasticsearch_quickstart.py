from datetime import datetime

from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch("http://localhost:9200")
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

    es.index(
        index=index_name,
        document={
            "title": "Elasticsearch in Action",
            "author": "Radu Gheorghe",
            "price": 59.9,
            "published_at": datetime.utcnow(),
            "tags": ["search", "es", "backend"],
        },
    )

    es.indices.refresh(index=index_name)

    resp = es.search(
        index=index_name,
        query={"match": {"title": "elasticsearch"}},
    )

    for hit in resp["hits"]["hits"]:
        print(hit["_source"]["title"], hit["_source"]["author"])


if __name__ == "__main__":
    main()
