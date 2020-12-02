# Тестовое задание

Программа, на основе конфигурационного словаря `NEWS_FEEDS_CONFIG`, создает методы для класса Grabber с именами новостных лент.
Каждая лента, имеет два свойства: news и grub.

`news` - выводит последние `limit` новостей в кратком виде
`grub` - выводит детали по `url`

## Установка и использование

Для корректного использования нужен [python 3.+](https://python.org)
Для установки, рекомендуется создать окружение и установить зависимости.
Пример эксплуатации для linux.
```
python3 -m venv venv
source 'venv/bin/activate'
pip install -r requirements.txt
python news_grabber.py
```

## Конфигурация

Для управления новостными потоками необходимо настроить словарь `NEWS_FEEDS_CONFIG`
ключами словаря будет имя метода класса `Grabber`, а значением вложенный словарь с ссылкой на поток `url`, и тегами, 
которые необходимо отпарсить для выделения заголовка, тела статьи, иллюстрации, в некоторых случаях кодировки.

## Ограничения
К сожалению, на текущий момент не представляется возможным реализовать быстрое добавление дополнительных новостных лент,
в силу того, что на каждом сайт может быть своя структура тегов. Поэтому без аналитики не обойтись.

## Author

Patsy Charmer. My git [there](https://github.com/fromRussiaImportLove)
