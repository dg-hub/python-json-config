# python-json-config
Any simple module for storing configuration parameters in JSON


## Generate a Key
Generate a new symetric encryption key (used to secure passwords)

    1. `python .\generate_key.py`
    2. `y` -  Generate new key
    3. `y` -  Update Global Config
```
Do you wish to generate new key? (y/n): y
07/14/2020 09:11:35 AM INFO: New Key File: "enc_20200714091135.key"
Update Global Config with new filename? (y/n): y
07/14/2020 09:11:36 AM INFO: config/config.json imported
07/14/2020 09:11:36 AM INFO: config/config.json encryption_key_path retrieved internally from key-path.
07/14/2020 09:11:36 AM INFO: set_value("key-path","config/enc_20200714091135.key")
07/14/2020 09:11:36 AM INFO: Global Config updated
```
