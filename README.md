# Item Catalog Web App

This project utilizes the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## In This Repo
This project has one main Python module `item_catalog.py` which runs the Flask application. A SQL database is created using the `database_setup.py` module and you can populate the database with test data using `inital_data.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. 
CSS/JS/Images files are stored in the static directory.

## How to Run?

### PreRequisites
  * [Python ~2.7](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Find the catalog folder and replace it with the content of this current repository, by either downloading or cloning it from
  [Here](https://github.com/rambo255/item_catalog).

### Launch Project
1. Launch the Vagrant VM (`vagrant up`)
2. Log into Vagrant VM (`vagrant ssh`)
3. Navigate to `cd/vagrant` as instructed in terminal
4. The app imports requests which is not on this vm. Run sudo pip install requests
5. Setup application database `python /item_catalog/database_setup.py`
6. *Insert fake data `python /item_catalog/initial_data.py`
7. Run application using `python /item_catalog/item_catalog.py`
8. Access the application locally using http://localhost:5000

## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/items/JSON`
    - Displays the whole items.

Categories JSON: `/catalog/categories/JSON`
    - Displays all categories

Category Items JSON: `/catalog/<int:category_id>/items/JSON`
    - Displays items for a specific category

Category Item JSON: `/catalog/<int:category_id>/items/<int:item_id>/JSON`
    - Displays a specific category item.
