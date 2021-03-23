# file_processor
Assignment for Interview. Solution basd on Python + SQLite.

---
## Docker

### Build docker image
> `$ docker build -t lfp .`

### Run repo in docker container
> `$ docker run -it --rm -v PATH_TO_DIR:/app lfp`

---
## Schema
There is only one table called 'products' with 3 fields for imported data and a default 'rowid' column created by SQLite.

* Schema: products (name, sku, description)
* SQL: "CREATE TABLE IF NOT EXISTS products (name, sku, description)"

An index named 'sku_idx' is created to make querying efficient.

* SQL: CREATE INDEX sku_idx ON products(sku)

---
## Data

---
## Deliverables

1. Steps to run your code. As less steps we are to run, better for you (Hint: Docker)

    See Docker section above

2. Details of all the tables and their schema, [with commands to recreate them]

    See Schema section above

3. What is done from “Points to achieve” and number of entries in all your tables with sample 10 rows from each.

    I think I have covered all points. See the Data section above.

4. What is not done from “Points to achieve”. If not achieved write the possible reasons and current workarounds.

    I think I have covered all points.

5. What would you improve if given more days

    Error handling and documentation.
