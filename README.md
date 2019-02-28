#Udacity  full-stack-web-developer-nanodegree--nd004

ITEM CATALOG-WEBAPP PRPJECT
By Sunkara Ramya
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About the Project:
This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit, and delete their own items.


## In This Project
This project has one main Python module `web_app.py` which runs the Flask application. A SQL database is created using the `DataBase_Items_init` module and you can populate the database with test data using `database_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills or tools Required
1. Python
2. HTML
3. CSS
4.Flask Framework
4. DataBaseModels
5.OAuth
6.DataBaseModels

## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install vagrant and virtualbox
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests

Or you can simply Install the dependency libraries (Flask, sqlalchemy, requests,psycopg2 and oauth2client) by running 
`pip install -r requirements.txt`

7. Setup application database `python /film_cam/Model_Data_Setup.py`
8. *Insert sample data `python /film_cam/DataBase_Items_init.py`
9. Run application using `python /film_cam/webapp.py`
10. Access the application locally using http://localhost:8000

*Optional step(s)

## For signin to Google Mail account
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Film Camera Hub'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in signin.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in film_cam directory that you cloned from here
14. Run application using `python /film_cam/webapp.py`

## JSON Endpoints
The following are open to the public:

Film_Camera Catalog JSON: `/CameraHub/JSON`
    - Displays the whole filmcamera  catalog.All cameras will be displayed.

 Categories JSON: `/film_camerastore/cameracategories/JSON`
    - Displays all Camera categories
All camera Models: `/film_camerastore/models/JSON`
	- Displays all Camera Models

Camera Model JSON: `/film_camerastore/<path:film_camera_name>/models/JSON`
    - Displays camera models for a specific camera category

Camera Category Model JSON: `/film_camerastore/<path:film_camera_name>/<path:model_name>/JSON`
    - Displays a specific Film_Camera category Model.

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
