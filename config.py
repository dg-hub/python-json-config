import logging
import json
import base64
from cryptography.fernet import Fernet
class config_file:

    def __init__(self, filename="config.json", encryption_key_path=None):
        self.values = None
        self.filename = filename
        self.encryption_key_path = encryption_key_path
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
        try:
            with open('{}'.format(filename)) as json_data_file:
                self.values = json.load(json_data_file)
            logging.info('{} imported'.format(filename))
            if encryption_key_path is None:
                try:
                    self.encryption_key_path = self.get_value("key-path")
                    logging.info('{} encryption_key_path retrieved internally from key-path.'.format(filename))
                except KeyError as e: 
                    logging.warning('{} encryption_key_path undefined.'.format(filename))
        except FileNotFoundError as e:
            logging.error('Config File Not found - FileNotFoundError {}'.format(filename))
            raise e
        

    def exists(self, key):
        if key in self.values:
            return True
        else:
            return False

    def get_value(self,key):
        try:
            return self.values[key]
        except KeyError as e:
            logging.warning('Configuration value not found: "{}"'.format(key))
            raise e

    def get_config(self):
        v = self.values.copy()
        v["db-password"] = self.get_password()
        return v

    def set_value(self,key, value):
        self.values[key] = value
        logging.info('set_value("{}","{}")'.format(key,value))

    def __get_key(self):
        if self.encryption_key_path is None:
            logging.error("config.__get_key() failed key-path undefined")
            raise Exception("key-path undefined")
        file = open(self.encryption_key_path, 'rb')
        key = file.read() # The key will be type bytes
        file.close()
        return key

    def write_config(self):
        js_config = json.dumps(self.values, sort_keys=True, indent=4, default=str)
        with open('{}'.format(self.filename),'w') as outfile:
            outfile.write(js_config)

    def get_password(self,key_name="db-password"):
        key = self.__get_key()
        f = Fernet(key)
        encrypted = str.encode(self.get_value(key_name))
        decrypted = f.decrypt(encrypted)
        return decrypted.decode()

    def set_password(self, password,key_name="db-password"):
        key = self.__get_key()
        f = Fernet(key)
        encrypted = f.encrypt(str.encode(password))
        #set_value("password-plain",password)
        self.set_value(key_name,encrypted.decode())
        self.write_config()

