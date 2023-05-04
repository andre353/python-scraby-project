# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from sqlalchemy import create_engine, text, inspect


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'product_description':
                value = adapter.get(field_name)
              # print("*****")
              # print(value)
                adapter[field_name] = value[0].strip()
        
        # Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)
      
        # Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        # Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        if stars_text_value == "one":
            adapter['stars'] = 1
        if stars_text_value == "two":
            adapter['stars'] = 2
        if stars_text_value == "three":
            adapter['stars'] = 3
        if stars_text_value == "four":
            adapter['stars'] = 4
        if stars_text_value == "five":
            adapter['stars'] = 5
      
        return item


class SaveToMySQLPipeline:
    def __init__(self, table_name=''):
      # Getting, but not using currently
        self.table_name = table_name
        db_connection_string = f"mysql+pymysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}?charset=utf8mb4"
      
        self.conn = create_engine(
          db_connection_string,
          connect_args={
            "ssl": {
              "ssl_ca": "/etc/ssl/cert.pem"
            }
          }
        )

        with self.conn.connect() as conn:
            # Do not substitute user-supplied database names here.
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS books(
                id int NOT NULL auto_increment, 
                url VARCHAR(255),
                title text,
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                product_description text,
                PRIMARY KEY (id))  
            """))

    def process_item(self, item, spider):
      
      
        with self.conn.connect() as conn:
            # insp = inspect(self.conn)
            # table_name
            ## Define insert statement
            # conn.execute(text(insert_str))
            conn.execute(self.table_name.insert(), {
              "url": item['url'],
              "title": item['title'],
              "upc": item['upc'],
              "product_type": item['product_type'],
              "price_excl_tax": item['price_excl_tax'],
              "price_incl_tax": item['price_incl_tax'],
              "tax": item['tax'],
              "price": item['price'],
              "availability": item['availability'],
              "num_reviews": item['num_reviews'],
              "stars": item['stars'],
              "category": item['category'],
              "product_description": str(item['product_description'][0]),
            })
      
            # ## Execute insert of data into database
            conn.commit()
            return item
    
    def close_spider(self, spider):
        self.conn.dispose()