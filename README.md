# Joe Store
Backend system for a simple e-commerce platform.

## Dependencies
* [pyenv](https://github.com/pyenv/pyenv)
* [poetry](https://python-poetry.org/)

## Running the project
1. Clone the repository
2. `cd joe-store`
3. Install Python 3.12 virtual environment via pyenv: `pyenv install 3.12`
4. Set the virtual environment on the project: `pyenv local 3.12`
5. Set Poetry to use the virtual environment: `poetry env use 3.12`
6. Install the packages needed to run the project: `poetry install`
7. `cd joestore/`
8. Run the migrations:
`poetry run python manage.py makemigrations && poetry run python manage.py migrate`
9. Create a superuser (admin): `poetry run python manage.py createsuperuser`
10. To run the server: `poetry run python manage.py runserver`
11. To run the tests: `poetry run python manage.py test store`

Admin dashboard can be accessed via `http://localhost:8000/admin`.\
The database can be accessed via command line shell using 
```bash
sqlite> sqlite3 db.sqlite3
```
In SQLite CLI, you can list all tables using `.tables`, SQL schemes can be seen
using 
```bash
sqlite> .schema [table name] --indent
```

# Overview
This project is a simple e-commerce app, with a basic front-end and back-end.
The users can register, log in, access the store, add items to the cart, modify
the number of items to be purchased, and make a purchase. Users also can see
their order history. Administrators can add, edit, or remove products via admin
dashboard.

## Development
Joe Store was written in Python, using [Django](https://www.djangoproject.com/)
for the back-end infrastructure. Django is a free open-source web framework
focused on clean and organized code. By default, Django uses SQLite as a
database and automatically handles the authentication, all entries related to
passwords are hashed. I chose Django as a framework for two reasons: first, it
is widely used and I saw this as an opportunity to learn more about the
framework, and second, thanks to its DRY principles, I could write a system
with clean and easy-to-understand code.

### Project structure
Inside `joestore` are two folders: `static` and `store`. The former is related
to static items, like CSS structures and images, and the latter is the store
app itself.

### Front-end
A minimal front-end was developed for ease of use. For login, register, order
history, and order detail pages all were written using basic HTML in addition
to Django forms to process data for sign-up or log-in a user. The home, cart,
and checkout pages use a basic [Bootstrap navbar](https://getbootstrap.com/)
for navigating between the pages. I used this opportunity to learn more about
front-end development, although this was not my main focus.

### Back-end
Inside the `store` app are two main folders: `templates` and `migrations`, the
former are HTML files for each store page and the latter are generated files by
Django after running the `makemigrations` command, which will map our classes
to tables in the database.

In `models.py` are all the classes we need to operate a storefront. Ideally,
this would be a folder, where each file corresponds to a specific class, but
this is a simple project, so I decided to keep it in one single file. There are
five classes in `models.py`: Customer, Product, Order, OrderItem, and
ShippingAddress. All this information is stored as tables in the database.

In `views.py`, the functions handle the data between the back and the front
ends. Thus, tasks related to registering a user (`register`), logging in
(`loginPage`), logging out (`logout`), rendering the store (`store`), creating
the cart (`cart`), checkout process, updating the cart (`updateItem`),
processing the order (`processOrder`) and rendering both order history and
order details pages. The last two mentioned tasks are only visible to logged-in
users.

### Tests
Basic unit tests evaluate the correctness of the store app.

## TODO
During the development, I noticed some aspects could be improved or added, but
due to time constraints, some went unfinished:
* **Guest accounts**: it is possible to see some pages without the need to log
  in, but it is not possible to add items to the cart.  It is possible to
  collect the cookies related to the activity of the guest user and save this
  information. After checkout, the guest user should log in or sign up to
  finish their order, this way, the app only needs to retrieve the information
  from the cookies after the guest logs in (currently, the cart contents are
  saved after the user logs out);
* **More tests**: It is preferable to develop using the TDD approach, even
  [Django developers recommend
  it](https://docs.djangoproject.com/en/5.1/intro/tutorial05/#basic-testing-strategies).
  However, I was adapting to the framework, and learning a bit more of the
  front end too, this made me question what tests I should do other than the
  basic ones (add user, add product, edit product, etc.). Now that I know how
  to organize and develop for Django, I have a better understanding of
  proceeding using the TDD approach.
