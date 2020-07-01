from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json

import process_search_query

app = Flask(__name__)
es_client = Elasticsearch(HOST="http://localhost", PORT=9200)

INDEX = 'songs'


@app.route('/', methods=['POST', 'GET'])
def search_box():
    print(request)
    if request.method == 'POST':
        query = request.form['search_term']
        query_body = process_search_query.process_search_query(query)

        response = es_client.search(
            index=INDEX,
            body=json.dumps(query_body)
        )
        hits = response['hits']['hits']
        aggregations = response['aggregations']
        num_results = len(hits)

        # hits
        for i in hits:
            print(i)

        # aggregations
        for j in aggregations:
            print(j)

        # hit count
        print("number of results found :", num_results)

        return render_template('index.html', query=query, hits=hits, num_results=num_results, aggs=aggregations)

    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == "__main__":
    app.run(debug=True)
