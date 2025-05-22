import pandas as pd
from sklearn.neighbors import NearestNeighbors
import os

# Абсолютный путь к CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "data", "top_100k_tracks.csv")
print("📁 CSV path inside container:", csv_path)
print("✅ Exists?", os.path.exists(csv_path))

# Загрузка и очистка данных
df = pd.read_csv(csv_path)
df = df[['name', 'artists', 'valence', 'energy', 'tempo']].dropna()

# Обучение KNN
features = df[['valence', 'energy', 'tempo']]
knn = NearestNeighbors(n_neighbors=5)
knn.fit(features)

def get_recommendations(valence, energy, tempo):
    try:
        query = [[valence, energy, tempo]]
        _, indices = knn.kneighbors(query)
        result = df.iloc[indices[0]][['name', 'artists', 'tempo']]
        return result.to_dict(orient='records')
    except Exception as e:
        print("❌ Ошибка в get_recommendations:", e)
        return []