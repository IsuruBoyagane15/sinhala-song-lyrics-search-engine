from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json

es_client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'songs'


def index():
    songs_index = Index(INDEX, using=es_client)
    res = songs_index.create()
    helpers.bulk(es_client, create_bulk())
    print(res)


def create_bulk():
    for i in range(20):
        with open("songs/" + str(i) + ".json") as json_file:
            json_data = json.load(json_file)
        print(json_data)
        yield {
            "_index": INDEX,
            "_source": {
                "title": json_data['title'],
                # "title_si": json_data['title_si'],
                "artist": json_data['Artist'],
                "genre": json_data['Genre'],
                "lyrics": json_data['Lyrics'],
                "music": json_data['Music'],
                "guitar_key": json_data['guitar_key'],
                "beat": json_data['beat'],
                "song_lyrics": json_data['song_lyrics'],
                "number_of_visits": json_data['number_of_visits'],
                "number_of_shares": json_data['number_of_shares'],
            },
        }

# Call elasticsearch bulk API to create the index
if __name__ == "__main__":
    index()
