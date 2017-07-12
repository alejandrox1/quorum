import datetime
import collections
import urllib.request
from urllib.parse import urlparse
import spacy
nlp = spacy.load('en') 

### DATETIME
def date_flag(dateTime):                                                        
    today = datetime.datetime.today()                                           
    yesterday = today - datetime.timedelta(days=1)                              
    if dateTime.date()==today.date():                                           
        return 'today'                                                          
    elif dateTime.date()==yesterday.date():                                     
        return 'yesterday'                                                      
    else:                                                                       
        return 'old'

### URLS
def get_url_mainsite(url):
    """ Get the domain for a url.
    
        Example:
            url = 'http://bit.ly/silly'
            returns 'www.google.com'
    """
    response = urllib.request.urlopen(url)
    return response.url.split('/')[2]


def get_url_domain(url):                                                        
    pieces = urlparse(url).hostname.split('.')                                  
                                                                                
    if pieces[0]!='www':                                                        
        return pieces[0]                                                        
    else:                                                                       
        return pieces[1]

### GENERAL PROCESSING
def list_of_dicts_to_dict(dictionary):                                          
    new_dict = {}                                                               
    key_name = 'entities'                                                       
    counter=1                                                                   
    for item in dictionary:                                                     
        name = key_name+str(counter)                                            
        new_dict[name] = item                                                   
        counter+=1                                                              
    return new_dict  


def flatten_dict(d, parent_key='', sep='__'):                                        
    items = []                                                                  
    for k, v in d.items(): 
        new_key = parent_key + sep + k if parent_key else k                     
        if isinstance(v, collections.MutableMapping):                           
            items.extend(flatten_dict(v, new_key, sep=sep).items())                 
        else:                                                                   
            items.append((new_key, v))                                          
    return dict(items)


### BASIC NLP
def twitter_word_test(word):                                                    
    skip_words = ['RT','#','amp', '&amp']                                               
    skip_starts = ['#', '@']                                                    
    if word in skip_words:                                                      
        return False                                                            
    if any([word.startswith(t) for t in skip_starts]):                          
        return False                                                            
    return True

def get_nouns(tweet_text):                                                      
    nouns = []                                                                  
    doc = nlp(tweet_text)                                                       
    for word in doc:                                                            
        if word.tag_ in ['NNP','NN'] and twitter_word_test(word.text):          
            nouns.append(word.text)                                             
    return nouns
