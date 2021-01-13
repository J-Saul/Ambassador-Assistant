import tkinter as tk  # create basic Graphical User Interface elements
import sqlite3  # database operations

from AmbassadorScroller import AmbassadorScroller
from Book_Hub import BookHub
from Validation import Reject

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class ChoosePage:
    def __init__(self, master):
        self.master = master
        self.master.title('Login System')
        self.master.geometry('600x700')
        self.master.config(bg='white')
        self.master.title('Choose your Ambassador')

        self.buffer = tk.Label(self.master, text = '        ', bg = 'white')
        self.buffer.grid(row = 0, column = 0)

        self.title = tk.Label(self.master, text= 'Hello there!', font = ('Arial', 30,'bold'), bg='white')
        self.subtitle = tk.Label(self.master, text= 'Who would you like to book an appointment with?',
                                 font = ('Arial', 16, 'italic'), bg='white')

        self.title.grid(row = 0, column = 1)
        self.subtitle.grid(row = 1, column = 1)

        self.scrollthrough = AmbassadorScroller(self.master, 525, 1)
        # creates a widget using the AmbassadorScroller object, passing the height and column

        self.enterIDLabel = tk.Label(self.master, text = 'Please enter the ID of the Ambassador '\
                                                         'you wish to meet with', font = ('Arial', 14, 'italic'))
        self.enterIDLabel.grid(row = 3, column = 1)

        self.enterID = tk.Entry(self.master)  # a widget for users to input text
        self.enterID.grid(row = 4, column = 1)

        self.buttonFrame = tk.Frame(self.master, bg = 'white')
        self.buttonFrame.grid(row = 5, column = 1)
        self.submit = tk.Button(self.buttonFrame, text= 'Submit', command = self.checkID)

        self.submit.grid(row = 0, column = 0)
        self.returnHome = tk.Button(self.buttonFrame, text= 'Return', command = self.returnHome)
        self.returnHome.grid(row = 0, column = 1)

    def checkID(self):
        try:
            dbCursor.execute("SELECT Forename FROM TechAmbassadors WHERE AmbassadorID = ?",(self.enterID.get(),))
            # find the forename of the ambassador with entered ID
            foundName = dbCursor.fetchone()  # only one result needed to be fetched, IDs are unique

            if foundName:  # if it exists
                self.enterIDLabel.config(text = foundName)
                self.ID = self.enterID.get()
                self.master.destroy()  # destroys the current root; the alternative would be to hide all pages, which makes things really slow
                self.master = tk.Tk()  # creates a new root
                self.app = BookHub(self.master, foundName, self.ID)  # self.app is an instance of the Bookhub class.
                self.master.mainloop()  # run a new loop
            elif not self.enterID.get().isnumeric():
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "Please enter the Ambassador's ID, no letters!")
            else:
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "This ID was not found. Please try again.")
        except:
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, "Invalid Ambassador ID. Please try again")

    def returnHome(self):
        self.master.destroy()
