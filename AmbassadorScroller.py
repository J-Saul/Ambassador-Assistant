import tkinter as tk  # create basic Graphical User Interface elements
from PIL import ImageTk, Image  # display images on Tkinter widgets
import sqlite3  # database operations

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class AmbassadorScroller:
    def __init__(self, master, height, column):  # height and column depend on the size of the window
        self.master = master
        self.height = height
        self.column = column
        self.container = tk.Frame(self.master)
        self.container.grid(row = 2, column = self.column)

        self.canvas = tk.Canvas(self.container, width = 500, height = self.height, bg = 'SkyBlue1')  # used for images and visual elements
        self.scrollbar = tk.Scrollbar(self.container, orient = 'vertical', command = self.canvas.yview)
        # creates a scrollbar within the container frame
        self.scrollableFrame = tk.Frame(self.canvas, bg = 'SkyBlue1', relief = 'sunken')  # creates a frame to scroll

        self.scrollableFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        # triggers when the inner contents change size, bbox("all") gives a tuple of the scroll region's corners' positions
        self.canvas.create_window((0,0), window = self.scrollableFrame, anchor = tk.NW)  # window is placed at the (0,0) coordinate
        self.canvas.configure(yscrollcommand = self.scrollbar.set)  # when the y position changes, the scrollbar moves

        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.TRUE)
        self.scrollbar.pack(side = tk.RIGHT, fill = 'y')

        TAresults = dbCursor.execute("SELECT AmbassadorID, Forename, Surname, Gender, YearGroup, Email, Photo FROM TechAmbassadors")
        # fetches all rows based on this query

        counter = 0
        for i in TAresults.fetchall():
            if counter%2 == 0:  # alternates colours for clarity
                self.colour = 'LightBlue2'
            else:
                self.colour = 'LightBlue1'
            counter += 1
            self.personFrame = tk.Frame(self.scrollableFrame, bg = self.colour)  # each person gets a unique frame
            self.personFrame.grid(row = counter, column = 0)
            # unique labels for each detail about the person
            tk.Label(self.personFrame, text = '', bg = self.colour, font = ('Arial', 20,'bold')).grid(row = 0, column = 0)
            tk.Label(self.personFrame, text = ('Ambassador ID: ' + str(i[0])), bg = self.colour, wraplength = 280,
                     font = ('Arial', 20,'bold')).grid(row = 1, column = 0)
            tk.Label(self.personFrame, text = (i[1],i[2]), bg = self.colour, font = ('Arial', 20)).grid(row = 2, column = 0)
            tk.Label(self.personFrame, text = i[3], bg = self.colour, font = ('Arial', 20)).grid(row = 3, column = 0)
            tk.Label(self.personFrame, text = "Year "+ str(i[4]), bg = self.colour, font = ('Arial', 20)).grid(row = 4, column = 0)
            tk.Label(self.personFrame, text = i[5], wraplength = 280, bg = self.colour, font = ('Arial', 20)).grid(row = 5, column = 0)
            tk.Label(self.personFrame, text = '', bg = self.colour, font = ('Arial', 20)).grid(row = 6, column = 0)

            # photos best at 198x197 pixels
            self.photoFrame = tk.Frame(self.scrollableFrame, bg = self.colour)
            self.photoFrame.grid(row = counter, column = 1)
            # note: database stores name of photo stored in seperate folder, not actual photo
            self.myPhoto = str(i[6]).replace("('",'').replace("',)",'')  # gets filename stored, in proper format
            self.im = Image.open(self.myPhoto)  # accesses the image from the fetched file name
            self.photo = ImageTk.PhotoImage(self.im)  # creates an image widget that is compatible with Tkinter
            self.label = tk.Label(self.photoFrame, image = self.photo)  # places this image on a label for that person
            self.label.image = self.photo
            self.label.grid()
