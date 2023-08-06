import requests
import os
import sys
import json
import time
from urllib.request import urlretrieve
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

class Convert:
    def __init__(self):
        pass

    def bar_custom(self, current, total, width=80):
        print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))
        
    def local_file(self, api_key: str, file: str, output_format: str, input="upload", verbose=False):
        if not verbose:
            sys.stdout = open(os.devnull, "w")
        if os.path.exists(file) == True:
            payload = json.dumps({"apikey": api_key, "input": input, "file": file, "outputformat": output_format})
            print("Starting conversion...")
            start_conversion = requests.post("http://api.convertio.co/convert", data=payload)
            if json.loads(start_conversion.text)['status'] == 'error':
                sys.stdout = sys.__stdout__
                print("Error: " + json.loads(start_conversion.text)['error'])
            else:
                conversion_id = json.loads(start_conversion.text)['data']['id']
                print("Uploading file...")
                convert_url = "https://api.convertio.co/convert/" + conversion_id + "/" + file
                file_to_send = open(file, "rb")
                send_file = requests.put(convert_url, data=file_to_send)
                if json.loads(send_file.text)['status'] == 'error':
                    sys.stdout = sys.__stdout__
                    print("Error: " + json.loads(send_file.text)['error'])
                else:
                    print("File uploaded.")
                    time.sleep(1.2)
                    print("Waiting for conversion to finish...")
                    status_url = "https://api.convertio.co/convert/"+ conversion_id + "/status"
                    file_status = requests.get(status_url)
                    if json.loads(file_status.text)['status'] == 'error':
                        sys.stdout = sys.__stdout__
                        print("Error: " + json.loads(file_status.text)['error'])
                    else:
                        while json.loads(file_status.text)['data']['step'] != 'finish':
                            file_status = requests.get(status_url)
                        save_url = json.loads(file_status.text)['data']['output']['url']
                        sys.stdout = sys.__stdout__
                        print("Downloading converted file...")
                        last_ocurrence = save_url.rfind("/") + 1
                        new_file_name = "converted-" + save_url[last_ocurrence:]
                        with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=save_url.split('/')[-1]) as t:
                            urlretrieve(save_url, filename=new_file_name.lower(), reporthook=t.update_to)
        else:
            print("File not found.")