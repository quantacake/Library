# Archive Application (Backend)
import sqlite3

"""
Backend:
    
    Attach functions to all objects (e.g. listbox, butotns,
    entries, etc) which will retreive data from an
    SQLite database.
"""

class Database:

    # initializer / constructor
    # this gets executed when you call an instance of the class.
    # it is called in frontend.py as database=Database()
    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title text, author text, year integer, isbn integer)")
        self.conn.commit()
    
    
    # user enters title, author, year, isbn
    def insert(self, title, author, year, isbn):
        # do not have to pass incremental values manually like id. 
        # only add id to string.
        self.cur.execute("INSERT INTO book VALUES(Null,?,?,?,?)",(title,author,year,isbn))
        self.conn.commit()
    
    
    # fetch all rows of the table.
    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows=self.cur.fetchall()
        return rows
        
    

    # user enter title, author, year, or isbn 
    # pass empty string as default values if they do not exist.
    # now the sql statement will search for an empty string along with values.
    def search(self,title="",author="",year="",isbn=""):
        self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",(title,author,year,isbn))
        rows=self.cur.fetchall()
        return rows
    
    
    # user first searches in database, then finds the ID of the book they want to delete.
    def delete(self,id):
        # column name is after the WHERE. paramter is the id user inputs
        self.cur.execute("DELETE FROM book WHERE id=?",(id,))
        self.conn.commit()
    
    
    # allow user to update the entry widgets(Title, Author, Year, ISBN)
    # select entry from widget box then refer to the id.
    # update tables with these new values where id = this
    def update(self,id,title,author,year,isbn):
        self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
        self.conn.commit()

    # before the script exits, this method will be executed
    # in order to close the connection.
    def __del__(self):
        self.conn.close()
        print('database has been closed')


