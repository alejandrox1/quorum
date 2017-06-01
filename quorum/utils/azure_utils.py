from os import listdir                                                          
from os.path import isfile, join 
from azure.datalake.store import core, lib, multithread

def get_adl_client(store_name, client_id=None, client_secret=None, tenant_id=None):
    if not client_id or not client_secret or not tenant_id:
        try:
            from ..config.config import ADL_CLIENT_ID, ADL_CLIENT_SECRET, TENANT_ID
            tenant_id = tenant_id or TENANT_ID
            client_id = client_id or ADL_CLIENT_ID
            client_secret = client_secret or ADL_CLIENT_SECRET
        except:
            raise Exception('Pass client_id, client_secret, and tenant_id or define in config.py')

    token = lib.auth(tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret)
    
    return core.AzureDLFileSystem(token, store_name=store_name)


def put_dir(client, local_dir_path, destination_dir):                           
    files = [f for f in listdir(local_dir_path) if isfile(join(local_dir_path, f))]
                                                                                
    for f in files:                                                             
        client.put(join(local_dir_path, f), join(destination_dir, f))
