import os
import json
from time import sleep
import requests
import traceback
from bs4 import BeautifulSoup                                                   
from selenium.common.exceptions import WebDriverException, TimeoutException
from quorum.producers.SeleniumProducer import SeleniumProducers
from quorum.utils.file_utils import create_dir, safe_filename, process_files


class DataDotWorldOD(SeleniumProducers):
    """ data.world Scraper

        Crawls through the opendata portal which contains multiple catalogs.
        Each catalog contains multiple datasets.

    """
    opendataCatalogs = [
        'https://data.world/opendata/data.cityofnewyork.us',
        'https://data.world/opendata/data.austintexas.gov',
        'https://data.world/opendata/data.cityofchicago.org',
        'https://data.world/opendata/brigades.opendatanetwork.com',
        'https://data.world/opendata/data.gov',
        'https://data.world/opendata/data.acgov.org',
        'https://data.world/opendata/data.chattlibrary.org',
        'https://data.world/opendata/data.illinois.gov',
        'https://data.world/opendata/data.lacity.org',
        'https://data.world/opendata/data.lacounty.gov',
        'https://data.world/opendata/data.livewellsd.org',
        'https://data.world/opendata/data.oaklandnet.com',
        'https://data.world/opendata/data.ohouston.org',
        'https://data.world/opendata/data.results.wa.gov' 
    ]

    def __init__(self, virtuald=True, driver='firefox', max_datasets=-1, 
                 data_dir='data', upload_freq=3, **kwargs):
        super().__init__(virtuald, driver)
        self.url                = 'https://data.world'
        self.portal             = '/opendata'
        self.max_datasets       = max_datasets
        self.data_dir           = data_dir
        self.virtuald           = virtuald
        self.formats            = kwargs["formats"]
        self.upload_freq        = upload_freq
        self._kwargs            = kwargs

    def get_opendata(self):
        self.start_driver()
        create_dir([self.url], self.data_dir)
        self.driver.get(self.url + self.portal)

    def grab_opendata_catalogs(self):
        self.get_opendata()
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        catalogs = soup.find_all('a',
                                 class_="DSICatalogsListView__catalogCard___30giA",
                                 href=True)
        self.catalogs = [self.url+x.attrs["href"] for x in catalogs]


    def parse_catalog(self, catalog):
        path = create_dir([self.url, catalog], self.data_dir)
        self.counter = 0

        # lgo and checkpoint files
        checkpoints = {}
        if os.path.isfile(self.data_dir+'/checkpoints.json'):                                            
            with open(self.data_dir+'/checkpoints.json', 'r') as f:                                      
                checkpoints = json.load(f)
        log_file = open(path+'/log_file.txt', 'w')
        checkpoint_filename = path+'/checkpoints_file.txt'
        checkpoint_file, checkpoint = self.restart_crawl(checkpoint_filename)
        if checkpoint:
            checkpoints[str(catalog)] = str(checkpoint[-1])
        main_page = checkpoints.get(str(catalog), catalog)

        while self.counter <= self.max_datasets or self.max_datasets<0:
            try:
                print('\t{}'.format(main_page))
        
                self.driver.get(main_page)
                self._parse_catalog(path)
                
                # go to next page
                checkpoints[str(catalog)] = str(main_page)
                self.driver.get(main_page)
                sleep(2)
                self.driver.find_element_by_xpath('//*[@aria-label="Next"]').click()   
                prev_page = main_page
                main_page = self.driver.current_url
                if main_page==prev_page:
                    break
            except WebDriverException as e:
                print(e)
                log_file.write('{}\n'.format(e))
                traceback.print_tb(e.__traceback__)
                break
            except TimeoutException:
                print("bro... there was a timeout!")
                sleep(60*5)
                continue
            except Exception as e:
                print(e)
                log_file.write('{}\n'.format(e))
                traceback.print_tb(e.__traceback__)
                sleep(60*5)
                break
        
        with open(self.data_dir+'/checkpoints.json', 'w') as f: 
            json.dump(checkpoints, f)
        log_file.close()
        checkpoint_file.close()
        return path
   
    
    def _parse_catalog(self, path):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        datasets = soup.find_all('a', class_="dw-dataset-name",href=True)
        datasets = [self.url+x.attrs["href"] for x in datasets] 
        for dataset in datasets:
            if self.counter <= self.max_datasets or self.max_datasets<0:
                self.driver.get(dataset)
                sleep(1)
                dataset_link, dataset_name = self._get_datasets()
                self._save_datasets(path, dataset_link, dataset_name)
            else:
                break
            # Store files
            if self.counter%self.upload_freq==0:
                process_files(path, **self._kwargs)
        process_files(path, **self._kwargs)



    def _get_datasets(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        info = self._find_all_keyword(soup, 'a', "dw-dataset", href=True)
        if info:
            author, dataset_name = info[0], info[1]
            dataset_name = dataset_name.contents[0]
        else:
            dataset_name = self.driver.current_url.split('/')[-1]
        #description = soup.find_all('span',class_="Markdown__content___3thyu")
        dataset_link = soup.find_all('a', target="_blank", href=True)
        dataset_link = [d for d in dataset_link 
                        if "data-reactid" not in d.attrs.keys()]
        return dataset_link, dataset_name

    def _save_datasets(self, path, links, dataset_name):
        for link in links:
            file_ext = (link.contents[0]).split('.')[-1]
            if file_ext.upper() in self.formats:
                try:
                    r = requests.get(link.attrs["href"], stream=True)
                    filename = dataset_name + '.' + file_ext
                    filename = safe_filename(filename)
                    with open(path+'/'+filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    self.counter += 1
                except Exception as e:
                    print(e)
                    continue



    @staticmethod
    def _find_all_keyword(soup, tag, keyword, href=True):                                  
        elements = [                                                                
            x for x in soup.find_all(tag, href=href)                                
            if ("class" in x.attrs) and (keyword in str(x.attrs["class"]))          
        ]                                                                           
        return elements                                                             

if __name__=="__main__":
    crawler = DataDotWorldOD()
    crawler.grab_opendata_catalogs()
    for catalog in crawler.catalogs:
        instance_dir = crawler.parse_catalog(catalog)
    crawler.terminate_driver()