#!/usr/bin/evn python

import sqlite3

from flask import Flask, jsonify, g

app = Flask(__name__)

DATABASE = 'union-bridge'

def query_db(query, args=(), one=False):
    cur=g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route("/")
def index():
    test = {
            "version": "0.0.1",
            "name": "historical-api",
            "tables": ("buildings", "facts", "sources", "subjects"),
            }
    return jsonify(test)

@app.route("/buildings")
def buildings():
    values = []
    for building in query_db('select * from buildings'):
        values.push(building)
    return(jsonify(values))

@app.route("/facts")
def facts():
    values = []
    for fact in query_db('select * from facts'):
        values.push(fact)
    return(jsonify(values))

@app.route("/sources")
def sources():
    values = []
    for source in query_db('select * from sources'):
        values.push(source)
    return(jsonify(values))

@app.route("/subjects")
def subjects():
    values = []
    for subject in query_db('select * from subjects'):
        values.push(subject)
    return(jsonify(values))


@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
