#!/bin/bash

cd /home/auto_ru_scrapper/auto_ru_scrapper/scrapper
source venv/bin/activate
cd checks

check_sold_process=$(pgrep -f offers_check_sold.py)

if [[ -z $check_sold_process ]]; then
  echo 'Запускаем проверку изменения статуса «Продан».'
  python offers_check_sold.py
else
  echo 'Проверка изменения статуса «Продан» уже запущена.'
fi
