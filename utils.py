from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json

es_client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'songs'


def index():
    songs_index = Index(INDEX, using=es_client)
    res = songs_index.create()
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
