from db_connector import DBConnector

# Responsible for implementing a layer between a 
# generic interface (terminal, desktop GUI or a frentend),
# a backend/api (if appliable) and the database connector.

# It's not responsible for parsing JSON into strings/integers. That's
# up to the API/Backend. Middleware uses the already parsed python data to 
# interact with the database, never directly, but through the functions 
# providaded by the db_connector. 

class Middleware:
	def __init__(self, user, password, database):
		self.connector = DBConnector(user=user, password=password, database=database)
		self.TABLE_NAME = 'books'
		self.ID_FIELD = 'BookID'

	def add_book(self, available, title, author, category, price, url):
		bookID = self.get_book_id(title, author, category, price=price)
		is_book_on_db = self.connector.is_value_on_column(bookID, self.ID_FIELD, self.TABLE_NAME)
		if not is_book_on_db: 
			CREATE_TABLE_QUERY = 'create table books(bookID varchar(60) not null, available int, title varchar(50), author varchar(100), category varchar(50), price float(7,2), url varchar(200), primary key(bookID));'
			INSERT_ROW_QUERY = f'insert into books (bookID, available, title, author, category, price, url) values ("{bookID}", {available}, "{title}", "{author}", "{category}", {price}, "{url}");'
			self.connector.upsert_table_and_row(self.TABLE_NAME, CREATE_TABLE_QUERY, INSERT_ROW_QUERY)
		else:
			INCREASE_AVAILABLE_BOOKS_QUERY = f'update books set available = available + {available} where bookid = "{bookID}";'
			self.connector.execute_query(INCREASE_AVAILABLE_BOOKS_QUERY)
			
	# Deveria estar em livro, não é responsabilidade de middleware saber
	# may have collisions. Use better hash algorithm. 
	@staticmethod
	def get_book_id(*args, price):
		id_ = str(price)
		for arg in args:
		    id_ = id_ + '_' + arg.split()[-1]
		return id_

	def list_books(self):
		all_books_contents = self.connector.get_table_contents(self.TABLE_NAME)
		return all_books_contents
		
	def search_book(self, field, content):
		cursor = self.connector.connection.cursor()
		all_books_contents = self.connector.get_fields_contents_like(self.TABLE_NAME, field, content)
		return all_books_contents
		
	def edit_book(self, oldBookID, available, title, author, category, price, url):
		cursor = self.connector.connection.cursor()
		
		is_old_ID_on_db = self.connector.is_value_on_column(oldBookID, self.ID_FIELD, self.TABLE_NAME)
		if not is_old_ID_on_db:
			print("Book cannot be edited: it's not on library")
			return None
		newBookID = self.get_book_id(title, author, category, price=price)
		is_new_book_on_db = self.connector.is_value_on_column(newBookID, self.ID_FIELD, self.TABLE_NAME)
		
		if is_new_book_on_db:
			# IDEIA: pegar quantidade do atual, deletar atual, somar quantidade do atual no novo. 
			print("Book cannot be editted: New book is already on library")
			print(f'Remove all {newBookID} and then edit current book.')
			return None
		else:
			QUERY = f'update books set bookID =  "{newBookID}", available = {available}, title = "{title}", author = "{author}", category = "{category}", price = {price}, url = "{url}" where bookID = "{oldBookID}"'
			self.connector.execute_query(QUERY)

	def delete_book(self, quantity, BookID):
		book_info = self.connector.get_table_row_by_id(self.TABLE_NAME, self.ID_FIELD, BookID)
		if book_info:
			books_available = book_info[0][1]
			if books_available > quantity:
				QUERY = f'update books set available = {books_available-quantity} where BookID = "{BookID}"'
				self.connector.execute_query(QUERY)
			elif books_available == quantity:
				QUERY = f'delete from books where BookID = "{BookID}"';
				self.connector.execute_query(QUERY)
			else:
				print(f'{books_available} books available < {quantity} attemtps to remove: ', "Books cannot be removed: Less books than required for removing." )
		else:
			print(f"Book {BookID} cannot be removed: it's not on library")
	
	def increment_book(self, quantity, BookID):
		book_info = self.connector.get_table_row_by_id(self.TABLE_NAME, self.ID_FIELD, BookID)
		if book_info:
			books_available = book_info[0][1]
			QUERY = f'update books set available = {books_available+quantity} where BookID = "{BookID}"'
			self.connector.execute_query(QUERY)
		else:
			print(f"Book {BookID} cannot be incremented: it's not on library")

	
	def populate_library(self):
		is_books_table_on_db = self.connector.is_table_on_db(self.TABLE_NAME)
		if not is_books_table_on_db:
			self.add_book(5, 'Harry potter and the Sorcerer Stone', 'Jk Rowling', 'Fantasy', 15.99, 'https://images-na.ssl-images-amazon.com/images/I/51HSkTKlauL._SX346_BO1,204,203,200_.jpg')
			self.add_book(3, 'Harry potter and the Chamber of Secrets', 'Jk Rowling', 'Fantasy', 15.99, 'https://images-na.ssl-images-amazon.com/images/I/91OINeHnJGL.jpg')
			self.add_book(2, 'Harry potter and Half Blood Prince', 'Jk Rowling', 'Fantasy', 15.99, 'https://images-na.ssl-images-amazon.com/images/I/51uO1pQc5oL._SX329_BO1,204,203,200_.jpg')
			self.add_book(2, "The Magician's Nephew", 'C.S Lewis', 'Fantasy', 10.48, 'https://i.harperapps.com/hcanz/covers/9780006716839/y648.jpg')
			self.add_book(3, "Dom Quixote", 'Miguel de Cervantes', 'Classics', 23.98, 'https://m.media-amazon.com/images/I/51BwjHCepIL.jpg')
			self.add_book(1, "Le Petit Prince", 'Antoine de Saint-Exupéry', 'Classics', 8.99, 'https://kbimages1-a.akamaihd.net/7334ddda-76e1-4028-9e18-ec871e81821f/1200/1200/False/le-petit-prince-el-principito.jpg')

