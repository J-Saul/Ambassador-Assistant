import tkinter as tk  # create basic Graphical User Interface elements
from PIL import ImageTk, Image  # display images on Tkinter widgets

from Choose_Page import ChoosePage
from Cancellations import CancelLogin
from Login_Pages import TALoginPage, AdminLoginPage


class LoginHub:
    def __init__(self, master):  # passes the root window as a parameter called master
        self.master = master
        self.master.geometry('610x420')  # the dimensions of the page
        self.bgColour = 'LightBlue2'
        self.master.config(bg = self.bgColour)  # sets the background colour
        self.master.title("Ambassador Assistant")  # the name of the window

        self.label = tk.Label(self.master, text='Welcome to the Ambassador Assistant',
                              font = ('Arial', 28,'bold'), bg = self.bgColour)  # creates a label
        self.label.grid(row=0, column=0)  # puts the label on the page
        self.subtitle = tk.Label(self.master, text='What would you like to do today?',
                                 font = ('Arial', 17, 'italic'), bg = self.bgColour)
        self.subtitle.grid(row=1, column=0)

        self.labelFrame = tk.Frame(self.master, bg=self.bgColour)
        # makes a tkinter frame; a place to put widgets in, a mini-window unaffected by settings on the rest of the page
        self.labelFrame.grid(row=2, column=0)
        self.studentLabel = tk.Label(self.labelFrame, text = 'Students', font = ('Arial', 16,'bold'), bg = self.bgColour)
        self.ambassadorLabel = tk.Label(self.labelFrame, text = 'Ambassadors', font = ('Arial', 16,'bold'), bg = self.bgColour)
        self.adminLabel = tk.Label(self.labelFrame, text = 'Admin', font = ('Arial', 16,'bold'), bg = self.bgColour)
        self.studentLabel.grid(row = 2, column = 0)
        self.ambassadorLabel.grid(row = 3, column = 0)
        self.adminLabel.grid(row = 4, column = 0)

        self.studentFrame = tk.Frame(self.labelFrame, width = 50, bg = self.bgColour)
        self.studentFrame.grid(row = 2, column = 1)
        self.bookAppointment = tk.Button(self.studentFrame, text = 'Book Appointment', width = 20,
                                         highlightbackground=self.bgColour, command = self.openChoosePage)
        self.bookAppointment.grid(row = 0, column = 0)

        self.cancelAppointment = tk.Button(self.studentFrame, text = 'Cancel Appointment', width = 20,
                                           highlightbackground=self.bgColour, command = self.openCancelPage)
        self.cancelAppointment.grid(row = 0, column = 1)

        self.ambassadorLogin = tk.Button(self.labelFrame, text = 'Login', width = 43, highlightbackground=self.bgColour, command = self.TALogin)
        self.ambassadorLogin.grid(row = 3, column = 1)
        self.adminLogin = tk.Button(self.labelFrame, text = 'Login', width = 43, highlightbackground=self.bgColour, command = self.adminLogin)
        self.adminLogin.grid(row = 4, column = 1)

        self.photoFrame = tk.Frame(self.master, bg = self.bgColour)
        self.photoFrame.grid(row = 3, column = 0)

        self.myPhoto = 'TALogo.png'  # retrieves the name of the file
        self.im = Image.open(self.myPhoto)
        self.photo = ImageTk.PhotoImage(self.im)
        self.label = tk.Label(self.photoFrame, image = self.photo, bg=self.bgColour)
        self.label.image = self.photo
        self.label.grid()

        self.master.protocol("WM_DELETE_WINDOW", self.master.quit())  # closes all windows if close button pressed

    def openChoosePage(self):
        self.openChoosePage = tk.Toplevel(self.master)
        # creates a new Toplevel window with the same root (self.master)
        self.app = ChoosePage(self.openChoosePage)
        # Opens ChoosePage, with the window as a parameter (because it is the new root)

    def openCancelPage(self):
        self.openCancelPage = tk.Toplevel(self.master)  # opens first top level window
        self.app = CancelLogin(self.openCancelPage)

    def TALogin(self):
        self.TALogin = tk.Toplevel(self.master)
        self.app = TALoginPage(self.TALogin)

    def adminLogin(self):  # both functions use the same login page, but inheritance involved for admin
        self.adminLogin = tk.Toplevel(self.master)
        self.app = AdminLoginPage(self.adminLogin)


# ===== run mainloop =====

def main():
    root = tk.Tk()
    # creates the root window- the application's main window
    window1 = LoginHub(root)
    root.mainloop()
    # a method that loops until the user exits the program, executing the main window


if __name__ == '__main__':
    main()


#  changes when porting to new system:
#  1) the file path all excel spreadsheets are saved to
