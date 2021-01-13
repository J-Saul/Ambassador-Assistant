import tkinter as tk
from tkinter import ttk  # more advanced GUI elements stored in inner directory
import sqlite3  # database operations
from functools import partial  # partial functions to bind GUI elements
import calendar  # get relevant dates
import hashlib  # encryption and hashing
import datetime  # get current time
import pandas as pd  # data analysis
import openpyxl  # extract data from excel files
import xlsxwriter  # write data to an excel file
import matplotlib
matplotlib.use("TkAgg")  # links with Tkinter, otherwise program crashes
from matplotlib import pyplot as plt  # display data on a graph 
from os.path import isfile  # used in case an excel file wasn't made last week, i.e. summer holidays

from AmbassadorScroller import AmbassadorScroller
from Validation import Success, Reject
from Extras import Help, New_Admin

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class AdminHub:
    def __init__(self, master):
        self.master = master
        self.master.title('Admin Hub')
        self.master.geometry('700x580')
        parentTab = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(parentTab)
        self.tab2 = ttk.Frame(parentTab)
        self.tab3 = ttk.Frame(parentTab)

        # setup for excel
        self.today = datetime.date.today()
        self.invalid = True
        self.week_counter = -1
        while self.invalid:
            self.LastMonday = self.today + datetime.timedelta(days=-self.today.weekday(), weeks=self.week_counter)
            self.oldFileName = '@' + str(self.LastMonday) + '.xlsx'
            self.path = '/Users/ForcaBarca/PycharmProjects/Databases/' + self.oldFileName
            if isfile(self.path):  # if this was last week's file
                self.invalid = False
            else:
                self.week_counter -= 1  # if file not found, looks to week before that

        self.Monday = self.today + datetime.timedelta(days=-self.today.weekday(), weeks=0)
        self.columnName = str(self.Monday) + ' to ' + str(self.today)
        self.newFileName = '@' + str(self.Monday) + '.xlsx'

        self.file = pd.ExcelFile(self.oldFileName)
        self.df1 = pd.read_excel(self.file, 'Meetings', index = False)  # skiprows = [1] // skips row 1
        self.df2 = pd.read_excel(self.file, 'Ambassadors', index = False)

        self.df1.reset_index(drop=True, inplace=True)
        self.df2.reset_index(drop=True, inplace=True)


        # =======tab1 widgets============
        parentTab.add(self.tab1, text = 'Weekly Summary')
        parentTab.pack(fill = tk.BOTH, expand = tk.TRUE)
        self.windowFrame = tk.Frame(self.tab1, bg = 'gold2', height = 600)
        self.windowFrame.pack(fill = tk.BOTH, expand = tk.TRUE, anchor = tk.CENTER)
        self.windowFrame.columnconfigure(0, weight = 1)
        self.title = tk.Label(self.windowFrame, text = 'Summary For The Week' +'\n', bg = 'gold2', font = ('Arial', 20, 'bold'))
        self.title.grid(row = 0, column = 0)

        self.viewFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.viewFrame.grid(row=1,column=0)
        self.container = tk.Frame(self.viewFrame, bg = 'gold2')
        self.container.grid(row = 0, column = 0)

        self.canvas = tk.Canvas(self.container, width = 280, height = 325, bg = 'aquamarine2')
        self.scrollbar = tk.Scrollbar(self.container, orient = 'vertical', command = self.canvas.yview)
        self.scrollableFrame = tk.Frame(self.canvas, bg = 'aquamarine2', relief = 'sunken')

        self.scrollableFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))

        self.canvas.create_window((0,0), window = self.scrollableFrame, anchor = tk.NW)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.TRUE)
        self.scrollbar.pack(side = tk.RIGHT, fill = 'y')

        self.meetingIDs = dbCursor.execute("SELECT MeetingID FROM Meetings")
        if len(self.meetingIDs.fetchall()) > 0:
            counter = 0
            self.meetingResults = dbCursor.execute("SELECT MeetingID, StudentID, AmbassadorID, MeetingTime FROM Meetings")  # needed again, otherwise below won't execute
            for i in self.meetingResults.fetchall():
                if counter%2 == 0:
                    self.colour = 'aquamarine2'
                else:
                    self.colour = 'seagreen1'
                counter += 1
                self.personFrame = tk.Frame(self.scrollableFrame, bg = self.colour)
                self.personFrame.pack(fill = tk.BOTH, expand = tk.TRUE)

                dbCursor.execute("SELECT Forename, Surname FROM CurrentStudents WHERE StudentID = ?", (i[1],))
                for studentName in dbCursor.fetchall():
                    self.fullname = 'Student: ' + studentName[0] + ' ' + studentName[1]
                dbCursor.execute("SELECT Forename, Surname FROM TechAmbassadors WHERE AmbassadorID = ?", (i[2],))
                for TAname in dbCursor.fetchall():
                    self.fullTAname = 'Ambassador: ' + TAname[0] + ' ' + TAname[1]

                tk.Label(self.personFrame, text = ('\n' +'Meeting ID: ' + str(i[0])), bg = self.colour, wraplength = 290, font = ('Arial', 20,'bold')).grid(row = 0, column = 0)
                tk.Label(self.personFrame, text = self.fullname, bg = self.colour, wraplength = 290, font = ('Arial', 20)).grid(row = 1, column = 0)
                tk.Label(self.personFrame, text = self.fullTAname, wraplength = 290, bg = self.colour, font = ('Arial', 20)).grid(row = 2, column = 0)
                tk.Label(self.personFrame, text = str(i[3]) + '\n', bg = self.colour, font = ('Arial', 20)).grid(row = 3, column = 0)
        else:
            self.scrollableFrame.columnconfigure(0, weight = 1)
            self.noMeetings = tk.Label(self.scrollableFrame, text = "No meetings were booked this week", bg = 'aquamarine2', wraplength = 280, font = ('Arial', 20,'bold'))
            self.noMeetings.pack()

        self.buffer = tk.Label(self.windowFrame, bg = 'gold2').grid(row = 2, column = 0)

        self.viewButtons = tk.Frame(self.viewFrame, bg = 'gold2')
        self.viewButtons.grid(row = 0, column = 1, padx = 10)
        self.meetings = tk.Label(self.viewButtons, bg = 'goldenrod1', text = 'All Meetings' + '\n' + 'Per Class', height = 7, width = 25, font = ('Arial', 20, 'bold'), borderwidth = 2, relief = 'raised')
        self.meetings.grid(row=0, column = 0)
        self.meetings.bind('<Enter>', partial(self.handle_enter, self.meetings))
        self.meetings.bind('<Leave>', partial(self.handle_leave, self.meetings))
        self.meetings.bind('<Double 1>', partial(self.double_click, self.meetings))

        self.ambassadors = tk.Label(self.viewButtons, bg = 'goldenrod1', text = 'All Meetings' + '\n' + 'Per Ambassador', height = 7, width = 25, font = ('Arial', 20, 'bold'), borderwidth = 2, relief = 'raised')
        self.ambassadors.grid(row=1, column = 0)
        self.ambassadors.bind('<Enter>', partial(self.handle_enter, self.ambassadors))
        self.ambassadors.bind('<Leave>', partial(self.handle_leave, self.ambassadors))
        self.ambassadors.bind('<Double 1>', partial(self.double_click, self.ambassadors))


        self.trackLabel = tk.Label(self.windowFrame, bg = 'gold2', text = 'Enter the ID of an Ambassador you want to track', font = ('Arial', 14, 'bold'))
        self.trackLabel.grid(row=3, column=0)
        self.trackFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.trackFrame.grid(row = 4, column = 0)
        self.trackEntry = tk.Entry(self.trackFrame, highlightbackground = 'gold2')
        self.trackEntry.grid(row = 0, column = 0)
        self.submitTrack = tk.Button(self.trackFrame, highlightbackground = 'gold2', text = 'Submit', command = lambda: self.track(self.trackEntry.get()))
        self.submitTrack.grid(row = 0, column = 1)

        self.track_buffer = tk.Label(self.windowFrame, bg = 'gold2', text = '').grid(row = 5, column = 0)
        self.buttonFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.buttonFrame.grid(row = 6, column = 0)
        self.resetButton = tk.Button(self.buttonFrame, highlightbackground = 'gold2', text = 'Reset Week', command = self.excelExport)
        self.resetButton.grid(row=0, column=0)
        self.returnButton = tk.Button(self.buttonFrame, highlightbackground = 'gold2', text = 'Quit', command = self.returnHome)
        self.returnButton.grid(row=0, column=1)
        self.helpButton = tk.Button(self.buttonFrame, highlightbackground = 'gold2', text = 'Help', command = self.openHelp)
        self.helpButton.grid(row=0, column=2)

        # Use as an extention for criterion E
        # self.addAdmin = tk.Button(self.buttonFrame, highlightbackground = 'gold2', text = 'Add Admin', command = self.add_admin)
        # self.addAdmin.grid(row=0, column=3)

        # =======tab 2 widgets===========
        parentTab.add(self.tab2, text = 'Input Ambassador')
        parentTab.pack(fill = tk.BOTH, expand = tk.TRUE)
        self.windowFrame = tk.Frame(self.tab2, bg = 'gold2', height = 600)
        self.windowFrame.pack(fill = tk.BOTH, expand = tk.TRUE)
        self.windowFrame.columnconfigure(0, weight = 1) # centers all widgets
        self.title = tk.Label(self.windowFrame, text = '\n' + 'Input an Ambassador' + '\n', bg = 'gold2', font = ('Arial', 20, 'bold'))
        self.title.grid(row = 0, column = 0)

        self.inputFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.inputFrame.grid(row = 1, column = 0)

        self.forenameLabel = tk.Label(self.inputFrame, bg = 'gold2', text = 'Forename', font = ('Arial', 14, 'bold'))
        self.forenameLabel.grid(row = 0, column = 0)
        self.forenameEntry = tk.Entry(self.inputFrame, highlightbackground = 'gold2')
        self.forenameEntry.grid(row = 0, column = 1)
        self.surnameLabel = tk.Label(self.inputFrame, bg = 'gold2', text = 'Surname', font = ('Arial', 14, 'bold'))
        self.surnameLabel.grid(row = 1, column = 0)
        self.surnameEntry = tk.Entry(self.inputFrame, highlightbackground = 'gold2')
        self.surnameEntry.grid(row = 1, column = 1)
        self.genderLabel = tk.Label(self.inputFrame, bg = 'gold2', text = 'Gender', font = ('Arial', 14, 'bold'))
        self.genderLabel.grid(row = 2, column = 0)
        self.genderFrame = tk.Frame(self.inputFrame, bg = 'gold2')
        self.genderFrame.grid(row = 2, column = 1)
        self.genderVar = tk.IntVar()
        self.male = tk.Radiobutton(self.genderFrame, text = 'Male', bg = 'gold2', variable = self.genderVar, value = 1)
        self.male.grid(row = 0, column = 0)
        self.female = tk.Radiobutton(self.genderFrame, text = 'Female', bg = 'gold2', variable = self.genderVar, value = 2)
        self.female.grid(row = 0, column = 1)
        self.yearTextLabel = tk.Label(self.inputFrame, text = 'Year Group', bg = 'gold2', font = ('Arial', 14, 'bold'))
        self.yearTextLabel.grid(row = 3, column = 0)
        self.yearList = tk.Listbox(self.inputFrame, height = 7)
        self.yearList.insert(tk.END)
        self.all_year_groups = ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12", "Year 13"]
        for i in self.all_year_groups:
            self.yearList.insert(tk.END, i)
        self.yearList.grid(row = 3, column = 1)
        self.email = tk.Label(self.inputFrame, bg = 'gold2', text = 'Email', font = ('Arial', 14, 'bold'))
        self.email.grid(row = 4, column = 0)
        self.emailEntry = tk.Entry(self.inputFrame, highlightbackground = 'gold2')
        self.emailEntry.grid(row = 4, column = 1)
        self.photo = tk.Label(self.inputFrame, bg = 'gold2', text = 'Photo Filename', font = ('Arial', 14, 'bold'))
        self.photo.grid(row = 5, column = 0)
        self.photoEntry = tk.Entry(self.inputFrame, highlightbackground = 'gold2')
        self.photoEntry.grid(row = 5, column = 1)
        self.passwordLabel = tk.Label(self.inputFrame, bg = 'gold2', text = 'Password', font = ('Arial', 14, 'bold'))
        self.passwordLabel.grid(row = 6, column = 0)
        self.passwordEntry = tk.Entry(self.inputFrame, show = '*', highlightbackground = 'gold2')
        self.passwordEntry.grid(row = 6, column = 1)

        self.buffer = tk.Label(self.windowFrame, text = ' ', bg = 'gold2').grid(row = 2, column = 0)
        self.buttonFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.buttonFrame.grid(row = 3, column = 0)
        self.submit = tk.Button(self.buttonFrame, text = 'Submit', highlightbackground = 'gold2', command = self.checkValid)
        self.submit.grid(row = 0, column = 0)
        self.quitButton = tk.Button(self.buttonFrame, text='Quit', highlightbackground = 'gold2', command = self.returnHome)
        self.quitButton.grid(row = 0, column = 1)

        # =======tab3 widgets============
        parentTab.add(self.tab3, text = 'Remove Ambassador')
        parentTab.pack(fill = tk.BOTH, expand = tk.TRUE)
        self.windowFrame = tk.Frame(self.tab3, bg = 'gold2', height = 600)
        self.windowFrame.pack(fill = tk.BOTH, expand = tk.TRUE, anchor = tk.CENTER)
        self.windowFrame.columnconfigure(0, weight = 1) # centers all widgets
        self.title = tk.Label(self.windowFrame, text = 'Remove an Ambassador', bg = 'gold2', font = ('Arial', 16, 'bold'))
        self.title.grid(row = 0, column = 0) # all columns are set to 1 just because that's how ChoosePage is
        self.subtitle = tk.Label(self.windowFrame, text = 'Please enter the ID of the Ambassador you want to remove' + '\n', bg = 'gold2', font = ('Arial', 14, 'italic'))
        self.subtitle.grid(row = 1, column = 0)

        self.scrollthrough = AmbassadorScroller(self.windowFrame, 370, 0)  # the same object used in ChoosePage

        self.buffer = tk.Label(self.windowFrame, bg = 'gold2').grid(row = 3, column = 0)
        self.entryFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.entryFrame.grid(row = 4, column = 0)
        self.IDLabel = tk.Label(self.entryFrame, bg = 'gold2', text = 'Ambassador ID  ', font = ('Arial', 14, 'bold'))
        self.IDLabel.grid(row = 0, column = 0)
        self.IDEntry = tk.Entry(self.entryFrame, highlightbackground = 'gold2')
        self.IDEntry.grid(row = 0, column = 1)

        self.buttonFrame = tk.Frame(self.windowFrame, bg = 'gold2')
        self.buttonFrame.grid(row = 5, column = 0)
        self.submit = tk.Button(self.buttonFrame, text = 'Submit', highlightbackground = 'gold2', command = self.deleteAmbassador)
        self.submit.grid(row = 0, column = 0)
        self.quitButton = tk.Button(self.buttonFrame, text='Quit', highlightbackground = 'gold2', command = self.returnHome)
        self.quitButton.grid(row = 0, column = 1)

    def openHelp(self):
        self.openHelp = tk.Toplevel(self.master)
        self.app = Help(self.openHelp)

    def add_admin(self):
        self.openAdmin = tk.Toplevel(self.master)
        self.app = New_Admin(self.openAdmin)

    def handle_enter(self, label, event):
        label.config(bg = 'gold')

    def handle_leave(self, label, event):  # returns border back to normal
        label.config(bg = 'goldenrod1')

    def track(self, ID):
        plt.style.use('dark_background')
        fig = plt.figure().gca()
        fig.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # displays integers only
        try:
            ID = int(ID)
            val = self.df2.loc[self.df2['AmbassadorID'] == ID].values
            y = [i for i in val[0][1:]]
            plt.title('Ambassador ' + str(ID)+ "'s Meetings")
            plt.xlabel('Week')
            plt.ylabel('Number of Meetings')
            fig.grid(False)
            plt.plot(y)
            plt.show()
        except:
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, 'This Ambassador ID does not exist.')


    def double_click(self, label, event):
        plt.style.use('ggplot')
        # these are different tables on the same excel file
        fig = plt.figure().gca()
        fig.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # displays integers only
        if label.grid_info()['row'] == '0':  #
            x = self.df1.iloc[:, 0]
            y = self.df1.sum(axis = 1)

            plt.title('Cumulative Meetings')
            plt.xlabel('Class')
            plt.ylabel('Number of Meetings')

            plt.bar(x,y)
            plt.show()

        else:
            x = self.df2.iloc[:, 0]
            y = self.df2.iloc[:, 1:len(self.df2.columns)].sum(axis = 1)  # slicing doesn't include last value

            plt.title('Cumulative Ambassador Meetings')
            plt.xlabel('Ambassador ID')
            plt.ylabel('Number of Meetings')

            plt.bar(x,y)
            plt.show()

    def checkValid(self):  # validates all fields
        self.valid = True
        self.specificError = ''

        self.forename = self.forenameEntry.get()
        self.surname = self.surnameEntry.get()
        self.password = self.passwordEntry.get()
        if len(self.forename) == 0 or len(self.surname) == 0 or len(self.password) == 0:
            self.valid = False

        self.gender = ''
        if self.genderVar.get() == 1:
            self.gender = 'Male'
        elif self.genderVar.get() == 2:
            self.gender = 'Female'
        else:
            self.valid = False

        self.yearGroup = self.yearList.get(tk.ANCHOR)  # checks something is selected
        if self.yearGroup not in self.all_year_groups:
            self.valid = False

        self.email = self.emailEntry.get()
        self.emailError = ''
        if '@dulwich-shanghai.cn' not in self.email:
            self.emailError = ', using a valid school email.'
            self.valid = False

        self.photoFilename = self.photoEntry.get()
        if '.png' not in self.photoFilename:
            if self.gender == 'Male':
                self.photoFilename = 'boy.png'  # a default, photo not so important
            elif self.gender == 'Female':
                self.photoFilename = 'girl.png'

        if self.valid:
            self.addAmbassador()
        else:
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, "Some fields you entered were empty or invalid. Please try again" + self.emailError)

    def addAmbassador(self):
        dbCursor.execute('''INSERT INTO TechAmbassadors (Forename, Surname, Gender, YearGroup, Email, Photo) VALUES (?,?,?,?,?,?)''', (self.forename, self.surname, self.gender, self.yearGroup, self.email, self.photoFilename))
        dbCursor.execute('''INSERT INTO AmbassadorAvailability (AmbassadorID, BeforeSchool, Breaktime, Lunchtime, AfterSchool) VALUES (?,?,?,?,?)''', (dbCursor.lastrowid, 'NNNNN', 'NNNNN', 'NNNNN', 'NNNNN'))
        dbCursor.execute('''INSERT INTO TempAmbassadorAvailability (AmbassadorID, BeforeSchool, Breaktime, Lunchtime, AfterSchool) VALUES (?,?,?,?,?)''', (dbCursor.lastrowid, 'NNNNN', 'NNNNN', 'NNNNN', 'NNNNN'))
        # dbCursor.lastrowid gets the primary key of the last inserted element by an instant of the cursor. Ensures there are no clashes/misallocations
        self.encodedPassword = self.password.encode()  # encodes the string into bytes that can be accepted
        self.result = hashlib.sha224(self.encodedPassword)  # sent to SHA224, secure hashing algorithm
        self.encryptedPassword = str(self.result.hexdigest())  # returns the encoded data in hexadecimal format
        dbCursor.execute('''INSERT INTO TAPass (AmbassadorID, Password) VALUES (?,?)''', (dbCursor.lastrowid, self.encryptedPassword))
        dbConnection.commit()

        self.addCounter = 9999999
        # self.addCounter is an absurdly high number to ensure the TA is added to the very end of the dataframe
        # once the page is open again, the indexes are reset anyway
        self.df2.loc[self.addCounter] = [dbCursor.lastrowid] + [0 for i in range(len(self.df2.columns) - 1)]  # adds ambassador to top; fills all columns with 0
        self.df2.index = self.df2.index + 1  # increments the automatic index
        self.df2 = self.df2.sort_index()

        self.write_to_excel(self.oldFileName)
        self.addCounter += 1  # to make sure adding 2 ambassadors at once doesn't clash

        self.openSuccess = tk.Toplevel(self.master)
        self.app = Success(self.openSuccess, self.forename + ' has been added to the database. Remember to tell them their password!')

    def delete_from_file(self):  # deletes from file, same as ambassador hub check_exists()
            with open(r"Fixed Meeting Times.txt", "r") as file_to_read:
                #find_lines = file_to_read.readlines()  # reads all the lines in the file

                find_lines = [i for i in file_to_read.readlines() if i != '\n']
                existing_fixed = [ID[0] for ID in find_lines if ID[0].isnumeric()]  # gets all IDs of fixed meetings into an array
                file_to_read.close()
                try:
                    existing_index = existing_fixed.index(str(self.entered_ID)) * 2  # finds the index of the ID in the array
                    # multiplied by 2 as the index is always on an even row, and the array on the odds
                    with open(r"Fixed Meeting Times.txt", "w") as file_to_write:
                        find_lines = find_lines[:existing_index] + find_lines[(existing_index + 2):]
                        # overwrites the file with everything before and everything after
                        file_to_write.writelines(find_lines)  # If you make a new availability it removes your fixed availability
                        file_to_write.close()
                except ValueError:  # if no fixed schedule was made for that ambassador: existing_index does not return an int
                    return

    def deleteAmbassador(self):
        self.entered_ID = self.IDEntry.get()
        try:
            self.entered_ID = int(self.entered_ID)
            self.checkStudent = dbCursor.execute("SELECT EXISTS(SELECT AmbassadorID FROM TechAmbassadors WHERE AmbassadorID = ?)", (self.entered_ID,))
            for e in dbCursor.fetchone(): # checks ambassador exists, returns either one or zero
                if e == 0:
                    self.openReject = tk.Toplevel(self.master)
                    self.app = Reject(self.openReject, "This Ambassador ID was not found in our database. Please try again.")
                else:
                    dbCursor.execute('''DELETE FROM TechAmbassadors WHERE AmbassadorID = ?''', (self.entered_ID,))
                    dbCursor.execute('''DELETE FROM TAPass WHERE AmbassadorID = ?''', (self.entered_ID,))
                    dbCursor.execute('''DELETE FROM AmbassadorAvailability WHERE AmbassadorID = ?''', (self.entered_ID,))
                    dbCursor.execute('''DELETE FROM TempAmbassadorAvailability WHERE AmbassadorID = ?''', (self.entered_ID,))
                    dbConnection.commit()

                    # removing from spreadsheet
                    self.df2 = self.df2[self.df2.AmbassadorID != self.entered_ID]  # keeps everything except the deleted index
                    self.write_to_excel(self.oldFileName)

                    self.delete_from_file()

                    self.openSuccess = tk.Toplevel(self.master)
                    self.app = Success(self.openSuccess, "This Ambassador has successfully been deleted")
        except ValueError:  # checks the user inputted an integer
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, "Ambassador IDs must be integers, please try again.")

    def excelExport(self):
        # exported to excel before data is deleted
        # add count for each class in Meetings worksheet
        classes = ["7A", "7B", "8A", "8B", "9A", "9B", "10A", "10B", "11A", "11B", "12A", "12B", "13A", "13B"]
        classes_with_meetings = []
        classCount = [0] * 14  # automatically 0 for all 14 classes

        dbCursor.execute("SELECT COUNT(*), Class FROM currentStudents GROUP BY Class")
        for class_and_counter in dbCursor.fetchall():
            classes_with_meetings.append(class_and_counter)
            # creates an array of classes that booked meetings and how many each
        for formClassIndex, formClass in enumerate(classes):  # CHANGED
            for e in classes_with_meetings:
                if e[1] == classes[formClassIndex]:  # if the name of the class is in the classes array
                    classCount[formClassIndex] = e[0]  # replace 0 with the number of meetings for that class

        self.df1[self.columnName] = classCount

        # new column for ambassadors
        allAmbassadorIDs = []
        allAmbassadorCounts = []
        dbCursor.execute("SELECT COUNT(*) FROM TechAmbassadors")  # retrieves number of Ambassadors
        for num in dbCursor.fetchall():
            allAmbassadorCounts = [0] * num[0]  # num is a tuple, e.g. (6,) so num[0] gets the number of meetings
            dbCursor.execute("SELECT AmbassadorID FROM TechAmbassadors")
            for e in dbCursor.fetchall():
                allAmbassadorIDs.append(e[0])

        dbCursor.execute("SELECT COUNT(*), AmbassadorID FROM Meetings GROUP BY AmbassadorID")
        ambassadors_with_meetings = []
        for count_and_ID in dbCursor.fetchall():
            ambassadors_with_meetings.append(count_and_ID)

        for ID in range(len(allAmbassadorIDs)):
            for count_and_ID in ambassadors_with_meetings:
                if count_and_ID[1] == allAmbassadorIDs[ID]:
                    allAmbassadorCounts[ID] = count_and_ID[0]

        self.df2[self.columnName] = allAmbassadorCounts  # df2.index is number of rows
        self.write_to_excel(self.newFileName)
        self.resetWeek()

    def resetWeek(self):
        dbCursor.execute("SELECT AmbassadorID, BeforeSchool, Breaktime, Lunchtime, AfterSchool FROM TempAmbassadorAvailability")
        for ambassador in dbCursor.fetchall():
            dbCursor.execute("UPDATE AmbassadorAvailability SET BeforeSchool = ?, Breaktime = ?, Lunchtime = ?, AfterSchool = ? WHERE AmbassadorID = ?",
                             (ambassador[1], ambassador[2], ambassador[3], ambassador[4], ambassador[0]))
            dbCursor.execute("UPDATE TempAmbassadorAvailability SET BeforeSchool = ?, Breaktime = ?, Lunchtime = ?, AfterSchool = ? WHERE AmbassadorID = ?",
                             ('NNNNN', 'NNNNN', 'NNNNN', 'NNNNN', ambassador[0]))

        with open(r"Fixed Meeting Times.txt", "r") as file:  # updates fixed availabilities
            indexes_and_availabilities = [thing[:-1] for thing in file.readlines()]  # gets rid of \n
            ambIndex = ''
            for i in indexes_and_availabilities:
                if not i.isnumeric():
                    new = i.replace('[','').replace('\'','').replace(']','')
                    dbCursor.execute("UPDATE AmbassadorAvailability SET BeforeSchool = ?, Breaktime = ?, Lunchtime = ?, AfterSchool = ? WHERE AmbassadorID = ?",
                                     (new.split(", ")[0], new.split(", ")[1], new.split(", ")[2], new.split(", ")[3], ambIndex))

                else:
                    ambIndex = i
            dbConnection.commit()
            file.close()

        dbCursor.execute("DELETE FROM Meetings")  # simply deletes all meetings
        dbCursor.execute("DELETE FROM CurrentStudents")
        dbConnection.commit()

        self.openSuccess = tk.Toplevel(self.master)
        self.app = Success(self.openSuccess, "The week has reset." +
                           "\n\nLast week's meetings, students and availabilities have been removed from the database. Download the excel file for a cumulative summary")

    def returnHome(self):
        self.master.destroy()

    def write_to_excel(self, filename):
        with pd.ExcelWriter(filename) as writer:
            self.df1.to_excel(writer, sheet_name='Meetings', index = False)  # this is the file name it saves to
            self.df2.to_excel(writer, sheet_name='Ambassadors', index = False)
