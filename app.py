import json

import pandas as pd
from altair import limit_rows
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import for handling Cross-Origin Resource Sharing
import pickle

with open('movie_reccomendation.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

similarity, new_movies = loaded_data


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (can be configured more specifically)


@app.route('/')
def hello():
    typeof = new_movies.title.sample(10).tolist()
    return jsonify(typeof)


def findreccomendation(movie_name):
    movie_index = new_movies[new_movies.title == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    movie_reccomend_index = [index for index, values in movies_list]
    movie_name = new_movies.iloc[movie_reccomend_index]
    moviesval = movie_name[['movie_id', 'title']]
    movie_jsonified = moviesval.to_json(orient="records")
    return json.loads(movie_jsonified)



@app.route('/Movie_Recommendation/<string:movie_name>')
def movie_recommendation(movie_name):

    recommendations = findreccomendation(movie_name)
    return recommendations # Return the recommendations directly

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)