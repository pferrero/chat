# Demo chat application

Chat application built using Flask.

## Usage
Install the virtual environment with:
```
pip install -r requirements.txt
```

Activate the envorinment:
```
bash: source venv/bin/activate
fish: source venv/bin/activate.fish
```

Create the database, this will create the .db file
with the tables and relations:
```
(venv)$ flask db upgrade
```

(optional) Fill the database with some users and
messages:
```
(venv)$ python populate_db.py
```

Run the application:
```
flask run
```