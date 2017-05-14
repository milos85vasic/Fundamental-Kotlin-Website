# Fundamental Kotlin Website
Fundamental Kotlin Website version 1.8

## Configuring project
To run website it is needed to create configuration_parameters.py file in website directory.
Configuration must contain the following:
```python
from pyga.requests import Tracker

salt = "Your captcha salt"
smtp_password = 'Smtp password'
contact_email = 'contact@example.com'
tracker = Tracker('UA-XXXXXXX-X', 'example.com')
```

## Running project example
- cd 'directory containing website'
- sudo pip install -e .
- pserve development.ini