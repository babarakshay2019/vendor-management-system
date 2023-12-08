# Installation #

Follow these steps to get the application running in your local/test environment:

## Requirements ##
* Python 3.6 and above
* PostgreSQL and above (Install `postgresql-contrib` and `pgadmin4` alongside)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

## db setup ##
```
* Create db and db user and provide your credentials in .env file 
```

## python packages ##
```
mkvirtualenv web
pip install -r requirements.txt
```

## commands for create db tables and runserver ##
```
./manage.py makemigrations
./manage.py migrate
./manage.py runserver 
```

## for run test cases ##
```
./pytest tests
```

## API document link ##
```
http://127.0.0.1:8000/api/swagger/
```



