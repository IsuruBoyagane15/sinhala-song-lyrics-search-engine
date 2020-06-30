from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json

es_client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'songs'

configs = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "analysis": {
            "analyzer": {
                "sinhala-ngram": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "char_filter": ["punc_char_filter"],
                    "token_filter": [
                        "edge_n_gram_filter"
                    ]
                },
                "sinhala": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "char_filter": ["punc_char_filter"]
                },
                "english":{
                    "type": "custom",
                    "tokenizer": "classic",
                    "char_filter": ["punc_char_filter"],
                },
                "sinhala-search": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["punc_char_filter"]
                },
                # "beat-search": {
                #     "type": "custom",
                #     "tokenizer": "standard",
                # },
            },
            "char_filter": {
                "punc_char_filter": {
                    "type": "mapping",
                    "mappings": [".=>", "|=>", "-=>", "_=>", "'=>", "/=>", ",=>", "?=>"]
                }
            },
            "token_filter": {
                "edge_n_gram_filter": {
                    "type": "edge_ngram",
                    "min_gram": "2",
                    "max_gram": "20",
                    "side": "front"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "long"
            },
            "title": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "artist": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "genre": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "lyrics": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "music": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "guitar_key": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
            },
            "beat": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                # "analyzer" : "english",
                # "search_analyzer": "beat-search"
            },
            "song_lyrics": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala",
                "search_analyzer": "sinhala-search"
            },
            "number_of_visits": {
                "type": "long"
            },
            "number_of_shares": {
                "type": "long"
            }
        }
    }
}


def index():
    # songs_index = Index(INDEX, using=es_client)
    # res = songs_index.create()

    res = es_client.indices.create(index=INDEX, body=configs)
    print(res)

    helpers.bulk(es_client, create_bulk())
    print(res)


def create_bulk():
    for i in range(510):
        with open("processed/" + str(i) + ".json") as json_file:
            json_data = json.load(json_file)
        print(json_data)
        yield {
            "_index": INDEX,
            "_source": {
                "title": json_data['title'],
                "artist": json_data['Artist'],
                "genre": json_data['Genre'],
                "lyrics": json_data['Lyrics'],
                "music": json_data['Music'],
                "guitar_key": json_data['guitar_key'],
                "beat": json_data['beat'],
                "number_of_visits": json_data['number_of_visits'],
                "number_of_shares": json_data['number_of_shares'],
                "song_lyrics": json_data['song_lyrics'],
            },
        }


# Call elasticsearch bulk API to create the index
if __name__ == "__main__":
    index()
