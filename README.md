# Ticketock : MAD2 Project
Name: Natasha Mittal

Roll no.: 21f1005823

This is my submission for the final project for the course Modern Application Development II

May term, 2023

# Project setup
How to use
NOTE - I did not copy the node_modules folder in this repository. If you decide to clone the repo and intent to use it, you need to create an empty Vue3.0 project using CLI. Copy the node modules folder into the root directory of my repo.

Before we could use the web app, we need to setup the environment and servers for it.

# Setting up the Flask server :

From the root folder, simply run the command

    python main.py
# Setting up Redis server :

in a new terminal tab, start the redis server bY command 

   redis-server
# Setting up mailhog :

in a new terminal tab, start the Mail-Hog server by typing

    mailhog
# Setting up Celery Worker and Celery Beat :

in a new terminal tab, start the Celery Workers by typing

   Celery --app main.celery_inst worker --loglevel=info
   
   Celery --app main.celery_inst beat --loglevel=info
