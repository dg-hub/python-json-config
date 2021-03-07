import config
import logging
import argparse
import getpass 

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

parser = argparse.ArgumentParser(description='Set configuartion file password')


parser.add_argument('-c','--config', default='db-password', type=str)
parser.add_argument('-k','--keypath', type=str)
parser.add_argument('filename', action="store", type=str)

args = parser.parse_args()
if args.keypath is None:
    global_config = config.config_file("config/config.json")
    encryption_key_path = global_config.get_value("key-path")
else:
    encryption_key_path = args.keypath

try:
    c = config.config_file(args.filename,encryption_key_path)
    print("Update Password for {}".format(args.filename))
except KeyError as e:
    logging.error('Configuration file does not contain password')
    exit(9)
except FileNotFoundError:
    logging.error('File not found: "{}"'.format(args.filename))
    exit(9)

password  = getpass.getpass(prompt=' Enter password: ')
password2 = getpass.getpass(prompt='Repeat password: ')
if password == password2:
    try:
        c.set_password(password,args.config)
    except KeyError as e:
        logging.error('Configuration file does not contain password: "{}"'.format(key))
        raise e
else:
    logging.error('Password mismatch - Failed to update: "{}"'.format(args.filename))
    exit(9)
