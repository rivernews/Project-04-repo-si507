# Project-04-repo-si507

## Which project option you chose
Option 1

## What your name is
Shaung Cheng

## What your project does, concisely
This python program scraps information of all sites on the National Park Service website and store them in database.

## How to run your project

### To install the project:

1. Git clone this project.
1. Make a virtual environment in the project root folder, **and activate it**.
1. `pip install -r requirements.txt` to install all dependencies.

### To run the project:

1. `python SI507_project4.py`, make sure you use Python 3.6+.

The repo already contains a database `my-database.sqlite` of all sites finished scrapping. 

If you run the program right after you clone this project, the program won't make any request since the program checks if data is already in database (caching). 

For demo purpose, you can delete `my-database.sqlite` w/o concerns and run the program. The program will start scrapping the website and store in database. The program also prints percentage information, so you can see the progress.

## Highlights

- A light ORM implemented by raw SQL.

The ORM can do `count`, `filter`, `update`, `create` and initial schema creation, and is largely used in the scrapper for storing and caching purpose. The `DatabaseManager` in `database.py` implements these methods. The final CSV is exported by using the sql command:

```sql
select Sites.Name, Sites.Description, Sites.Location, Sites.Type, States.Name AS `State` from Sites join States on Sites.StateID = States.id;
```

- Using `Selenium` for scrapping.

[Selenium](https://selenium-python.readthedocs.io/locating-elements.html) is originally intended for UI testing, but it can do web scrapping as well. I implemented a `Browser` class in `browser.py` to provide a convenient interface for my python program to access elements and values on the web page.

- OOP

A scrapper class `NationalParkWebCrawler` instance in `SI507_project4.py` mainly do the scrapping and data storing job, while using the `Browser` class and `DatabaseManager` instance to perform higher-level operations.

### Database schema
![database schema](db-schema.png)



# Reference 

- [Proj instr goo doc](https://docs.google.com/document/d/12ysom92FnaIamL38yiYrno7alWyCoRIStK-ME8ORD3Q/edit#)
- [Tool for designing database schema](https://app.quickdatabasediagrams.com/#/d/oo35Ob)

## Dev notes

### Project overall flow:

Do it once

1. [x] (get/navigate to home page)
1. [x] get state index urls
1. [x] get state abbrv
1. [x] store urls & abbrv in db

Loop (plus caching to avoid duplication)

1. (get/navigate to state page)
1. get site element
1. try to get each value
1. store data in db