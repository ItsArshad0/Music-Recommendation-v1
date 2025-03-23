from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from ytmusicapi import YTMusic
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
ytmusic = YTMusic()

# Load dataset (Ensure this file exists)
df = pd.read_csv('data.csv')

# Define numerical features used for recommendation
numerical_features = [
    "valence", "danceability", "energy", "tempo",
    "acousticness", "liveness", "speechiness", "instrumentalness"
]

# 🔹 Home Route (Serves index.html)
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 API Route to Get Songs from YouTube Music
@app.route("/api/get_songs", methods=["GET"])
def get_songs():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "No song query provided"}), 400

    search_results = ytmusic.search(query, filter="songs")

    songs = [
        {
            "title": song["title"],
            "artist": song["artists"][0]["name"] if song["artists"] else "Unknown",
            "album": song.get("album", {}).get("name", "Unknown"),
            "videoId": song["videoId"],
            "url": f"https://music.youtube.com/watch?v={song['videoId']}",
        }
        for song in search_results
    ]

    return jsonify(songs)

# 🔹 Function to Recommend Songs from Dataset
def recommend_songs(song_name, num_recommendations=5):
    if song_name not in df['name'].values:
        return []

    # Get song's cluster
    song_cluster = df[df["name"] == song_name]["Cluster"].values[0]
    same_cluster_songs = df[df["Cluster"] == song_cluster]

    # Compute similarity
    song_index = same_cluster_songs[same_cluster_songs["name"] == song_name].index[0]
    cluster_features = same_cluster_songs[numerical_features]
    similarity_matrix = cosine_similarity(cluster_features, cluster_features)
    similar_songs = np.argsort(similarity_matrix[song_index])[-(num_recommendations + 1):-1][::-1]

    # Format recommended songs
    recommendations = same_cluster_songs.iloc[similar_songs][["name", "year", "artists"]].to_dict(orient="records")

    return recommendations

# 🔹 Web Route for Song Recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    song_name = request.form.get("song_name")
    recommendations = recommend_songs(song_name)
    return render_template("index1.html", recommendations=recommendations)

# 🔹 API Route for External Use
@app.route("/api/recommend", methods=["GET"])
def api_recommend():
    song_name = request.args.get("song_name", "")
    recommendations = recommend_songs(song_name)
    return jsonify(recommendations)

# 🔹 API Route to Get Song List from Dataset (for Autocomplete)
@app.route("/api/get_song_list", methods=["GET"])
def get_song_list():
    try:
        song_list = df["name"].dropna().unique().tolist()
        return jsonify(song_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)