import pandas as pd

df = pd.read_csv('/datasets/yandex_music_project.csv')

# получение первых 10 строк таблицы df
df.head(10)
# получение общей информации о данных в таблице df
df.info()

# перечень названий столбцов таблицы df
df.columns
# переименование столбцов
df = df.rename(columns={'  userID': 'user_id', 'Track': 'track', '  City  ': 'city', 'Day': 'day'})
# проверка результатов - перечень названий столбцов
df.columns

# подсчёт пропусков
df.isna().sum()
# перебор названий столбцов в цикле и замена пропущенных значений на 'unknown'
columns_to_replace = ['track', 'artist', 'genre']
for column in columns_to_replace:
    df[column].fillna(value='unknown', inplace=True)
# подсчёт пропусков
df.isna().sum()

# подсчёт явных дубликатов
df.duplicated().sum()
# удаление явных дубликатов (с удалением старых индексов и формированием новых)
df.drop_duplicates(inplace=True)
# проверка на отсутствие дубликатов
df.duplicated().sum()
# Просмотр уникальных названий жанров
unique_genres = df['genre'].sort_values().unique()
print(unique_genres)
# Устранение неявных дубликатов
df['genre'].replace(['hip', 'hop', 'hip-hop'], 'hiphop', inplace=True)
# Проверка на неявные дубликаты
unique_genres = df['genre'].sort_values().unique()
print(unique_genres)

# Подсчёт прослушиваний в каждом городе
city_groups = df.groupby('city')
city_tracks_count = city_groups['track'].count()
print(city_tracks_count)
# Подсчёт прослушиваний в каждый из трёх дней
grouped_by_day = df.groupby('day')['time'].count()
print(grouped_by_day)
#Функция объединения группировки по городу и по дням недели
def number_tracks(day, city):
    track_list = df.loc[df['day'] == day].loc[df['city'] == city]
    track_list_count = track_list['user_id'].count()
    return track_list_count

# количество прослушиваний в Москве по понедельникам
number_tracks('Monday', 'Moscow')
# количество прослушиваний в Санкт-Петербурге по понедельникам
number_tracks('Monday', 'Saint-Petersburg')
# количество прослушиваний в Москве по средам
number_tracks('Wednesday', 'Moscow')
# количество прослушиваний в Санкт-Петербурге по средам
number_tracks('Wednesday', 'Saint-Petersburg')
# количество прослушиваний в Москве по пятницам
number_tracks('Friday', 'Moscow')
# количество прослушиваний в Санкт-Петербурге по пятницам
number_tracks('Friday', 'Saint-Petersburg')

# Таблица с результатами
data = [['Москва', number_tracks('Monday', 'Moscow'), number_tracks('Wednesday', 'Moscow'), number_tracks('Friday', 'Moscow')],
         ['Санкт-Петербург', number_tracks('Monday', 'Saint-Petersburg'), number_tracks('Wednesday', 'Saint-Petersburg'), number_tracks('Friday', 'Saint-Petersburg')]]
info = pd.DataFrame(data, columns=['city', 'monday', 'wednesday', 'friday'])
print(info)

moscow_general = df[df['city'] == 'Moscow']
spb_general = df[df['city'] == 'Saint-Petersburg']

def genre_weekday(df, day, time1, time2):
    # последовательная фильтрация
    # оставляем в genre_df только те строки df, у которых день равен day
    genre_df = df[df['day'] == day]
    # оставляем в genre_df только те строки genre_df, у которых время меньше time2
    genre_df = genre_df[genre_df['time'] < time2]
    # оставляем в genre_df только те строки genre_df, у которых время больше time1
    genre_df = genre_df[genre_df['time'] > time1]
    # сгруппируем отфильтрованный датафрейм по столбцу с названиями жанров, возьмём столбец genre и посчитаем кол-во строк для каждого жанра методом count()
    genre_df_grouped = genre_df.groupby('genre')['genre'].count()
    # отсортируем результат по убыванию (чтобы в начале Series оказались самые популярные жанры)
    genre_df_sorted = genre_df_grouped.sort_values(ascending=False)
    # вернём Series с 10 самыми популярными жанрами в указанный отрезок времени заданного дня
    return genre_df_sorted[:10]

# вызов функции для утра понедельника в Москве
genre_weekday(moscow_general, 'Monday', '07:00', '11:00')
# вызов функции для утра понедельника в Петербурге
genre_weekday(spb_general, 'Monday', '07:00', '11:00')
# вызов функции для вечера пятницы в Москве
genre_weekday(moscow_general, 'Friday', '17:00', '23:00')
# вызов функции для вечера пятницы в Петербурге
genre_weekday(spb_general, 'Friday', '17:00', '23:00')

# одной строкой: группировка таблицы moscow_general по столбцу 'genre',
# подсчёт числа значений 'genre' в этой группировке методом count(),
# сортировка получившегося Series в порядке убывания и сохранение в moscow_genres
moscow_genres = moscow_general.groupby('genre')['genre'].count().sort_values(ascending=False)
moscow_genres

# просмотр первых 10 строк moscow_genres
moscow_genres.head(10)

# одной строкой: группировка таблицы spb_general по столбцу 'genre',
# подсчёт числа значений 'genre' в этой группировке методом count(),
# сортировка получившегося Series в порядке убывания и сохранение в spb_genres
spb_genres = spb_general.groupby('genre')['genre'].count().sort_values(ascending=False)
print(spb_genres)
# просмотр первых 10 строк spb_genres
spb_genres.head(10)
