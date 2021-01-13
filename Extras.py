import tkinter as tk


class Help:
    def __init__(self, master):
        self.master = master
        self.master.title("Troubleshooting")
        self.master.geometry('500x360')
        self.master.config(bg = 'cyan')
        self.title = tk.Label(self.master, text = "Troubleshooting", bg = 'cyan', width = 25, font = ('Arial', 18, 'bold'))
        self.title.grid(row = 0, column = 0)
        self.subtitle = tk.Label(self.master, text = "Version 1.0 \n", bg = 'cyan', font = ('Arial', 14, 'italic'))
        self.subtitle.grid(row = 1, column = 0)

        self.container = tk.Frame(self.master)
        self.container.grid(row = 2, column = 0)
        self.canvas = tk.Canvas(self.container, width = 450, height = 250, bg = 'cyan')
        self.scrollbar = tk.Scrollbar(self.container, orient = 'vertical', command = self.canvas.yview)
        self.scrollableFrame = tk.Frame(self.canvas, bg = 'cyan', relief = 'sunken')
        self.scrollableFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window = self.scrollableFrame, anchor = tk.NW)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.TRUE)
        self.scrollbar.pack(side = tk.RIGHT, fill = 'y')

        self.emailTitle = tk.Label(self.scrollableFrame, bg = 'cyan', text = "Emails aren't sending or are lagging out", font = ('Arial', 16, 'bold'))
        self.emailTitle.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)
        self.emailHelp = tk.Label(self.scrollableFrame, bg = 'cyan', wraplength = 350, text = "This is likely a school server error, because of the firewall. Ask IT to allow emails to be sent from TATest11@outlook.com, or make a new account and make that the new sender (line 548)")
        self.emailHelp.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.email_not_sending = tk.Label(self.scrollableFrame, bg = 'cyan', text = "\n Emails aren't arriving at students inbox", font = ('Arial', 16, 'bold'))
        self.email_not_sending.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)
        self.email_not_sending_help = tk.Label(self.scrollableFrame, bg = 'cyan', wraplength = 350, text = "This is probably because the emails are being sent straight to junk, or the student entered the wrong email address. First check the database to see the email is correct, if so, ask IT to allow this email address to be authenticated.")
        self.email_not_sending_help.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.incorrect_excel_files = tk.Label(self.scrollableFrame, bg = 'cyan', text = "\n The excel files are all wrong", font = ('Arial', 16, 'bold'))
        self.incorrect_excel_files.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)
        self.incorrect_excel_files_help = tk.Label(self.scrollableFrame, bg = 'cyan', wraplength = 350, text = "Yikes, this could be a mess. It's likely the dates that are all messed up. Remember to reset the week at THE END OF FRIDAY and don't do anything else until Monday! Email me the most recent excel file, database file and code; I'll see what I can do")
        self.incorrect_excel_files_help.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.page_not_opening = tk.Label(self.scrollableFrame, bg = 'cyan', text = "\n Pages are not opening properly and the \n rejection page is opening even for valid entry", font = ('Arial', 16, 'bold'))
        self.page_not_opening.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)
        self.page_not_opening_help = tk.Label(self.scrollableFrame, bg = 'cyan', wraplength = 350, text = "This is potentially a database error. Check the Python console to see if it's a python error, otherwise check the database itself. \n If the program has been moved to a new computer, it could be that you didn't move all the right files. Ensure the correct database file and all excel files are in the SAME DIRECTORY on pycharm (Mr Whitaker/Mr Forbes will know what that means)")
        self.page_not_opening_help.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.notice = tk.Label(self.scrollableFrame, text = "\n Email jfmsaul@hotmail.com if all else fails! \n", bg = 'cyan', font = ('Arial', 14, 'italic'))
        self.notice.pack()

        self.quitButton = tk.Button(self.master, text = 'Quit', width = 25, highlightbackground='cyan', command = self.close_windows)
        self.quitButton.grid(row = 3, column = 0)

    def close_windows(self):
        self.master.destroy()


class New_Admin:  # future expansion
    def __init__(self, master):
        self.master = master
        self.master.title("Troubleshooting")
        self.master.geometry('500x360')
        self.master.config(bg = 'orange')
        self.title = tk.Label(self.master, text = "Add an admin to the system", bg = 'orange', width = 25, font = ('Arial', 18, 'bold'))
        self.title.grid(row = 0, column = 0)
        self.entryFrame = tk.Frame(self.master, bg = 'orange')
        self.entryFrame.grid(row = 1, column = 0)
        self.ID_label = tk.Label(self.entryFrame, bg = 'orange', text = 'ID', font = ('Arial', 14, 'bold'))
        self.ID_label.grid(row = 0, column = 0)
        self.ID_entry = tk.Entry(self.entryFrame, highlightbackground = 'orange')
        self.ID_entry.grid(row = 0, column = 1)
        self.pass_label = tk.Label(self.entryFrame, bg = 'orange', text = 'Password', font = ('Arial', 14, 'bold'))
        self.pass_label.grid(row = 1, column = 0)
        self.pass_entry = tk.Entry(self.entryFrame, highlightbackground = 'orange', show = '*')
        self.pass_entry.grid(row = 1, column = 1)

        self.returnButton = tk.Button(self.entryFrame, highlightbackground = 'orange', text = 'Quit', command = self.returnHome)
        self.returnButton.grid(row=2, column=1)
        self.submitButton = tk.Button(self.entryFrame, highlightbackground = 'orange', text = 'Help', command = self.submit)
        self.submitButton.grid(row=2, column=0)

    def submit(self):
        pass

    def returnHome(self):
        self.master.destroy()  #
