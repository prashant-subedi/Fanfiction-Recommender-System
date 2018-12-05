#!/bin/bash
#### Change this path to reflect the location of virtual env"
source config.sh
if [ ! -z "$VIRTUALENV_DIR" ] 
then
	cd $VIRTUALENV_DIR
	source bin/activate
fi
cd $PROJECT_DIR/Scraper
while [ 1 ];do
	echo "Starting Crawler"
	scrapy crawl minimal
	echo "Proably Finised or Killed. Sleeping for 15 minutes"
	sleep 900
done
