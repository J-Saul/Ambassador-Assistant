import tkinter as tk  # create basic Graphical User Interface elements


class Reject:  # universally used when the user does anything wrong
    bgColour = 'red'
    title = 'Rejected Entry'

    def __init__(self, master, rejectText):
        self.master = master
        self.master.title(self.__class__.title)
        self.rejectText = rejectText  # reject text is unique for each error, passed as a parameter
        self.master.geometry('300x200')
        self.master.config(bg = self.__class__.bgColour)
        self.label = tk.Label(self.master, text = self.rejectText, bg = self.__class__.bgColour,
                              wraplength = 280, width = 25, font = ('Arial', 14, 'bold'))
        self.label.pack(side = 'top', expand = 'YES', fill = 'both')
        self.quitButton = tk.Button(self.master, text = 'Quit',
                                    width = 25, highlightbackground=self.__class__.bgColour, command = self.close_windows)
        self.quitButton.pack()

    def close_windows(self):
        self.master.destroy()


class Success(Reject):
    bgColour = 'lightgreen'
    title = 'Success'

    def __init__(self, master, successText):
        Reject.__init__(self, master, successText)
        # inherits the reject page, the only difference being the green background colour
