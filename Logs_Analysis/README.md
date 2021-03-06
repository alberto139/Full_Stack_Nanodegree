# Full Stack Nanodegree Project: Logs Analysis


## Introduction


The database in question is a newspaper company database where we have 3 tables; `articles`, `authors` and `log`.
* `articles` - Contains articles posted in the newspaper so far.
* `authors` - Contains list of authors who have published their articles.
* `log` - Stores log of every request sent to the newspaper server.



## Running

* Make sure you have `newsdata.sql`, the SQL script file with all the data. It can be downloaded from the Udacity course page.

* Then run the following command to execute it in `news` database. You might have to create the database before-hand.

```sh
psql -d news -f newsdata.sql
```

* Finally run the script.

```sh
python2 solution.py
```

* It will present you with necessary stats.

----
