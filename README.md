```
// clone this project

// go to the project directory
cd {project_dir}

// create a virtual env
py -m venv venv

// activate venv
"./venv/Scripts/activate.bat"

// install deps
pip install -r requirements.txt

// setup django
python manage.py makemigrations
python manage.py migrate

// create super user
python manage.py createsuperuser

// run server
python manage.py runserver

// login to the web app by using the created superuser
```
