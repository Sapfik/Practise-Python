#! /bin/bash

cd /home/auto_ru_scrapper/auto_ru_scrapper/scrapper
source venv/bin/activate

cd auto_ru

# Санкт-Петербург

offers_scrapper_processes=$(pgrep -f offers_scrapper.py)

if [[ -z $offers_scrapper_processes ]]; then
  echo 'Запускаем сбор объявлений (Санкт-Петербург)'
  python offers_scrapper.py
else
  echo 'Сбор объявлений уже запущен (Санкт-Петербург)'
fi

offers_data_scrapper_processes=$(pgrep -f offers_data_scrapper.py)

if [[ -z $offers_data_scrapper_processes ]]; then
  echo 'Запускаем сбор данных у объявлений (Санкт-Петербург)'
  python offers_data_scrapper.py
else
  echo 'Сбор объявлений у объявлений уже запущен (Санкт-Петербург)'
fi

offers_check_processes=$(pgrep -f offers_check.py)

if [[ -z $offers_check_processes ]]; then
  echo 'Запускаем проверку объявлений (Санкт-Петербург)'
  python offers_check.py
else
  echo 'Проверка объявлений уже запущена (Санкт-Петербург)'
fi
