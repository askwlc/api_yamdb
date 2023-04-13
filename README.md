### ЯП - Спринт 10 - Проект YaMDb (групповой проект). Python-разработчик бекенд в Яндекс.Практикум.
### Описание

![Logo](https://cdn-irec.r-99.com/sites/default/files/product-images/399872/EOXOqQkXnjTMTRnIpMUSvQ.jpg)

Команда разработки: 

- :white_check_mark: [Nikita Shinkov (в роли Python-разработчика Тимлид - разработчик 2)](https://github.com/#)
- :white_check_mark: [Igor Merkushev (в роли Python-разработчика - разработчик 1)](https://github.com/#)
- :white_check_mark: [Sergei Tregubov (в роли Python-разработчика - разработчик 3)](https://github.com/SergeiTregubov/)


Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Стек технологий использованный в проекте:
- Python 3.7
- Django 3.2
- DRF 3.12.4
- PyJWT 2.1.0


## Техническое описание проекта YaMDb:

### Ресурсы API YaMDb:
- auth: аутентификация.
- users: пользователи.
- titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Пользовательские роли:
Аноним, Аутентифицированный пользователь, Модератор, Администратор, Суперюзер.

Реализована самостоятельная регистрация пользователей через эндпоинт /api/v1/auth/signup/ с последующим получением JWT-токена.

## Инструкция по установке:

Для запуска проекта необходимо клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/askwlc/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv        (для *nix-систем)
source venv/bin/activate    (для *nix-систем)
```
```
python -m venv venv         (для Windows-систем)
venv/Scripts/activate.bat   (для Windows-систем)
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip    (для *nix-систем)
python -m pip install --upgrade pip     (для Windows-систем)
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate   (для *nix-систем)
python manage.py migrate    (для Windows-систем)
```
Запустить проект:
```
python3 manage.py runserver (для *nix-систем)
python manage.py runserver  (для Windows-систем)
```

Перейти в браузере по адресу
```
http://127.0.0.1:8000
```
