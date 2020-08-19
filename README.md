## ProjectRoomate
Create a virtual environment

```
$ python -m venv ll_env
```
Once you are in the project first run the following command to be in a virtual enviroment

```
$ source ./venv/bin/activate
```
To get out of the virtual enviroment
```
$ deactivate
```
To start the server run

```
$ python manage.py runserver
```

Install the Environments 

```
$ pip install -r requirements.txt
```
Run Unit Tests
 1. Standard
  ```
  $ ./manage.py test
  ```
 2. Allow all print statements to be printed
  ```
  $ ./manage.py test --nocapture
  ```
 3. Verbose
  ```
  $ ./manage.py test --verbose
  ```
Run Aloe Tests
  ```
  $ aloe THEAPP/features/TESTCASE.feature
  ```
