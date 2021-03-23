import pandas as pd
import sqlite3
import threading

class DataProcessor:
    def __init__(self, db_name='defaultDB.sqlite3'):
        self.db_name = db_name

        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            
            cur.execute("CREATE TABLE IF NOT EXISTS products (name, sku, description)")
            cur.execute("CREATE INDEX IF NOT EXISTS sku_idx ON products(sku)")
            
            cur.execute("SELECT COUNT(1) FROM products")
            print('Connected to {name} with {records} records'.format(name=self.db_name, records=cur.fetchone()[0]))
    
    def get_record_count(self):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT COUNT(1) FROM products")
            print('Products table has {records} records'.format(records=cur.fetchone()[0]))
    
    def load_data(self, path_to_file, chunksize=100000, block=False):
        
        def write_to_db(df):
            with sqlite3.connect(self.db_name, timeout=40) as db:
                df.to_sql("products", db, if_exists="append", index=False)
        
        threads = []
        
        # read csv file in chunks and assign to threads for db write
        for df in pd.read_csv(path_to_file, chunksize=chunksize):
            thread = threading.Thread(target=write_to_db, args=[df])
            thread.start()
            threads.append(thread)

        # TO-DO: read about join
        if block:
            for thread in threads:
                thread.join()
            print('All tasks are done.')
        else:
            print('Tasks have been scheduled.')
    
    def update_products_by_sku(self, sku_key, record, all_occurances=False):
        assert type(record) == tuple, 'records should be a tuple'
        
        query = """
                UPDATE products
                SET name=(?), sku=(?), description=(?)
                WHERE sku = (?)
                """
        with sqlite3.connect(self.db_name) as db:
            num_records = db.execute("SELECT COUNT(1) FROM products WHERE sku = (?)", [sku_key]).fetchone()[0]
            
            if num_records==1 or all_occurances==True:
                db.execute(query, (record[0], record[1], record[2], sku_key))
                print('Total changes:', db.total_changes)
            else:
                print('Key Conflict: This sku has {0} records. Set all_occurances=True or use update_products_by_rowid method'.format(num_records))

    def get_records_by_sku(self, sku_list):
        assert type(sku_list) == list, 'Input should be a list'
        
        sku_values = str(tuple([key for key in sku_list])).replace(',)', ')')
        query = "SELECT rowid, * FROM products WHERE sku IN ({0})".format(sku_values)
        # print(query)
        
        with sqlite3.connect(self.db_name) as db:
            # return db.execute(query).fetchall()
            return pd.read_sql(query, db).values
    
    def update_products_by_rowid(self, records):
        # assert type(records) == list and type(records[0]) == tuple, 'records should be a list of tuples'

        query = """
                UPDATE products
                SET name=(?), sku=(?), description=(?)
                WHERE rowid=(?)
                """
        def row_generator():
            for row in records:
                yield (row[1], row[2], row[3], row[0])
        
        with sqlite3.connect(self.db_name) as db:
            db.executemany(query, row_generator())
            print('Total changes:', db.total_changes)
    
    def get_aggregate_table(self, LIMIT=-1):
        query = """
                SELECT name, COUNT(1) as 'no. of products'
                FROM products
                GROUP BY name
                LIMIT {0}""".format(LIMIT)
        with sqlite3.connect(self.db_name) as db:
            return pd.read_sql(query, db)