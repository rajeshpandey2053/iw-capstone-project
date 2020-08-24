pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations accounts
python manage.py makemigrations blog
python manage.py makemigrations posts
python manage.py migrate
python manage.py runserver