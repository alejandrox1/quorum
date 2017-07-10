#!/bin/bash

set -o xtrace 

clear

# Start Kafka server
cd kafka/
sudo docker-compose down --remove-orphans
cd ../


# Start DB
cd storage/
sudo docker-compose down --remove-orphans                                       
cd ../

# Start scrapers
sudo docker-compose down --remove-orphans
cd quorum/twitter/
sudo docker-compose down --remove-orphans                                       
cd ../../

# Start queue
cd celery/
sudo docker-compose down --remove-orphans                                      
cd ..
