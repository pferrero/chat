# Demo chat application

Chat application built using Flask.

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