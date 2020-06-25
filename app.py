from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)
es_client = Elasticsearch(HOST="http://localhost", PORT=9200)
import json

INDEX = 'songs'


@app.route('/', methods=['POST', 'GET'])
def search_box():
    print(request)
    if request.method == 'POST':
        query = request.form['search_term']
        print(query)
        body = {
            "query":
                {"match":
                     {"title_en": query}
                 }
        }
        response = es_client.search(
            index=INDEX,
            body=json.dumps(body)
        )
        hits = response['hits']['hits']
        print(hits)
        for i in hits:
            print(i)
            print(i["_source"])
        num_results = len(hits)

        return render_template('index.html', query=query, hits=hits, num_results=num_results)
    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == "__main__":
    app.run(debug=True)
