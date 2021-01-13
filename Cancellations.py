import tkinter as tk
import smtplib  # socket for email
import email.message  # HTML email formatting
from socket import gaierror  # common email error: getAddrInfo()
from functools import partial
import sqlite3  # database operations

from Validation import Reject

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class CancelLogin:
    def __init__(self, master):
        self.master = master
        self.master.config(bg ='MediumOrchid1')
        self.master.title('Confirm Booking')
        self.master.geometry('450x250')
        self.Title = tk.Label(self.master, text = " Please enter your email to cancel your email\n", wraplength = 500, font = ('Arial', 20,'bold'), bg = "MediumOrchid1")
        self.Title.grid(row = 0, column = 0, sticky = 'n')

        self.frame = tk.Frame(self.master, bg = 'MediumOrchid1')
        self.frame.grid(row=1, column = 0)

        self.emailtext = tk.Label(self.frame, text = 'Email', bg = 'MediumOrchid1')
        self.emailtext.grid(row = 0, column = 0)
        self.emailEntry = tk.Entry(self.frame, highlightbackground = 'MediumOrchid1')
        self.emailEntry.grid(row = 0, column = 1)

        self.buttonFrame = tk.Frame(self.master, bg = 'MediumOrchid1')
        self.buttonFrame.grid(row = 2, column = 0)

        self.submit = tk.Button(self.buttonFrame, text = 'Submit', highlightbackground = 'MediumOrchid1', command = self.cancelCheck)
        self.submit.grid(row = 0, column = 0)
        self.homeButton = tk.Button(self.buttonFrame, text = 'Quit', highlightbackground = 'MediumOrchid1', command = self.returnHome)
        self.homeButton.grid(row = 0, column = 1)

    def cancelCheck(self):  # only called by the child class
        self.studentEmail = self.emailEntry.get()
        self.checkStudent = dbCursor.execute("SELECT EXISTS(SELECT Email FROM CurrentStudents WHERE Email = ?)", (self.studentEmail,))
        for i in dbCursor.fetchone():
            if i == 1:  # if found
                self.getInfo = dbCursor.execute("SELECT Forename, Surname, Class FROM CurrentStudents WHERE Email = ?", (self.studentEmail,))
                for e in dbCursor.fetchall():
                    dbConnection.commit() # poterror
                    self.openCancelHub = tk.Toplevel(self.master)
                    self.app = CancelHub(self.openCancelHub, e[0], e[1], e[2], self.studentEmail)
            else:
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "We could not find you in our database. Did you make a spelling error?")

    def returnHome(self):
        self.master.destroy()


class CancelHub:
    def __init__(self, master, studentName, surname, formClass, studentEmail):
        self.master = master
        self.studentName = studentName
        self.surname = surname
        self.formClass = formClass
        self.studentEmail = studentEmail
        self.master.title('Cancel Hub')

        self.master.geometry('500x300')
        self.master.config(bg = 'orchid1')
        self.label = tk.Label(self.master, text = ('Hi there, ' + self.studentName + '. Here are the meetings you booked.'), bg = 'orchid1', font = ('Arial', 20, 'bold'), wraplength = 490)
        self.label.grid(row = 0, column = 0)

        self.buffer = tk.Label(self.master, text = (' '), bg = 'orchid1')
        self.buffer.grid(row=1, column=0)

        self.cancelFrame = tk.Frame(self.master, bg = 'orchid1')
        self.cancelFrame.grid(row=2, column=0)

        self.buffer2 = tk.Label(self.master, text = (' '), bg = 'orchid1')
        self.buffer2.grid(row=3, column=0)

        self.returnHome = tk.Button(self.master, text = 'Quit', bg = 'orchid1', highlightbackground = 'orchid1', command = self.returnHome)
        self.returnHome.grid(row=4, column=0)

        def update(meetingID, meetingTime, studentName, surname, formClass, AmbassadorID, labelText, studentEmail):
            # this is the partial function later called
            newText = labelText.replace('[',"").replace(']',"").replace('\'',"")
            newText = newText.split(', ')

            DayToIndex = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
            TimeToIndex = {"BeforeSchool": 0, "Breaktime": 1, "Lunchtime": 2, "AfterSchool": 3}
            newAvailability = ''

            dbCursor.execute('''DELETE FROM Meetings WHERE MeetingID = ?''', (meetingID,))
            dbConnection.commit()

            if self.meetingsCounter == 1:  # if the student only booked one meeting, we know for certain to delete everything
                dbCursor.execute('''DELETE FROM CurrentStudents WHERE Forename = ? AND Surname = ? AND Class = ?''', (studentName, surname, formClass))
                dbConnection.commit()

            # below updates the ambassador Availability (e.g. YYNYN)
            if newText[1] in TimeToIndex:
                if newText[0] in DayToIndex:
                    dayIndex = DayToIndex[newText[0]]  # converts a day to its index (e.g. Wednesday -> 2)
                    dbCursor.execute("SELECT %s FROM AmbassadorAvailability WHERE AmbassadorID = ?" %(newText[1]), (AmbassadorID,))

                    for schedule in dbCursor.fetchall():
                        schedule = "".join(schedule)
                        if dayIndex == 0:  # some string manipulation
                            newAvailability = 'Y' + str(schedule[1:])
                            # everything after target letter
                        elif dayIndex != 4:
                            newAvailability = str(schedule[:dayIndex]) + 'Y' + str(schedule[dayIndex+1:])
                            # everything before target letter, then 'Y' then everything INCLUDING target+1
                        else:
                            newAvailability = str(schedule[:4]) + 'Y'
                            # everything before the final letter, add a Y instead

                    dbCursor.execute("UPDATE AmbassadorAvailability SET %s = ? WHERE AmbassadorID = ?" % (newText[1]), (newAvailability, AmbassadorID))

                else:
                    self.openReject = tk.Toplevel(self.master)
                    self.app = Reject(self.openReject, "Database error. Please contact a Tech Ambassador as soon as possible.")
            else:
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "Database error. Please contact a Tech Ambassador as soon as possible.")

            dbConnection.commit()

            self.label.config(text=' Meeting successfully cancelled. We hope to see you again!', bg = 'lightgreen')
            self.master.config(bg='lightgreen')
            self.buffer.config(bg='lightgreen')
            self.buffer2.config(bg='lightgreen')
            self.cancelFrame.config(bg='lightgreen')
            self.returnHome.config(highlightbackground='lightgreen')
            self.label.grid(row=5)
            self.buffer.grid(row=6)
            self.buffer2.grid(row=7)
            self.returnHome.grid(row=8)

            for meetings in self.widgetArray:  # deletes every widget on the page
                for widget in meetings:
                    widget.grid_forget()

            # ============= send email ==============

            getEmail = dbCursor.execute('''SELECT Forename, Email FROM TechAmbassadors WHERE AmbassadorID = ?''', (AmbassadorID,))
            for forename, TAemail in getEmail.fetchall():
                msg = email.message.Message()
                msg['Subject'] = 'Tech Ambassador Appointment'
                msg['From'] = 'TATest11@outlook.com'
                recipients = [studentEmail, TAemail]
                msg.add_header('Content-Type','text/html')
                msg.set_payload("""Dear {name} {formClass},
                    <br> You have cancelled your appointment with the Tech Ambassador <b>{TAforename}</b> at this time slot: {meetingTime}. Don't worry, {TAforename} has been notified.
                    
                    <br><b>Please do not respond to this email.</b></br>
                    <br><b>We hope to see you again some day,</br></b>
                    <b>The Tech Ambassadors</b>
                    """.format(name=studentName, formClass = formClass, meetingTime=meetingTime, TAforename=forename))

                # Send the message via local SMTP server.

                try:
                    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                    type(server)
                    server.ehlo()
                    server.starttls()
                    server.login('TATest11@outlook.com',
                            'BigTest123')
                    server.sendmail(msg['From'], recipients, msg.as_string())
                    server.quit()

                except (gaierror, ConnectionRefusedError):
                    self.openReject = tk.Toplevel(self.master)
                    self.app = Reject(self.openReject, "Failed to connect to the server. Most likely a bad connection. Appointment could not be booked, please try again.")
                except smtplib.SMTPServerDisconnected:
                    self.openReject = tk.Toplevel(self.master)
                    self.app = Reject(self.openReject, "'Failed to connect to the server. Wrong username/password? Appointment could not be booked, please try again.")
                except smtplib.SMTPException as e:
                    self.openReject = tk.Toplevel(self.master)

        # main loop
        self.getID = dbCursor.execute("SELECT StudentID FROM CurrentStudents WHERE Forename = ? AND Surname = ? AND Class = ?",
                                      (self.studentName, self.surname, self.formClass))
        for ID in dbCursor.fetchone():
            self.studentID = ID
        dbConnection.commit()

        self.allMeetings = dbCursor.execute("SELECT MeetingID, AmbassadorID, MeetingTime FROM Meetings WHERE StudentID = ?", (self.studentID,))
        rowCounter = 3
        self.meetingsCounter = 0
        self.widgetArray = []  # create array, will become a 2D array when we fill with widgets

        for meetingID, AmbassadorID, meetingTime in dbCursor.fetchall():
            self.meetingsCounter += 1
            self.widgetArray.append([])

            self.getAmbassador = dbCursor.execute("SELECT Forename, Surname FROM TechAmbassadors WHERE AmbassadorID = ?", (AmbassadorID,))
            for Forename, Surname in dbCursor.fetchall():
                self.AmbassadorName = Forename + ' ' + Surname

            self.AmbassadorLabel = tk.Label(self.cancelFrame, text = (str(self.AmbassadorName)),
                                            bg = 'orchid1', highlightbackground = 'orchid1', font = ('Arial', 15, 'italic'))
            self.AmbassadorLabel.grid(row = rowCounter, column = 0)
            self.widgetArray[self.meetingsCounter - 1].append(self.AmbassadorLabel)  # adds this widget to 2D array's sub array

            self.cancelTime = tk.Label(self.cancelFrame, text = meetingTime, bg = 'orchid1',
                                       highlightbackground = 'orchid1', font = ('Arial', 15, 'bold'))

            self.button = tk.Button(self.cancelFrame, text = 'Cancel Meeting', highlightbackground = 'orchid1',
                                    command = partial(update, meetingID, meetingTime, self.studentName, self.surname,
                                                      self.formClass, AmbassadorID, self.cancelTime.cget('text'), self.studentEmail))
            # partial functions are higher order: they 'freeze' an object's state.

            self.cancelTime.grid(row = rowCounter, column = 1)
            self.button.grid(row = rowCounter, column = 2)
            self.widgetArray[self.meetingsCounter - 1].append(self.cancelTime)
            self.widgetArray[self.meetingsCounter - 1].append(self.button)

            rowCounter += 1

    def cancel(self, newList, rowCounter):
        self.newList = newList
        self.rowCounter = rowCounter
        self.label.config(text = rowCounter)

    def returnHome(self):
        self.master.destroy()
