
Gantt chart implementation in Django (using twproject for gantt chart)

# Features
* manage task statuses –> sort of workflow handling
* manage dependecies
* manage assignements (resources, roles, efforts,file upload)
* full undo-redo support

# Requirements
* Django==1.9
* djangorestframework==3.4.6

# How to clone?
git clone https://github.com/sayonetech/ganttchartapp.git

# Quick Start

Create a virtual ,see this http://docs.python-guide.org/en/latest/dev/virtualenvs/

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
