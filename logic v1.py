import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import silhouette_score

# Load Dataset
df = pd.read_csv("data.csv")
df = df.sample(n=6000, random_state=42).reset_index(drop=True)  # Sampling for performance

# Features for clustering
numerical_features = [
    'valence', 'danceability', 'energy', 'tempo',
    'acousticness', 'liveness', 'speechiness', 'instrumentalness'
]

# Scale Features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[numerical_features])

# Function to Find Optimal K (Using Silhouette Score)
def find_optimal_clusters(data, max_k=10):
    scores = []
    for k in range(2, max_k + 1):
        kmeans = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=256)
        labels = kmeans.fit_predict(data)
        score = silhouette_score(data, labels)
        scores.append(score)
    
    optimal_k = range(2, max_k + 1)[np.argmax(scores)]
    
    # Plot silhouette scores
    plt.figure(figsize=(10, 6))
    plt.plot(range(2, max_k + 1), scores, marker='o')
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score vs Number of Clusters")
    plt.show()

    return optimal_k

optimal_k = find_optimal_clusters(df_scaled, max_k=10)

# Perform Clustering
kmeans = MiniBatchKMeans(n_clusters=optimal_k, random_state=42, batch_size=256)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Save Clustered Data
df.to_csv("Clustered_data.csv", index=False)

# Perform PCA for Visualization
pca = PCA(n_components=2)
pca_results = pca.fit_transform(df_scaled)

plt.figure(figsize=(10, 6))
plt.scatter(pca_results[:, 0], pca_results[:, 1], c=df['Cluster'], cmap='viridis', alpha=0.5)
plt.colorbar(label="Cluster")
plt.title("K-Means Clustering Visualization (PCA Reduced)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.show()

# Function to Recommend Songs
def recommend_songs(song_name, df, num_recommendations=5):
    if song_name not in df['name'].values:
        return f"'{song_name}' not found in the dataset."

    song_cluster = df[df['name'] == song_name]['Cluster'].values[0]
    same_cluster_songs = df[df['Cluster'] == song_cluster].reset_index(drop=True)

    song_index = same_cluster_songs[same_cluster_songs['name'] == song_name].index[0]
    cluster_features = same_cluster_songs[numerical_features]

    similarity_matrix = cosine_similarity(cluster_features, cluster_features)
    similar_songs = np.argsort(similarity_matrix[song_index])[-(num_recommendations + 1):-1][::-1]

    return same_cluster_songs.iloc[similar_songs][['name', 'year', 'artists']]

# Example Song Recommendation
test_song = "Soul Junction"
recommended_songs = recommend_songs(test_song, df, num_recommendations=5)

print(f"Songs similar to '{test_song}':")
print(recommended_songs)