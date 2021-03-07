import base64
import logging
import os
from datetime import datetime
import argparse
import config

def ui_confirm(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def generate_key():
    if ui_confirm("Do you wish to generate new key?"):
        enc_key = base64.urlsafe_b64encode(os.urandom(32))
        filename = "enc_{}.key".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        with open('config/{}'.format(filename),'w') as outfile:
            outfile.write(enc_key.decode("utf-8"))
        logging.info('New Key File: "{}"'.format(filename))
        return filename
    else: 
        logging.info('User canceled operation')
        raise Exception("User canceled operation")

def update_config(key_filename):
    if ui_confirm("Update Global Config with new filename?"):
        config_global = config.config_file("config/config.json")
        config_global.set_value("key-path", "config/" + key_filename)
        config_global.write_config()
        logging.info('Global Config updated')
        return True
    else: 
        logging.info('User canceled operation')
        return False

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
parser = argparse.ArgumentParser(description='Generate new Symetric Encyrption key file')
args = parser.parse_args()

try:
    key_filename = generate_key()
    update_config(key_filename)
except Exception as e:
    pass

    
