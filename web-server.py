#!/usr/bin/env python
import random
import datetime
import time

from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import BadRequest
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
import couchbase.fulltext as FT
import couchbase.exceptions as E

app = Flask(__name__)

# Lab 2: Connect to the cluster

@app.route('/', methods=['GET'])
def shop():
    # Lab 2: Retrieve items document from the bucket

    return render_template('shop.html', random=random, sorted=sorted,
                           display_url="", items=None)


@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    order = request.form.getlist('order[]')
    print 'name=', name
    print 'order=', order

    if len(order) != 5:
        raise BadRequest('Must have 5 items in the order')

    # Lab 3: Insert the order document into the bucket

    return '', 204


@app.route('/filter', methods=['GET'])
def filter_items():
    filter_type = request.args.get('type')
    keys = []
    print 'type=', filter_type

    # Lab 4: Use N1QL to retrieve products that match the requested category

    print 'Found results:', ', '.join(keys), 'for type', filter_type
    return jsonify({'keys': keys})


@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q')
    print 'User searched for', search_term
    keys = []

    # This is the part the user has to fill in
    # Bonus points for fuzzy searching
    # They can make this as simple or complex as they want
    result = bucket.search('matt', FT.MatchQuery(search_term, fuzziness=1))
    for row in result:
        keys.append(row['id'])

    print 'Found matches', ', '.join(keys)
    return jsonify({'keys': keys})

app.run(host='0.0.0.0',port=8080)
