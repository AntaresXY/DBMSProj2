import json
import pymysql
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)
            
            book_info_json = json.loads(book_json_str)
            title = book_info_json.get("title")
            tags = book_info_json.get("tags")
            
            if tags is not None:
                tags = ",".join(tags)
            author = book_info_json.get("author")
            book_intro = book_info_json.get("book_intro")
            price = book_info_json.get("price")
            self.cursor = self.conn.cursor()
            
            self.cursor.execute(
                "INSERT into store(store_id, book_id, title, price, tags, author, book_intro, stock_level)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (store_id, book_id, title, price, tags, author, book_intro, stock_level)
            )
            
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)
            
            self.cursor = self.conn.cursor()            

            self.cursor.execute(
                "UPDATE store SET stock_level = stock_level + %s "
                "WHERE store_id = %s AND book_id = %s",
                (add_stock_level, store_id, book_id),
            )
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            self.cursor = self.conn.cursor()   
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            self.cursor.execute(
                "INSERT into user_store(store_id, user_id)" 
                "VALUES (%s, %s)",
                (store_id, user_id),
            )
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
       
    # def deliver_order(self, order_id: str) -> (int, str):
    #     try:
    #         self.cursor = self.conn.cursor()
    #         self.cursor.execute(
    #             "SELECT status FROM new_order"
    #             "WHERE order_id = %s and status < 3;",
    #             (order_id, )
    #         )
    #         row = self.cursor.fetchone()

    #         if row is None:
    #             return error.error_invalid_order_id(order_id)
            
    #         status = row[0]

    #         if status == -1:
    #             return error.error_invalid_order_id(order_id)
    #         elif status == 0:
    #             return error.error_order_not_paid(order_id)
    #         elif status == 2:
    #             return error.error_order_delivered(order_id)
            
    #         self.cursor.execute(
    #             "UPDATE new_order set status = %s"
    #             "WHERE order_id = %s;",
    #             (2, order_id)
    #         )
    #         self.conn.commit()
    #     except pymysql.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         return 530, "{}".format(str(e))
    #     return 200, "ok"
    