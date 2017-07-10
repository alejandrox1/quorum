import sys
import json
import dataset
from time import sleep
from kafka import KafkaProducer, KafkaConsumer
import praw
from config import REDDIT



def format_submission(submission):                                                        
    formatedSub = {                                                           
        'id': submission.id,                                                  
        'created_at': submission.created,                                      
        'author': submission.author,                                 
        'text': submission.title,                                                  
        'urls': submission.permalink,                            
    }                                                                           
    return formatedSub 


def authenticate_api():
    reddit = praw.Reddit(client_id=REDDIT['CLIENT_ID'],
                         client_secret=REDDIT['CLIENT_SECRET'],
                         user_agent=REDDIT['USER_AGENT'])
    return reddit


def get_reddit_submissions(subreddit):
    # Connect to DB
    db = dataset.connect('postgresql://user:pass@redditdb/myredb')
    table = db['subreddits']
    # Connect to Kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    # Reddit API
    reddit = authenticate_api()

    submissions = 0
    need_update = True
    lastUpdated = table.find_one(subreddit=subreddit)
    for submission in subreddit.new():
        if submissions > 1000:
            break
        if lastUpdated.get('username')==submission.author and lastUpdated.get('since_id')==submission.id:
            break
        
        msg = producer.send('data', json.dumps(format_submission(submission)).encode('utf-8'))
        submissions += 1

        if need_update: 
            record = {
                'username': submission.author,
                'since_id': submission.id,
            }
            with dataset.connect('postgresql://user:pass@redditdb/myredb') as tx:
                tx['user'].upsert(record, record['username'])

        if submissions%100 == 0:
            print(submissions)
            break
    # Flush kafka producer                                                  
    producer.flush()                                                        
    
    return subreddit


if __name__=="__main__":
    sleep(10)
    if len(sys.argv)>1:
        get_reddit_submissions(sys.argv[1])
    else:
        consumer = KafkaConsumer('twitterUser', bootstrap_servers=['kafka:9092'])
        for msg in consumer:
            with open('test.txt', 'a') as f:
                f.write(msg.value.decode('utf-8')+'\n')
            get_reddit_submissions(msg.value.decode('utf-8'))
