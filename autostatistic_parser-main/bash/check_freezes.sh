#! /bin/bash

FREEZE_TIME=600
OFFERS_SCRAPPER_PNAME='offers_scrapper.py'
offers_scrapper_pid=$(pgrep -f -o $OFFERS_SCRAPPER_PNAME)

if [[ -z $offers_scrapper_pid ]]; then
  exit 1
fi

echo 'Процесс имеется...'
offers_scrapper_ptime=$(ps -p $offers_scrapper_pid -o etimes | sed -e 's/[^0-9]*//g')

if [[ $offers_scrapper_ptime -gt $FREEZE_TIME ]]; then
  echo 'Возможно процесс завис. Закрываем...'
  kill $(ps aux | grep 'python $OFFERS_SCRAPPER_PNAME' | awk '{print $2}')
  exit 1
fi

echo 'Процесс работает нормально.'
echo "Время работы процесса: $offers_scrapper_ptime с."

