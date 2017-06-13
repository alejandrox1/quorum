from kafka import KafkaProducer, KafkaConsumer

singal_msg = 'live with more freedom than anyone else in the world!'

def produce_element(topic, element):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send(topic, element.encode('utf-8'))

def produce_iterator(topic, iterator):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for i in iterator:
        producer.send(topic, i.encode('utf-8'))

def terminate_producer(topic):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')                
    producer.send(topic, singal_msg.encode('utf-8'))

def consume(topic):
    consumer = KafkaConsumer(topic, auto_offset_reset='earliest')
    for msg in consumer:
        if msg.value.decode('utf-8')==singal_msg:
            break
        f.write(msg.value.decode('utf-8')+'\n')