# Archive Application (Frontend/GUI)
from backend import Database
from tkinter import *


"""
Frontend:

    A program that stores this book information:
    title, Author
    Year, ISBN (id for books)

    User can:
    View all records
    Search an entry
    Add entry
    Update entry
    Delete
    Close

    Need:
    4 labels boxes (title, author, year, isbn)
    1 listbox (output for list of books)
    6 Buttons for View all, search, add, update, delete, close

    Need visual drawing of design/UI.
"""

# connect to Database class in backend file
database=Database("books.db")


class Application(object):

    def __init__(self, window):
        self.window=window
        # WINDOW + WIDGETS
        # Add title on window
        self.window.wm_title("BookStore")
        
        # Labels
        l1=Label(window,text="Title")
        l1.grid(row=0,column=0)
        
        l2=Label(window,text="Author")
        l2.grid(row=0,column=2)
        
        l3=Label(window,text="Year")
        l3.grid(row=1,column=0)
        
        l4=Label(window,text="ISBN")
        l4.grid(row=1,column=2)
        
        # Entries for Labels
        # textvariable expects value the user will enter.
        # datatype - function that creates the special object
        self.title_text=StringVar()
        self.e1=Entry(window,textvariable=self.title_text)
        self.e1.grid(row=0,column=1)
        
        self.author_text=StringVar()
        self.e2=Entry(window,textvariable=self.author_text)
        self.e2.grid(row=0,column=3)
        
        self.year_text=StringVar()
        self.e3=Entry(window,textvariable=self.year_text)
        self.e3.grid(row=1,column=1)
        
        self.isbn_text=StringVar()
        self.e4=Entry(window,textvariable=self.isbn_text)
        self.e4.grid(row=1,column=3)
        
        
        # Listbox
        self.lb1=Listbox(window,height=10,width=27)
        self.lb1.grid(row=2,column=0,rowspan=6,columnspan=2)
        # bind method to a listbox widget so user can select a row and view it in the widget entries.
        self.lb1.bind("<<ListboxSelect>>",self.get_selected_row)
        
        # Scrollbar
        self.sb1=Scrollbar(window, orient="vertical")
        self.sb1.grid(row=2,column=2,rowspan=6)
        
        self.lb1.configure(yscrollcommand=self.sb1.set)  # set y axis to scrollbar
        # create cofigure method to the listbox and scrollbar
        self.sb1.configure(command=self.lb1.yview)  # vertical view will not change.
        
        
        # Buttons
        # Add functions to buttons
        
        self.b0=Button(window,text="Clear entries",width=12,command=self.clear_command)
        self.b0.grid(row=2,column=3)
        
        self.b1=Button(window,text="View all",width=12,command=self.view_command)
        self.b1.grid(row=3,column=3)
        
        self.b2=Button(window,text="Search entry",width=12,command=self.search_command)
        self.b2.grid(row=4,column=3)
        
        self.b3=Button(window,text="Add entry",width=12,command=self.add_command)
        self.b3.grid(row=5,column=3)
        
        self.b4=Button(window,text="Update",width=12,command=self.update_command)
        self.b4.grid(row=6,column=3)
        
        self.b5=Button(window,text="Delete",width=12,command=self.delete_command)
        self.b5.grid(row=7,column=3)
        
        self.b6=Button(window,text="Close",width=12,command=window.destroy)
        self.b6.grid(row=8,column=3)



    # FUNCTIONS
    # event parameter holds info about the type of event. 
    def get_selected_row(self,event):
        global selected_tuple
        # get the index
        if len(self.lb1.curselection()) != 0:
            index=self.lb1.curselection()[0]
            # get the actual tuple. from lb1 get tuple from index x.
            self.selected_tuple=self.lb1.get(index)
            # delete any text in entries 
            self.e1.delete(0,END)
            # fill entries with values user selects
            self.e1.insert(0,self.selected_tuple[1])
        
            self.e2.delete(0,END)
            self.e2.insert(0,self.selected_tuple[2])
    
            self.e3.delete(0,END)
            self.e3.insert(0,self.selected_tuple[3])
    
            self.e4.delete(0,END)
            self.e4.insert(0,self.selected_tuple[4])
    
    
    def clear_command(self):
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        self.e4.delete(0,END)
    
    
    # Add the tuple values from the database view function to the window.
    def view_command(self):
        # delte everything from 0 to the end before iterating.
        # this deltes the previous output on the screen.
        self.lb1.delete(0,END)
        # this loops through the tuples outputting each individually.
        for row in database.view():
            # insert each new tuple in the list of tuples to the end of box
            self.lb1.insert(END,row)  # 0 = start of listbox
    
    
    def search_command(self):
        # before starting you want to empty the listbox
        self.lb1.delete(0,END)
        # loop through database list output and add in entry widgets
        # get() outputs a string value.
        if len(database.search(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get())) > 0:
            for row in database.search(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get()):
                # insert list values at end of listbox
                self.lb1.insert(END,row)
        else:
            self.lb1.insert(END, "Cannot find book")
    
    
    # allow user to insert a book
    def add_command(self):
        self.lb1.delete(0,END)
        database.insert(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get())
        self.lb1.insert(END, database.search(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get()))
    
    
    # allow user to click a book, then values will be inserted in their corresponding entry widgets for them to delete.
    def delete_command(self):
        self.lb1.delete(0,END)
        # pass id of deleted function to the database script
        database.delete(self.selected_tuple[0])
        for row in database.view():
            # insert each new tuple in the list of tuples to the end of box
            self.lb1.insert(END, row)  # 0 = start of listbox
    
    
    def update_command(self):
        self.lb1.delete(0,END)
        database.update(self.selected_tuple[0],self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get())



window=Tk()
Application(window)
window.mainloop()






#


