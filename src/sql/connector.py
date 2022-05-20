"""
The object used to do the sql stuff safety
"""

import mysql.connector
import src.constants as constants
import sys
import csv
import datetime
class connector:

	def __init__(self):
		"""
		create a mysql.connector base on constants.SQLCONFIG
		"""
		self.con = mysql.connector.connect(**constants.SQLCONFIG)
	
	def __del__(self):
		"""
		disconnect to the database
		"""
		self.con.close()


	def init_db(self):
		"""
		Iniitialize the database
		Create the table
		"""
		
		c = self.con.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS item_info (
			id SERIAL,
			itemid BIGINT UNSIGNED NOT NULL,
			shopid BIGINT UNSIGNED NOT NULL,
			catid BIGINT UNSIGNED NOT NULL,
			name TEXT NOT NULL,
			image TEXT,
			PRIMARY KEY(itemid)
			)""")


		self.con.commit()

		c.execute("""CREATE TABLE IF NOT EXISTS item_rating(
			itemid BIGINT UNSIGNED NOT NULL,
			shopid	BIGINT UNSIGNED NOT NULL,
			rating_count INT NOT NULL,
			rating1 INT,
			rating2 INT,
			rating3 INT,
			rating4 INT, 
			rating5 INT,
			rating_star DECIMAL,
			rcount_with_context INT,
			rcount_with_image INT,
			FOREIGN KEY(itemid) REFERENCES item_info(itemid) 
			)""")
		self.con.commit()

		c.execute("""CREATE TABLE IF NOT EXISTS comments(
			id SERIAL,
			rating_star INT,
			cmtid BIGINT UNSIGNED NOT NULL,
			author_username TEXT NOT NULL,
			author_shopid BIGINT UNSIGNED,
			comment TEXT,
			itemid BIGINT UNSIGNED NOT NULL,
			shopid BIGINT UNSIGNED NOT NULL,
			PRIMARY KEY(cmtid)
			)""")
		self.con.commit()

		c.close()

	def is_item_exists(self, item):
		"""
		return if the item is existed in table by cid
		"""
		c = self.con.cursor()
		sql = f"\
			SELECT itemid FROM item_info WHERE itemid = '{item.itemid}'\
			"
		c.execute(sql)
		if c.fetchone() == None:
			c.close()
			return False
		c.close()
		return True
	
	def is_comment_exists(self, comment):
		"""
		return if the comment is existed in table by cid
		"""
		exist = False
		c = self.con.cursor()
		sql = f"\
			SELECT cmtid FROM comments WHERE itemid = {comment.itemid}\
			"
		try:
			c.execute(sql)
			resultSet = c.fetchall()
			for comments in resultSet:
				if comments[0] == comment.cmtid:
					exist = True
					break
			
		except Exception as e:
			sys.stderr.write(str(e)+"\n")
			exist = False
		finally:
			c.close()
			return exist

	def insert_item(self, item):
		"""
		insert item into table
		"""
		success = False
		if not self.is_item_exists(item):
			c = self.con.cursor()
			name = item.name.replace("'", "''")

			sql = f"\
				INSERT INTO item_info\
				(itemid, shopid, catid, name, image)\
				VALUES\
				({item.itemid}, {item.shopid}, {item.catid}, '{name}', '{item.images[0]}')\
				"
			item_rating = item.item_rating
			sql2 = f"\
				INSERT INTO item_rating\
				(itemid, shopid, rating_count, rating1, rating2, rating3, rating4, rating5, rating_star ,rcount_with_context ,rcount_with_image)\
				VALUES\
				({item.itemid}, {item.shopid}, {item_rating.rating_count}, {item_rating.rating1}, {item_rating.rating2}, {item_rating.rating3}, {item_rating.rating4}, {item_rating.rating5}, {item_rating.rating_star}, {item_rating.rcount_with_context}, {item_rating.rcount_with_image})\
				"
			try:
				c.execute(sql)
				c.execute(sql2)
				success = True
			except Exception as e:
				sys.stderr.write(str(e)+"\n")
				success = False
			finally:
				self.con.commit()
				c.close()
				return success
		return False

	def insert_comment(self, comment):
		"""
		insert comment into table
		"""
		success = False
		if not self.is_comment_exists(comment):
			c = self.con.cursor()
			text = comment.comment
			author_username = comment.author_username

			if comment.comment != None:
				text = comment.comment.replace("'", "''")
			if comment.author_username != None:
				author_username = comment.author_username.replace("'", "''")
			if text == None:
				text = 'NULL'
			if author_username == None:
				author_username = 'NULL'
				comment.author_shopid = 'NULL'
			sql = f"\
				INSERT INTO comments\
				(rating_star, cmtid, author_username, author_shopid, comment, itemid, shopid)\
				VALUES\
				({comment.rating_star}, {comment.cmtid}, '{author_username}', {comment.author_shopid}, '{text}', {comment.itemid}, {comment.shopid})\
				"
			try:
				c.execute(sql)
				success = True
			except Exception as e:
				sys.stderr.write(str(e)+"\n")
				success = False
			finally:
				self.con.commit()
				c.close()
				return success
		return success