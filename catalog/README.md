# Item Catalog
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About
Learn the CRUD pattern (Create, Read, Update, Delete) and how it relates to RESTful architectures and to the operations of a database-backed web service. Learn the difference between authentication and authorization and some best practices in developing a login system.

## In This Repo
This project has one main Python module `app.py` which runs a Flask application. A SQL database is created using the `database_setup.py` module.



## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd/vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run sudo pip install requests
7. Setup application database `python /item-catalog/database_setup.py`
8. *Insert fake data `python /item-catalog/database_init.py`
9. Run application using `python /item-catalog/app.py`
10. Access the application locally using http://localhost:5010

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Item-Catalog'
7. Authorized JavaScript origins = 'http://localhost:5010'
8. Authorized redirect URIs = 'http://localhost:5010/login' && 'http://localhost:5010/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in item-catalog directory that you cloned from here
14. Run application using `python /item-catalog/app.py`

## JSON Endpoints
The following are open to the public:


Categories JSON: `/catalog/categories/JSON`
    - Displays all categories

Category Items JSON: `/catalog/<path:category_name>/items/JSON`
    - Displays items for a specific category

