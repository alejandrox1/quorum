#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           
set -x  

# Start Kafka server
cd kafka/
./setup_kafka.sh
cd ../


# Start DB
cd storage/
./start_app.sh
cd ../

# Start scrapers
cd quorum/twitter/
./start_app.sh
cd ../../

# Start queue
cd celery/
./start_app.sh
