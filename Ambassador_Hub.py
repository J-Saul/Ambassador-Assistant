import tkinter as tk
from tkinter import ttk  # more advanced GUI elements stored in inner directory
import sqlite3  # database operations
import calendar  # get relevant dates
import datetime  # get current time
from functools import partial

from Validation import Success

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class AmbassadorHub:
    def __init__(self, master, ambassadorID):
        self.master = master
        self.ambassadorID = ambassadorID
        self.master.geometry('625x690')
        self.master.title('Ambassador Hub')
        parentTab = ttk.Notebook(self.master)
        self.tab1 = ttk.Frame(parentTab)
        self.tab2 = ttk.Frame(parentTab)
        dbCursor.execute('''SELECT Forename FROM TechAmbassadors WHERE AmbassadorID = ?''', (self.ambassadorID,))
        for name in dbCursor.fetchone():
            self.forename = name

        # ======= tab 1 widgets ===========
        parentTab.add(self.tab1, text='Set Availability')
        self.windowFrame = tk.Frame(self.tab1, bg = 'orange')
        self.windowFrame.grid()
        self.title = tk.Label(self.windowFrame, text = 'Welcome back, ' + self.forename + '.', bg = 'orange', font = ('Arial', 20,'bold'))
        self.title.grid(row = 0, column = 0)
        self.subtitle = tk.Label(self.windowFrame, text = 'Double click when you are available next week' +'\n', bg = 'orange', font = ('Arial', 14, 'italic'))
        self.subtitle.grid(row = 1, column = 0)
        self.availabilityFrame = tk.Frame(self.windowFrame, bg = 'orange')
        self.availabilityFrame.grid(row = 2, column = 0)
        self.gridInfo = []
        self.buttonFrame = tk.Frame(self.windowFrame, bg = 'orange')
        self.buttonFrame.grid(row = 3, column = 0)
        self.submit = tk.Button(self.buttonFrame, text = 'Submit', highlightbackground = 'orange', command = lambda: self.updateAvailability())
        self.submit.grid(row = 0, column = 0)
        self.fix = tk.Button(self.buttonFrame, text = 'Fix Schedule', highlightbackground = 'orange', command = self.fix_time)
        self.returnHome = tk.Button(self.buttonFrame, text = 'Quit', highlightbackground = 'orange', command = self.returnHome)
        self.returnHome.grid(row = 0, column = 2)

        self.months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: "September", 10: 'October', 11: 'November', 12: 'December'}
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.times = ['BeforeSchool', 'Breaktime', 'Lunchtime', 'AfterSchool']

        def double_click(button, event):
            if [button.grid_info()['row'], button.grid_info()['column']] in self.gridInfo:
                # checks if the button has been clicked before
                self.gridInfo.remove([button.grid_info()['row'], button.grid_info()['column']])
                button.config(bg = 'lightgrey')
            else:  # if the button hasn't yet been clicked
                self.gridInfo.append([button.grid_info()['row'], button.grid_info()['column']])
                button.config(bg = 'lightgreen')

        self.rowCounter = 0
        self.columnCounter = 0
        self.updatedDates = []
        self.buttonCounter = 0

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
            button.config(relief = 'raised')

        def handle_leave(button, event):  # returns border back to normal
            button.config(relief = 'sunken')

        for i in range(4): # create unique buttons and retrieves information
            for e in range(5): # same variable used to define 2D array; that there are 3 ambassadors

                if self.buttonCounter % 5 == 0: # if there is a need for a new row, every fifth button
                    self.columnCounter = 0 # column resets to 0, otherwise continues to 5,6,7 etc.
                    self.meetingTime = (self.days[self.columnCounter]+ ': ' +'\n' + self.times[self.rowCounter] +'\n')
                    self.rowCounter+=1 # incremented when new row needed
                else:
                    self.columnCounter +=1
                    self.meetingTime = (self.days[self.columnCounter]+ ': ' +'\n' + self.times[self.rowCounter-1] + '\n')
                self.relevantDate = str(self.updatedDates[self.columnCounter]).replace("('",'').replace('\',',"").replace(")",'')

                self.button = tk.Label(self.availabilityFrame, text = (self.meetingTime + self.relevantDate),
                                       height = 8, width = 12, bg = 'lightgrey', wraplength = 225, justify = 'center', borderwidth = 2, relief = 'sunken')
                self.button.bind('<Double 1>', partial(double_click, self.button))  # function found in line 886
                self.button.bind("<Enter>", partial(handle_enter, self.button))  # when the mouse hovers over
                self.button.bind("<Leave>", partial(handle_leave, self.button))  # when the mouse leaves

                self.button.grid(row = self.rowCounter, column = self.columnCounter)
                self.buttonCounter += 1

        # ======= tab2 widgets ============
        parentTab.add(self.tab2, text='View Meetings')
        parentTab.pack()

        self.windowFrame = tk.Frame(self.tab2, bg = 'orange', height = 600)
        self.windowFrame.pack(fill = tk.BOTH, expand = tk.TRUE)
        self.title = tk.Label(self.windowFrame, text = 'Your Meetings This Week', bg = 'orange', font = ('Arial', 20,'bold'))
        self.title.grid(row = 0, column = 0, sticky = 'nsew')
        self.dateRange = str(self.updatedDates[0]) + ' - ' + str(self.updatedDates[4]) + '\n'
        self.dateRange = self.dateRange.replace("\'",'').replace("(",'').replace(")",'').replace(',',"")
        self.subtitle = tk.Label(self.windowFrame, text = self.dateRange, bg = 'orange', font = ('Arial', 14, 'italic'))
        self.subtitle.grid(row = 1, column = 0, sticky = 'nsew')
        self.meetingFrame = tk.Frame(self.windowFrame, bg = 'orange')
        self.meetingFrame.grid(row = 3, column = 0, sticky = 'nsew')
        self.buffer = tk.Label(self.windowFrame, text = '', bg = 'orange')
        self.buffer.grid(row = 5, column = 0)

        self.colours = ['SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'DodgerBlue2', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'DodgerBlue3']  # assumes no more than 8 meetings booked

        dbCursor.execute("SELECT EXISTS(SELECT StudentID, MeetingID FROM Meetings WHERE AmbassadorID = ?)", (self.ambassadorID,))
        dbConnection.commit()
        for e in dbCursor.fetchone():
            if e == 0:
                self.meetingDetails = tk.Label(self.windowFrame, text = 'You have no meetings this week.', bg = 'lightgreen', width = 100, height = 6, relief = 'flat', borderwidth = 2, font = ('Arial', 12, 'bold'))
                self.meetingDetails.grid(row = 4)

            else:
                self.canvas = tk.Canvas(self.meetingFrame, width = 550, height = 450, bg = 'SkyBlue1')
                self.scrollbar = tk.Scrollbar(self.meetingFrame, orient = 'vertical', command = self.canvas.yview)
                self.scrollableFrame = tk.Frame(self.canvas, bg = 'SkyBlue1', relief = 'sunken')
                self.scrollableFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))

                self.canvas.create_window((0,0), window = self.scrollableFrame, anchor = tk.NW)
                self.canvas.configure(yscrollcommand = self.scrollbar.set)
                self.canvas.pack(side = 'left', fill = tk.BOTH, expand = tk.TRUE)
                self.scrollbar.pack(side = 'right', fill = 'y')
                self.getMeetings = dbCursor.execute("SELECT StudentID, MeetingTime FROM Meetings WHERE AmbassadorID = ?", (self.ambassadorID,))
                self.counter = 0
                self.fetched_meetings = []

                for i in dbCursor.fetchall():
                    self.fetched_meetings.append([i[0], i[1]])  # appends studentID and meetingTime to array

                self.numMeetings = len(self.fetched_meetings)
                self.numMeetingsLabel = tk.Label(self.windowFrame, text = 'You have ' + str(self.numMeetings) + ' meetings this week.' + '\n', bg = 'orange', font = ('Arial', 14, 'bold'))
                self.numMeetingsLabel.grid(row = 2, column = 0)

                for meeting in range(self.numMeetings):
                    self.getStudentDetails = dbCursor.execute("SELECT Forename, Surname, Class, Email FROM CurrentStudents WHERE StudentID = ?", (self.fetched_meetings[meeting][0],))

                    for student in dbCursor.fetchall():
                        # below is just to make things easier to understand and nicer formatted
                        self.fullName = '\n' + student[0] + ' ' + student[1]
                        self.formClass = 'Class: ' + student[2] + '\n'
                        self.email = 'Email: ' + student[3] + '\n'
                        self.fetched_meeting_time = str(self.fetched_meetings[meeting][1]).replace("{",'').replace('}','').replace("\'",'')

                        self.meetingDetailsFrame = tk.Frame(self.scrollableFrame, bg = self.colours[self.counter])
                        self.meetingDetailsFrame.pack(expand=True, fill='y')

                        self.nameLabel = tk.Label(self.meetingDetailsFrame, text = self.fullName, bg = self.colours[self.counter], width = 70, relief = 'flat', borderwidth = 2, font = ('Arial', 14, 'bold'))
                        self.otherDetails = tk.Label(self.meetingDetailsFrame, text = self.formClass + self.email + self.fetched_meeting_time, bg = self.colours[self.counter], width = 70, height = 8, relief = 'flat', borderwidth = 2, font = ('Arial', 14))
                        self.nameLabel.grid(row = 0, column = 0)
                        self.otherDetails.grid(row = 1, column = 0)
                        self.meetingDetailsFrame.grid_rowconfigure(0, weight = 1)
                    self.counter += 1

        self.returnHome2 = tk.Button(self.windowFrame, text= 'Return', highlightbackground = 'orange', command = lambda: self.master.destroy())
        self.returnHome2.grid(row = 6, column = 0)

    def returnHome(self):
        self.master.destroy()

    def updateAvailability(self):
        self.next_week_availabilities = ['NNNNN'] * 4
        for meetingTime in self.gridInfo:
            # tempList -> ['N','N' ...]                       V grid row V   V row is 1 too big
            tempList = list(self.next_week_availabilities[int(meetingTime[0])- 1])
            # meetingTime[0] gets the row (which is the time for the meeting)
            tempList[int(meetingTime[1])] = 'Y'
            self.next_week_availabilities[int(meetingTime[0])-1] = ''.join(tempList)
            # gets the list for each row
        for i in range(4):
            dbCursor.execute("UPDATE TempAmbassadorAvailability SET %s = ? WHERE AmbassadorID = ?"
                             % self.times[i], (self.next_week_availabilities[i], self.ambassadorID))
        dbConnection.commit()

        self.openSuccess = tk.Toplevel(self.master)
        self.app = Success(self.openSuccess,
                           "Database successfully updated. You can set this as your default "
                           "schedule by clicking the 'fix schedule' button")
        self.fix.grid(row = 0, column = 1)
        self.check_exists()

    def check_exists(self):  # check if the user has a fixed schedule already
        with open(r"Fixed Meeting Times.txt", "r") as file_to_read:
            #find_lines = file_to_read.readlines()  # reads all the lines in the file

            find_lines = [i for i in file_to_read.readlines() if i != '\n']
            existing_fixed = [ID[0] for ID in find_lines if ID[0].isnumeric()]  # gets all IDs of fixed meetings into an array
            file_to_read.close()
            try:
                existing_index = existing_fixed.index(str(self.ambassadorID)) * 2  # finds the index of the ID in the array
                # multiplied by 2 as the index is always on an even row, and the array on the odds
                with open(r"Fixed Meeting Times.txt", "w") as file_to_write:
                    find_lines = find_lines[:existing_index] + find_lines[(existing_index + 2):]
                    # overwrites the file with everything before and everything after
                    file_to_write.writelines(find_lines)  # If you make a new availability it removes your fixed availability
                    file_to_write.close()
            except ValueError:  # if no fixed schedule was made for that ambassador: existing_index does not return an int
                return


    def fix_time(self):
        self.check_exists()

        with open(r"Fixed Meeting Times.txt", "a+") as file_to_write:
            self.what_to_write = str(self.ambassadorID) + '\n' + str(self.next_week_availabilities) + '\n'
            self.fixedtime = file_to_write.write(self.what_to_write)
            file_to_write.close()

        self.openSuccess = tk.Toplevel(self.master)
        self.app = Success(self.openSuccess, 'Schedule successfully fixed')
