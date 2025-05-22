# Описание данных

- Для проекта был использован датасет top_100k_tracks.csv, содержащий сведения о 90 000 музыкальных треках.

## Основные характеристики:
- 24 признака, включая числовые (valence, energy, tempo, duration_ms) и категориальные (name, artists, album, release_date);
- ~30% пропущенных значений (особенно в name, album, release_date);
- Аномалии в полях duration_ms и tempo, что потребовало фильтрации;
- Корреляции: высокая зависимость между valence, energy, tempo, danceability.







