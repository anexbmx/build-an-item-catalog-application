# Build an Item Catalog Application

develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
# PreRequisites:
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)
  * [Google+ ID](https://accounts.google.com/)

# Run Project:


1. Install Vagrant and VirtualBox  [Details](https://www.udacity.com/wiki/ud088/vagrant).
2. create account &  create client ID [Google+](https://accounts.google.com/)
3. Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
4. Launch the Vagrant VM in the directory fullstack/vagrant from the terminal
```
 vagrant up
 ```
tou can find all steps  [here](https://www.udacity.com/wiki/ud088/vagrant).
5. Clone [this repository](https://github.com/anexbmx/build-an-item-catalog-application) to your `/vagrant` folder.

# setup  database

1. Run `databaseSetup.py` from the application folder.

```
    $ python3 databaseSetup.py
```

2. Run `catalogAppData.py`  testdata will be loaded to the our database

```
    $ python3 catalogAppData.py
```


 Run `application.py` to start the web application.
```
    $ python3 application.py
```

8. Open a browser and type  [localhost:8000](http://localhost:8000/).