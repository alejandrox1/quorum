#!/bin/bash


sudo apt-get update -y && sudo apt-get upgrade -y

# Install Oracle JDK 8 using the Webupd8 team PPA repo
sudo add-apt-repository -y ppa:webupd8team/java 
sudo apt-get update -y && sudo apt-get install -y oracle-java8-installer 

# Install Zookeeper open source service for maintaining configuration
# information, providing distributed synchronization, naming and providing
# group services.
sudo apt-get install -y zookeeperd


# Download Kafka
curl http://apache.spinellicreations.com/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz | tar xz
cd /kafka_2.11-0.10.2.0

# Start Kafka server (quick and dirty local setup)
export KAFKA_HEAP_OPTS="-Xmx100M -Xms100M"
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
bin/kafka-server-start.sh -daemon config/server.properties 

# Create topic
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic mariotest
bin/kafka-topics.sh --list --zookeeper localhost:2181

# Send some msgs
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test


# delete topic
bin/kafka-server-stop.sh
bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic mariotest
