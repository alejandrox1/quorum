#!/bin/bash

export KAFKA_HEAP_OPTS="-Xmx100M -Xms100M"

nohup /kafka/bin/kafka-server-start.sh -daemon /kafka/config/server.properties > /dev/null 2>&1 &

