import tkinter as tk  # create basic Graphical User Interface elements
import calendar  # get relevant dates
import datetime  # get current time
from functools import partial
import sqlite3  # database operations

from Book_Meeting import BookMeeting


dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class BookHub:
    def __init__(self, master, nameResult, ID):
        self.master = master
        self.master.geometry('1240x616')
        self.master.title('Booking Hub')

        self.windowFrame = tk.Frame(self.master, bg = 'lightgreen')
        self.windowFrame.grid()
        self.nameResult = nameResult
        self.ID = ID

        self.name = str(self.nameResult).replace("\'","").replace("(","").replace(")","").replace(',',"")
        self.Title = tk.Label(self.windowFrame, text = (str(self.name) + "'s Availability Schedule"), font = ('Arial', 20,'bold'), bg = 'lightgreen')
        self.description = tk.Label(self.windowFrame, text = 'Please double click a time slot that works for you.', font = ('Arial', 15, 'bold'), bg ='lightgreen')
        self.Title.grid(row = 0, column = 1)
        self.description.grid(row = 1, column = 1)

        self.timetableFrame = tk.Frame(self.windowFrame, bg = 'red', width = 1200, height = 700)
        self.timetableFrame.grid(row = 4, column = 1)
        self.home = tk.Button(self.windowFrame, text = 'Quit', width = 50, highlightbackground = 'lightgreen', command = self.returnHome)
        self.home.grid(row = 5, column = 1)
        self.TAavailability = dbCursor.execute('''SELECT BeforeSchool, Breaktime, Lunchtime, AfterSchool FROM AmbassadorAvailability WHERE AmbassadorID = ?''', (self.ID,))
        self.availability = [[0 for days in range(5)] for times in range(4)]  # create empty 2D array

        counter = 0
        for e in self.TAavailability.fetchone():  # gets the string for each ambassador, e.g. 'YYNYNNYNYNYN...'
            for i in range(5):
                self.availability[counter][i] = e[i]
            counter+= 1

        def double_click(button, event):
            row = int(button.grid_info()['row']) - 1
            column = int(button.grid_info()['column'])

            width = 248  # width of each label
            height = 133
            lowerboundX = 50  # x coordinate from very left of page
            lowerboundY = 150  # y coordinate at very top of timetable boxes

            x = event.x_root
            y = event.y_root
            column = 0

            global day
            global time


            if y < (lowerboundY+(2*height)):
                # centre y, equivalent of binary search, far faster than a FOR loop
                if y < (lowerboundY+(height)):
                    time = 'BeforeSchool'
                else:
                    time = 'Breaktime'
            else:
                if y < (lowerboundY+(3*height)):
                    time = 'Lunchtime'
                else:
                    time = 'AfterSchool'

            if x < (lowerboundX+(2*width)):  # leftmost 2
                if x < (lowerboundX+(width)):
                    day = 'Monday'
                    column = 0
                else:
                    day = 'Tuesday'
                    column = 1
            else:
                if x < (lowerboundX+(4*width)):
                    if x < (lowerboundX+(3*width)):
                        day = 'Wednesday'
                        column = 2
                    else:
                        day = 'Thursday'
                        column = 3
                else:
                    day = 'Friday'
                    column = 4

            date = self.updatedDates[column][0] + " " + str(self.updatedDates[column][1])
            dbConnection.commit()
            self.openBookMeeting = tk.Toplevel(self.master)  # opens first top level window
            self.app = BookMeeting(self.openBookMeeting, self.ID, self.name,"Please enter your full name, class and email to book a meeting for " + day + " at "+ time + ".", date, day, time)

        self.rowCounter = 0
        self.columnCounter = 0
        self.updatedDates = []
        self.buttonCounter = 0

        self.colours = ['IndianRed1','yellow','CadetBlue1','OliveDrab1','PaleVioletRed1','tomato','yellow2','turquoise1','OliveDrab2','hot pink','firebrick1','gold','DeepSkyBlue2', 'green2', 'deep pink', 'firebrick3','goldenrod','RoyalBlue1', 'green3', 'DeepPink3']
        # loops through the colours for each day
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.times = ['Before School', 'Break Time', 'Lunch Time', 'After School']
        self.months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: "September", 10: 'October', 11: 'November', 12: 'December'}
        # dictionary to convert a counter into the relevant month

        self.today = datetime.date.today()
        self.nextMonday = self.today + datetime.timedelta(days=-self.today.weekday(), weeks=0)  # gets next Monday's data, e.g. 2020-10-12
        self.lastDay = calendar.monthrange(2020,self.today.month)  # gets the last day of the current month

        self.totalDayCounter = 0
        self.newMonthcounter = 0
        while self.totalDayCounter < 5:
            if (self.nextMonday.day + self.totalDayCounter) > self.lastDay[1]: # if the day is before the last day of the month
                try:
                    self.updatedDates.append((self.months[self.nextMonday.month + 1], 1 + self.newMonthcounter))  # date resets to 1
                    # appends the next 5 dates to the array
                except:
                    self.updatedDates.append(('January', 1 + self.newMonthcounter))  # triggers if its December- end of the year
                    # appends the next 5 dates to the array
                self.newMonthcounter += 1

            else:
                self.updatedDates.append((self.months[self.nextMonday.month], self.nextMonday.day + self.totalDayCounter))
            self.totalDayCounter += 1

        def handle_enter(button, event):
            button.config(relief = 'sunken')

        def handle_leave(button, event):  # returns border back to normal
            button.config(relief = 'raised')

        for i in range(4):  # create unique buttons and retrieves information
            for e in range(5):  # same variable used to define 2D array; that there are 3 ambassadors

                if self.buttonCounter % 5 == 0: # if there is a need for a new row, every fifth button
                    self.columnCounter = 0 # column resets to 0, otherwise continues to 5,6,7 etc.
                    self.meetingTime = (self.days[self.columnCounter]+ ': ' + self.times[self.rowCounter] +'\n')
                    self.rowCounter+=1 # incremented when new row needed
                else:
                    self.columnCounter +=1
                    self.meetingTime = (self.days[self.columnCounter]+ ': ' + self.times[self.rowCounter-1] + '\n')
                self.relevantDate = self.updatedDates[self.columnCounter][0] + " " + str(self.updatedDates[self.columnCounter][1])

                if self.availability[i][e] == 'Y':
                    self.button = tk.Label(self.timetableFrame, text = (self.meetingTime + self.relevantDate + '\n\n Available'), height = 8, width = 27,
                                           bg = self.colours[self.buttonCounter], wraplength = 225, justify = 'center', borderwidth = 2, relief = 'raised')
                    self.button.bind('<Double 1>', partial(double_click, self.button))
                    self.button.bind("<Enter>", partial(handle_enter, self.button))  # when the mouse hovers over
                    self.button.bind("<Leave>", partial(handle_leave, self.button))  # when the mouse leaves

                else:
                    self.button = tk.Label(self.timetableFrame, text = (self.meetingTime + self.relevantDate + '\n\n' + 'Unavailable'), height = 8, width = 27,
                                           bg = 'gray50', wraplength = 225, justify = 'center', borderwidth = 2, relief = 'raised')

                self.button.grid(row = self.rowCounter, column = self.columnCounter)
                self.buttonCounter += 1

    def returnHome(self):
        self.master.destroy()
