import tkinter as tk
import calendar  # get relevant dates
import datetime  # get current time
import smtplib  # socket for email
import email.message  # HTML email formatting
from socket import gaierror  # common email error: getAddrInfo()
import sqlite3  # database operations

from Validation import Reject, Success

dbConnection = sqlite3.connect('AmbassadorDatabase3.db')  # Passes name of the database to connect() method
dbCursor = dbConnection.cursor()  # Create cursor object using the connection returned from connect method


class BookMeeting:
    def __init__(self, master, ID, name, text, date = '', day='', time=''):
        self.master = master
        self.ID = ID
        self.TAname = name
        self.text = text
        self.date = date
        self.day = day
        self.time = time

        self.master.config(bg = 'salmon1')
        self.frame = tk.Frame(self.master)
        self.master.title('Confirm Booking')
        self.master.geometry('510x400')

        self.Title = tk.Label(self.master, text = self.text, wraplength = 500, font = ('Arial', 20,'bold'), bg = 'salmon1')
        self.Title.grid(row = 0, column = 0, sticky = 'n')

        self.sendText = tk.Label(self.master, text = self.date, bg = 'salmon1', font = ('Arial', 18,'italic'))
        self.sendText.grid(row = 1, column = 0)

        self.entryFrame = tk.Frame(self.master, bg = 'salmon1')
        self.entryFrame.grid(row = 2, column = 0)

        self.nametext = tk.Label(self.entryFrame, text = 'First Name', bg = 'salmon1')
        self.nametext.grid(row = 0, column = 0)
        self.nameEntry = tk.Entry(self.entryFrame, highlightbackground = 'salmon1')
        self.nameEntry.grid(row = 0, column = 1)

        self.surnametext = tk.Label(self.entryFrame, text = 'Surname', bg = 'salmon1')
        self.surnametext.grid(row = 1, column = 0)
        self.surnameEntry = tk.Entry(self.entryFrame, highlightbackground = 'salmon1')
        self.surnameEntry.grid(row = 1, column = 1)

        self.classtext = tk.Label(self.entryFrame, text = 'Class', bg = 'salmon1')
        self.classtext.grid(row = 2, column = 0)
        self.classList = tk.Listbox(self.entryFrame)
        self.classList.insert(tk.END)
        for i in ["7A", "7B", "8A", "8B", "9A", "9B", "10A", "10B", "11A", "11B", "12A", "12B", "13A", "13B"]:
            self.classList.insert(tk.END, i)
        self.classList.grid(row = 2, column = 1)
        # self.classEntry = tk.Entry(self.entryFrame, highlightbackground = 'medium spring green')
        # self.classEntry.grid(row = 1, column = 1)

        self.emailtext = tk.Label(self.entryFrame, text = 'Email', bg = 'salmon1')
        self.emailtext.grid(row = 3, column = 0)

        self.emailEntry = tk.Entry(self.entryFrame, highlightbackground = 'salmon1')
        self.emailEntry.grid(row = 3, column = 1)

        self.buttonFrame = tk.Frame(self.master, bg = 'salmon1')
        self.buttonFrame.grid(row = 3, column = 0)

        self.submit = tk.Button(self.buttonFrame, text = 'Book', highlightbackground = 'salmon1', command = self.sendEmail)
        self.submit.grid(row = 0, column = 0)

        self.homeButton = tk.Button(self.buttonFrame, text = 'Quit', highlightbackground ='salmon1', command = self.returnHome)
        self.homeButton.grid(row = 0, column = 1)

        self.entryFrame.grid_rowconfigure(1, minsize=30)

    def returnHome(self):
        self.master.destroy()

    def sendEmail(self):
        self.studentName = self.nameEntry.get()
        self.formClass = self.classList.get(tk.ACTIVE)
        self.studentEmail = self.emailEntry.get()
        self.surname = self.surnameEntry.get()

        if '@dulwich-shanghai.cn' in self.studentEmail:  # simple way to check it is correctly formatted
            self.requestedTime = [self.day, self.time]
            self.getEmail = dbCursor.execute('''SELECT Email FROM TechAmbassadors WHERE AmbassadorID = ?''', (self.ID,))
            for e in self.getEmail.fetchone():
                self.TAemail = e

            self.msg = email.message.Message()
            self.msg['Subject'] = 'Tech Ambassador Appointment'
            self.msg['From'] = 'TATest11@outlook.com'
            self.recipients = [self.studentEmail, self.TAemail]
            self.msg.add_header('Content-Type','text/html')
            self.msg.set_payload("""Dear {name},
                <br> You have booked an appointment with the Tech Ambassador <b>{TAforename}</b> at this time slot: {requestedTime}.
                <br> Your meeting will take place on <b>{date}</b>. </br>
                
                <br><b>Please do not respond to this email.</b></br>
                <br><b>Have a great meeting,</br></b>
                <b>The Tech Ambassadors</b>
                """.format(name=self.studentName, requestedTime=self.requestedTime, TAforename=self.TAname, date = self.date))

            self.DayToIndex = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
            try:  # Send the message via local SMTP server.
                self.server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                type(self.server)
                self.server.ehlo()  # 'extended HELO', identifies itself to the email server
                self.server.starttls()  # begin a secure TLS connetion with server
                self.server.login('TATest11@outlook.com', 'BigTest123')
                self.server.sendmail(self.msg['From'], self.recipients, self.msg.as_string())
                self.server.quit()

                unchangedDay = dbCursor.execute("SELECT %s FROM AmbassadorAvailability WHERE AmbassadorID = ?" %(self.time), (self.ID,))
                # markers like ? cannot be used for column names
                for i in unchangedDay.fetchone():
                    self.index = self.DayToIndex[self.day]  # e.g. Monday = 0, Tuesday = 1
                    self.dayList = list(i)  # returns their availability in the form ['Y', 'N', 'Y'...]
                    self.dayList[self.index] = 'N'  # makes the time at that index value with a N
                    self.dayList = ','.join(self.dayList).replace(',','')

                    self.updateDay = dbCursor.execute("UPDATE AmbassadorAvailability SET %s = ? WHERE AmbassadorID = ?"
                                                      %(self.time), (self.dayList, self.ID))

                    self.checkStudent = dbCursor.execute("SELECT EXISTS(SELECT Forename, Surname, Class FROM CurrentStudents WHERE Forename = ? "\
                                                         "AND Surname = ? AND Class = ?)",
                                                         (self.studentName, self.surname, self.formClass))
                    # checks student exists, returns either one or zero
                    for e in dbCursor.fetchone():
                        if e == 0: # if student hasn't yet booked a meeting this week
                            dbCursor.execute('''INSERT INTO CurrentStudents (Forename, Surname, Class, Email) VALUES(?,?,?,?)''',
                                             (self.studentName, self.surname, self.formClass, self.studentEmail))
                            dbCursor.execute('''SELECT StudentID FROM CurrentStudents WHERE Forename = ? AND Surname = ? AND Class = ? AND Email = ?''',
                                             (self.studentName, self.surname, self.formClass, self.studentEmail))
                            for ID in dbCursor.fetchone():
                                self.studentID = ID
                            dbConnection.commit()
                        else:
                            dbCursor.execute("SELECT StudentID FROM CurrentStudents WHERE Forename = ? AND Surname = ? AND Class = ?",
                                             (self.studentName, self.surname, self.formClass))
                            for ID in dbCursor.fetchone():
                                self.studentID = ID
                            # these are the only variables that are not static, they can change.
                            dbConnection.commit()

                    self.addMeeting = dbCursor.execute('''INSERT INTO Meetings (StudentID, AmbassadorID, MeetingTime) VALUES (?,?,?)''',
                                                       (int(self.studentID), int(self.ID), str(self.requestedTime)))
                    dbConnection.commit()
                    self.openSuccess = tk.Toplevel(self.master)
                    self.app = Success(self.openSuccess, 'Email successfully sent, you have booked an appointment.')

            # note, program won't work in school, school has blocked email sending. Will have to contact admin. Also, SMTP has issues over a VPN, will have to sort this out.

            except (gaierror, ConnectionRefusedError):
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "Failed to connect to the server. Most likely a bad connection. Appointment could not be booked, please try again.")
            except smtplib.SMTPServerDisconnected:
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "'Failed to connect to the server. Wrong username/password? Appointment could not be booked, please try again.")
            except smtplib.SMTPException as e:
                self.openReject = tk.Toplevel(self.master)
                self.app = Reject(self.openReject, "Appointment could not be booked, please try again.")
        else:
            self.openReject = tk.Toplevel(self.master)
            self.app = Reject(self.openReject, "Invalid email address, please try again with your school email.")
