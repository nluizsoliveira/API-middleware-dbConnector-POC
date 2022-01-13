import mysql.connector
from mysql.connector import errorcode

# Responsible for providing a connector to the DB, 
# As well as basic functions to interact with the db,
# Such as logging, creating a table and inserting a row.
class DBConnector:
	def __init__(self, user, password, database):
		self.connection = self.get_connection(user, password, database)
		self.cursor = self.connection.cursor()
		self.connection.autocommit = True

	@staticmethod
	def get_connection(user, password, database):
		CREDENTIALS_ERROR =  errorcode.ER_ACCESS_DENIED_ERROR
		DATABASE_ERROR = errorcode.ER_BAD_DB_ERROR
		CREDENTIALS_ERROR_MSG = "DB ERROR: User and Password dont' match"
		DATABASE_ERROR_MSG = "DB ERROR: Database doesn't exist."
		try:
		  connection = mysql.connector.connect(
		  	user=user, 
		  	password=password, 
		  	database=database
		  )
		  return connection
		except mysql.connector.Error as err:
		  if err.errno == CREDENTIALS_ERROR:
		    print(CREDENTIALS_ERROR_MSG)
		  elif err.errno == DATABASE_ERROR:
		    print(DATABASE_ERROR_MSG)
		  else:
		    print(err)
		  quit(1)
		
	def upsert_table_and_row(self, table_name, create_table_query, insert_row_query):
		is_table_on_db = self.is_table_on_db(table_name)
		if is_table_on_db: 
			self.execute_query(insert_row_query)
		else:
			self.execute_query(create_table_query)
			self.execute_query(insert_row_query)
	
	def execute_query(self, query):
		self.cursor.execute(query)

	def is_value_on_column(self, value, column, table):
		is_table_on_db =  self.is_table_on_db(table)
		if is_table_on_db:
			QUERY = f'select {column} from {table} where {column} = "{value}"';
			
			self.execute_query(QUERY)
			results = self.cursor.fetchall()
			if results:
				return True
			else:
				return False
		return False
		
	def is_table_on_db(self, table_name):
		is_table = False
		SHOW_TABLES_QUERY = 'show tables'
		self.execute_query(SHOW_TABLES_QUERY)
		tables = self.cursor.fetchall()
		for table in tables:
			if table_name in table:
				is_table = True
		return is_table
		
	def get_table_contents(self, table_name):
		QUERY = f'select * from {table_name}'
		contents = self.get_query_contents(table_name, QUERY)
		return contents

	def get_fields_contents_like(self, table_name, field, content):
		QUERY = f'select * from {table_name} where {field} like "%{content}%"'
		contents = self.get_query_contents(table_name, QUERY)
		return contents
	
	def get_table_row_by_id(self, table_name, idField, id_):
		QUERY = f'select * from {table_name} where {idField} = "{id_}"'
		row = self.get_query_contents(table_name, QUERY)
		return row
	
	def get_query_contents(self, table_name, QUERY):
		contents = []
		is_table_on_db = self.is_table_on_db(table_name)
		if(is_table_on_db):
			self.execute_query(QUERY)
			for touple in self.cursor:
				contents.append(touple)
		return contents