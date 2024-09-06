import taipy as tp
import pandas as pd
from taipy import Config, Scope, Gui

# Сценарий Taipy и управление данными 

# Функция фильтрации (задача) 
def filter_genre(initial_dataset: pd.DataFrame, selected_genre):
    filtered_dataset = initial_dataset[initial_dataset["genres"].str.contains(selected_genre)]
    filtered_data = filtered_dataset.nlargest(7, "Popularity %")
    return filtered_data

# Загрузка конфигурации, выполненной с помощью Taipy Studio
Config.load("config.toml")
print(Config.scenarios)

scenario_cfg = Config.scenarios["scenario"]

# Запуск сервиса Taipy Core
tp.Core().run()

# Создание сценария
scenario = tp.create_scenario(scenario_cfg)

# Пользовательский интерфейс Taipy 
# Добавим GUI в систему управления сценариями для создания полнофункционального приложения

# Определение обратного вызова - передача сценария с определением жанра
def on_genre_selected(state):
    scenario.selected_genre_node.write(state.selected_genre)
    tp.submit(scenario)
    state.df = scenario.filtered_data.read()

# Получение списка жанров
genres = [
    "Action", "Adventure", "Animation", "Children", "Comedy", "Fantasy", "IMAX"
    "Romance","Sci-FI", "Western", "Crime", "Mystery", "Drama", "Horror", "Thriller", "Film-Noir","War", "Musical", "Documentary"
    ]

# Инициализация переменных
df = pd.DataFrame(columns=["Title", "Popularity %"])
selected_genre = "Action"

## Установка первичного значения Action
def on_init(state):
    on_genre_selected(state)

# Определение пользовательского интерфейса 
my_page = """
# Film recommendation
## Choose your favorite genre
<|{selected_genre}|selector|lov={genres}|on_change=on_genre_selected|dropdown|>
## Here are the top seven picks by popularity
<|{df}|chart|x=Title|y=Popularity %|type=bar|title=Film Popularity|>
"""
Gui(page=my_page).run()