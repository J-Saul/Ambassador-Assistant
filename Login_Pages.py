import tkinter as tk  # create basic Graphical User Interface elements
import sqlite3  # database operations
import hashlib  # encryption and hashing

from Validation import Reject
from Ambassador_Hub import AmbassadorHub
from Admin_Hub import AdminHub

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class TALoginPage:
    backgroundColour = 'hot pink'
    # class variables must be used, as they are declared before the window is 'made', so changes can be made by subclass
    title = 'Tech Ambassador Login'
    subtitle = 'Please enter your Ambassador ID and password.'
    windowTitle = 'Tech Ambassador Login System'
    tablePass = "SELECT AmbassadorID, Password FROM TAPass"

    def __init__(self, master):
        self.master = master
        self.master.title(self.__class__.title)

        self.master.geometry('400x200')
        self.master.config(bg=self.__class__.backgroundColour)

        self.title = tk.Label(self.master, text=self.__class__.title,
                              font = ('Arial', 20,'bold'), bg=self.__class__.backgroundColour)
        self.subtitle = tk.Label(self.master, text=self.__class__.subtitle,
                                 font = ('Arial', 14, 'italic'), bg=self.__class__.backgroundColour)
        self.title.pack(side='top')
        self.subtitle.pack(side='top')

        self.user_label = tk.Label(self.master, text = 'User ID   ',
                                   bg=self.__class__.backgroundColour)
        self.username = tk.Entry(self.master,
                                 highlightbackground = self.__class__.backgroundColour)

        self.user_label.place(x=60, y=70) #pady(top,bottom)
        self.username.place(x=130, y=70)

        self.pass_label = tk.Label(self.master, text = 'Password ', bg=self.__class__.backgroundColour)
        self.password = tk.Entry(self.master, show = "*", highlightbackground =self.__class__.backgroundColour)

        self.pass_label.place(x=60,y=100)
        self.password.place(x=130,y=100)

        self.submit = tk.Button(self.master, text = 'Submit', highlightbackground=self.backgroundColour,
                                command=self.check)  # calls username and password to be checked
        self.submit.place(x=120,y=150)
        self.Return = tk.Button(self.master, text = 'Quit', highlightbackground=self.backgroundColour,
                                command=self.returnHome)  # this command closes this window, back to duel login
        self.Return.place(x=200, y=150)

    def check(self):  # checks that the username and password are stored
        try:
            self.userString = int(self.username.get())  # accesses the inputted label
            self.passString = str(self.password.get())

            self.encodedPassword = self.passString.encode() # encodes the string into bytes that can be accepted
            self.result = hashlib.sha224(self.encodedPassword)  # sent to SHA224, secure hashing algorithm
            self.encryptedPassword = str(self.result.hexdigest())  # returns the encoded data in hexadecimal format which is then converted to a string

            self.results = dbCursor.execute(self.__class__.tablePass)  # selects the ID and password from either the student or ambassador table
            self.attempts = 0  # incremented for every record, used to check if a username/password does (or does not) exist in table
            self.foundFlag = False

            for row in self.results.fetchall():  # for every record (person) in database...
                if self.userString == row[0] and self.encryptedPassword == row[1]:  # checks if entered userID is the same as the stored ID
                    self.confirmLogin()
                    # removed default password bit for now
                else:
                    self.attempts += 1
            if self.attempts > len(self.results.fetchall()) and self.foundFlag == False:  # if every record has been checked and the user has not been found

                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, 'Incorrect user ID or password, please try again.')

        except ValueError:
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, "Invalid user ID or Password")

    def confirmLogin(self):
        self.foundFlag = True
        self.master.withdraw()  # hides the window
        dbConnection.commit()
        self.openAmbassadorHub = tk.Toplevel(self.master)
        self.app = AmbassadorHub(self.openAmbassadorHub, self.userString)

    def returnHome(self):
        self.master.destroy()


class AdminLoginPage(TALoginPage):
    # inherits from the TALoginPage parent class
    backgroundColour = 'gold'
    title = 'Admin Login'
    subtitle = 'Please enter your Admin ID and password.'
    windowTitle = 'Admin Login System'
    tablePass = "SELECT AdminID, Password FROM AdminPass"

    def __init__(self,master):
        TALoginPage.__init__(self, master)

    def confirmLogin(self):  # overrides the parent class method
        self.foundFlag = True
        self.master.withdraw()
        dbConnection.commit()
        self.openAdminHub = tk.Toplevel(self.master)
        self.app = AdminHub(self.openAdminHub)
