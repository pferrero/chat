# Chat demo application

Chat application built using Flask.

## Screenshot
![screenshot1](https://user-images.githubusercontent.com/39303220/125351969-1d58d700-e337-11eb-992e-1d1d0dcfba95.png)

## Usage
Set up the virtual environment with:
```
$ virtualenv venv
```

Activate the virtual envorinment:
```
bash: source venv/bin/activate
fish: source venv/bin/activate.fish
```

Install the dependencies in the venv:
```
(venv)$ pip install -r requirements.txt
```


Create the database, this will create the .db file
with the tables and relations:
```
(venv)$ flask db upgrade
```

(optional) Fill the database with some users and
messages to test the application:
```
(venv)$ python populate_db.py
```

Run the application:
```
(venv)$ flask run
```

To deactivate the venv simply type:
```
(venv)$ deactivate
```
