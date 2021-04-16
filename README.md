# file_processor
Assignment for Interview. Solution based on Python + SQLite.

---
## Docker

Clone and change directory into it the repo.

* **Build docker image**
> `$ docker build -t lfp .`

* **Run repo in docker container**

The PATH_TO_DIR will be mounted as ./app and used as working directory in container.
> `$ docker run -it --rm -v PATH_TO_DIR:/app lfp`

* **Python shell**

After the above two steps, you should see a python shell with ./app as working direcory. Import the app and initializ with a name.

> `>>> from data_processor import DataProcessor`

> `>>> app = DataProcessor('test.db')`

* **Usage**

Note: [Google Colab](https://colab.research.google.com) is a free notebook server that can use data in your GDrive account.

---
## Schema
There is only one table called 'products' with 3 fields for imported data and a default 'rowid' column created by SQLite.

* Schema: products (name, sku, description)
* SQL: "CREATE TABLE IF NOT EXISTS products (name, sku, description)"

An index named 'sku_idx' is created to make querying efficient.

* SQL: CREATE INDEX sku_idx ON products(sku)


## Note
If you see Database is locked error, it is because of the lightweight nature of SQLite and using parallelism to update, which shouldn't be a problem when using a other DBs.
