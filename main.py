
from PyQt5 import QtCore, QtGui, QtWidgets
import os #for restarting the program


from PyQt5.QtWidgets import QMainWindow #provides a framework for building an application's user interface.
from PyQt5.QtWidgets import QWidget #widget that pretty much all pyqt5 interfaces is based on as the central widget. It is what recieves events (ex. click, keydown)

from PyQt5.QtWidgets import QStatusBar

import requests


class Ui_MainWindow(QMainWindow):
    '''
    QMainWindow Layout
    ______________________________________
   |__Menu Bar____________________________| #dropdown menu selections file, edit, etc
   |_______________ToolBars_______________| #makes buttons that give users access to functions, typcially just visual buttons for menu bar quick access
   |   __________Dock Windows__________   | #creates side view next to the central widget
   |  |                                |  |
   |  |                                |  |
   |  |          Cental Widget         |  | #the main widget, which is almost always QWidget to recieve the user's inputs
   |  |                                |  |
   |  |________________________________|  |
   |______________________________________|
   |___Status Bar_________________________| #can add temperary or permanent messages
    '''
    def __init__(self):
        super().__init__() #initialize the QMainWindow
        self.windowTitleSetter('Example Form') #call to name the default

        self.resize(597, 200) #set default size

        self.makeCentralWidget() #make the central widget and central layout
        self.makeCentralScroll() #calls to make central layout able to scroll
        self.addToCentralScroll() #add the content inside of the scroll area

        #self.makeStatusBar() #call to make status bar
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SET WINDOW TITLE

    def windowTitleSetter(self, title):
        self.setWindowTitle(title)  # name the mainWindow with the specified title

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Central Widget
    def makeCentralWidget(self):
        self.centralWidget = QWidget()  # define qWidget as the central widget, (accepts input)
        self.verticalLayoutForScroll = QtWidgets.QVBoxLayout(self.centralWidget)  # make a verticle layout so the scrollArea widget can be placed in a layout, (needs to be entire, so this will only contain one container)

    # Scroll vert. layout which is actual main layout
    def makeCentralScroll(self):
        self.scrollArea = QtWidgets.QScrollArea(
            self.centralWidget)  # set the central Qwidget to a scroll area which allows for the user to scroll if window is too small
        self.scrollArea.setWidgetResizable(
            True)  # allow for the scroll area to be resized... necessary as adding more into the scroll area
        # now there a scroll area inside of the uppermost vertical layout that will recieve input scroll input from central widget, Qwidget

        self.scrollAreaWidgetContents = QtWidgets.QWidget()  # defining what is in scroll area... which is the QWidget, which accepts user input, however Qwidget still has to be defined as central above to receive user input for the scroll
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 577, 207))  # set intial geometry of scroll area

        self.mainVerticalLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)  # now need to put not technically the main layout, but the layout everything is going to be placed in since everything has to be inside the scroll area.

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ADD TO SCROLL CONTENTS
    def addToCentralScroll(self):
        # now add the contents to the mainVert.layout
        self.nameInput()  # add name input line
        self.ageInput()  # add age
        self.addScrollContentsToScrollWidget()  # updates the contents from the object to the widget

        self.makeSubmitButton()

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SCROLL CONTENTS
    # NAME INPUT
    def nameInput(self):
        self.horizontalNameLayout = QtWidgets.QHBoxLayout()  # make a new horizontal layout

        self.label = QtWidgets.QLabel('Name: ', self.scrollAreaWidgetContents)  # make a new label
        self.horizontalNameLayout.addWidget(self.label)  # add it to the name vert layout

        self.nameInputLine = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)  # make a new line edit
        self.horizontalNameLayout.addWidget(self.nameInputLine)  # add it to horizontal name layout

        self.mainVerticalLayout.addLayout(self.horizontalNameLayout)  # add the name horizontal layout to the vertical layout so it looks like... T - top is horizontal, downwards part is vertical layout

    #ADD AGE
    def ageInput(self):
        self.horizontalAgeLayout = QtWidgets.QHBoxLayout()  # make a new horizontal layout

        self.ageLabel = QtWidgets.QLabel('Age: ', self.scrollAreaWidgetContents)  # make a new label
        self.horizontalAgeLayout.addWidget(self.ageLabel)  # add it to the name vert layout

        self.ageBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)  # make a new line edit
        self.horizontalAgeLayout.addWidget(self.ageBox)  # add it to horizontal name layout

        self.mainVerticalLayout.addLayout(self.horizontalAgeLayout)  # add the name horizontal layout to the vertical layout so it looks like... T - top is horizontal, downwards part is vertical layout

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #SCROLL SETTER THAT ADDS CONTENTS TO WIDGET
    def addScrollContentsToScrollWidget(self):
        self.scrollArea.setWidget(self.scrollAreaWidgetContents) #add the contents (ex. buttons, line edit) to the scroll area
        self.verticalLayoutForScroll.addWidget(self.scrollArea) #add the scroll area to the veritcal layout
        self.setCentralWidget(self.centralWidget) #now that scroll has its contents, contents need to interact and receive input, so set the central widget to Qwidget

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #STATUS BAR
    #MAKE STATUS BAR
    def makeStatusBar(self):
        self.statusbar = QStatusBar() #makes a new object that an instance of QStatusBar

        self.statusBarSetter() #call to set the status bar

    #STATUS BAR SETTER
    def statusBarSetter(self):
        self.setStatusBar(self.statusbar) #sets the object to the status bar

    #------------------------------------
    #SUBMIT BUTTON AT BOTTOM
    def makeSubmitButton(self):
        self.submitButton = QtWidgets.QPushButton('Submit', self.scrollAreaWidgetContents) #make a new button
        self.submitButton.clicked.connect(lambda: self.storeData()) #call to store data if its clicked
        self.mainVerticalLayout.addWidget(self.submitButton)#add ot to the main layout

    #Store data that the button calls
    def storeData(self):
        name = self.nameInputLine.text()
        age = self.ageBox.value()

        print(name)
        print(age)
        #try:
        url = "http://127.0.0.1:5000/people"
        data = {
            'name':name,
            'age':age
        }
        response = requests.post(url, json=data)
        message = name + " has been added to the database."
        self.statusBar().showMessage(message, 5000)
        '''
        except:
            message = "There was an Error. The server is most likely down."
            self.statusBar().showMessage(message, 5000)
        '''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv) #make an instance of the application
    ui = Ui_MainWindow() #make an instance of the ui
    ui.show()
    sys.exit(app.exec_())