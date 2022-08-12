#!/bin/bash

cd /home/auto_ru_scrapper/auto_ru_scrapper/scrapper
source venv/bin/activate

cd service

export_processes=$(pgrep -f export_offers.py)

if [[ -z $export_processes ]]; then
  echo 'Запускаем экспорт предложений'
  python export_offers.py
else
  echo 'Экспорт предложений уже запущен'
fi
