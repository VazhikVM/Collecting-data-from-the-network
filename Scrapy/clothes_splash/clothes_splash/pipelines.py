# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ClothesSplashPipelineSQL:
    def open_spider(self, spader):
        self.connection = sqlite3.connect('clothe_db.db')
        self.cursor = self.connection.cursor()

        create_table = '''
        create table if not exists all_clothe(
            title varchar(500),
            img varchar(500),
            price varchar(20),
            desc text
        );
        '''

        self.cursor.execute(create_table)
        self.connection.commit()

    def process_item(self, item, spider):
        insert_query = '''
            insert into all_clothe(
            title, img, price, desc)
            values(?, ?, ?, ?);
        '''

        self.cursor.execute(insert_query, tuple(item.values()))
        self.connection.commit()
        return 'Good_insert'

    def close_spider(self, spider):
        self.connection.close()

