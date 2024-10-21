#http://api.openweathermap.org/geo/1.0/zip?zip=E14,GB&appid={API key}


import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import requests
import json
import re

import WeatherAPIRequest_v01 as weather

# handle character encoding
sys.stdout.reconfigure(encoding="utf-8")

# Window for all weather settings
class WeatherSettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, dashboard):
        super().__init__()
        print("Weather settings")
        self.dashboard = dashboard
        self.setWindowTitle("Weather Settings")
        self.setGeometry(200, 200, 300, 200)

        self.geoLocation = GeoLocation()
        self.weatherRequester = weather.WeatherAPIRequest()
        self.searchByCity = None
        #self.weatherRequester = None
        self.createWidgets()
        self.createLayouts()
        self.connectUI()

    def createWidgets(self):
        # Container for
        self.appIDInputArea = QtWidgets.QWidget()#input stuff
        self.appIDInputArea.setAutoFillBackground(True)
        inputPalette = QtGui.QPalette()
        inputPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(70, 70, 70))
        self.appIDInputArea.setPalette(inputPalette)

        self.appIDLabel = QtWidgets.QLabel("App ID")
        self.appIDInput = QtWidgets.QLineEdit()
        self.appIDInput.setText(self.geoLocation.checkExistingID())

        self.locationLabel = QtWidgets.QLabel("Location")
        self.locationInput = QtWidgets.QLineEdit()
        self.locationInput.setText("Enter City or Zipcode")

        self.locationSearchButton = QtWidgets.QPushButton("Search")
        self.locationChoiceButton1 = QtWidgets.QPushButton("")
        self.locationChoiceButton1.setVisible(False)
        self.locationChoiceButton2 = QtWidgets.QPushButton("")
        self.locationChoiceButton2.setVisible(False)
        self.locationChoiceButton3 = QtWidgets.QPushButton("")
        self.locationChoiceButton3.setVisible(False)
        self.locationChoiceButton4 = QtWidgets.QPushButton("")
        self.locationChoiceButton4.setVisible(False)
        self.locationChoiceButton5 = QtWidgets.QPushButton("")
        self.locationChoiceButton5.setVisible(False)
        self.locationChoiceButtonList = [
            self.locationChoiceButton1,
            self.locationChoiceButton2,
            self.locationChoiceButton3,
            self.locationChoiceButton4,
            self.locationChoiceButton5,
        ]

        self.appIDButtonArea = QtWidgets.QWidget()#button stuff
        self.appIDButtonArea.setAutoFillBackground(True)
        buttonPalette = QtGui.QPalette()
        buttonPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 50, 50))
        self.appIDButtonArea.setPalette(buttonPalette)
        self.appIDSubmitButton = QtWidgets.QPushButton("Submit")

    def createLayouts(self):
        self.weatherInputLayout = QtWidgets.QVBoxLayout()
        self.weatherInputLayout.addWidget(self.appIDLabel)
        self.weatherInputLayout.addWidget(self.appIDInput)
        self.weatherInputLayout.addWidget(self.locationLabel)
        self.weatherInputLayout.addWidget(self.locationInput)
        self.weatherInputLayout.addWidget(self.locationSearchButton)
        self.weatherInputLayout.addWidget(self.locationChoiceButton1)
        self.weatherInputLayout.addWidget(self.locationChoiceButton2)
        self.weatherInputLayout.addWidget(self.locationChoiceButton3)
        self.weatherInputLayout.addWidget(self.locationChoiceButton4)
        self.weatherInputLayout.addWidget(self.locationChoiceButton5)
        self.appIDInputArea.setLayout(self.weatherInputLayout)

        self.appIDButtonLayout = QtWidgets.QHBoxLayout()
        self.appIDButtonLayout.addWidget(self.appIDSubmitButton)
        self.appIDButtonArea.setLayout(self.appIDButtonLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.mainLayout.addWidget(self.appIDInputArea)
        self.mainLayout.addWidget(self.appIDButtonArea)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def connectUI(self):
        self.appIDSubmitButton.clicked.connect(lambda: self.submitAppID())
        self.locationInput.textChanged.connect(lambda: self.validate_input())
        self.locationSearchButton.clicked.connect(lambda: self.submitLocation())#self.searchByCity
    
    def validate_input(self):
        text = self.locationInput.text().strip()
        
        if self.isZipCode(text):
            #self.result_label.setText(f"'{text}' is a valid ZIP code.")
            print("Valid Zip")
            self.searchByCity = False
        elif self.isCityName(text):
            #self.result_label.setText(f"'{text}' is a valid city name.")
            print("valid City")
            self.searchByCity = True
        else:
            print("Invalid Input")
            self.searchByCity = None

    def isZipCode(self, text):
        return bool(re.match(r'^\d{5}(-\d{4})?$', text))  # Matches 5-digit ZIP code and optional 4-digit extension

    def isCityName(self, text):
        # Here you can define a list of valid city names or a regex for validation
        # For simplicity, let's just check if it contains only letters and spaces
        return bool(re.match(r'^[A-Za-z\s]+$', text))

    def submitAppID(self):
        self.appIDString = self.appIDInput.text()
        if not self.appIDString:
            print("no id!")

        self.geoLocation.setAppID(self.appIDInput.text())
    
    def submitLocation(self):#byCity
        if self.searchByCity:
            self.geoLocation.byCity(self.locationInput.text())
            self.createLocationChoiceMenu(self.geoLocation.buttonNames)
        elif self.searchByCity == False:
            self.geoLocation.byZipcode(self.locationInput.text())
            self.createLocationChoiceMenu(self.geoLocation.buttonNames)
        elif self.searchByCity == None:
            self.locationInput.setText("Invalid Search")
        #self.createLocationChoiceMenu(self.geoLocation.buttonNames)

    def createLocationChoiceMenu(self, incomingList):
        incomingList = self.geoLocation.buttonNames
        
        for button, text in zip(self.locationChoiceButtonList, incomingList):
            button.setText(text)
            button.setVisible(True)
        for index, button in enumerate(self.locationChoiceButtonList):
            button.clicked.connect(lambda _, i = index: self.setLocation(i))
        
        for button in self.locationChoiceButtonList[len(incomingList):]:
            button.setText("")
            button.setVisible(False)

    def setLocation(self, which):
        if isinstance(self.geoLocation.request, list):
            # For city searches, where the request is a list of dictionaries
            locationChoice = self.geoLocation.request[which]
        elif isinstance(self.geoLocation.request, dict):
            # For ZIP code searches, where the request is a single dictionary
            locationChoice = self.geoLocation.request
        
        self.weatherRequester.city = locationChoice.get("name", "Unknown")
        self.weatherRequester.lat = locationChoice.get("lat")
        self.weatherRequester.lon = locationChoice.get("lon")
        self.weatherRequester.requestWeather()
        self.dashboard.updateUI()
        

# Window for setting location
class SetLocationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Location")
        self.setGeometry(200, 300, 300, 200)

# Window for setting units
class SetUnitsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Units")
        self.setGeometry(200, 400, 300, 200)

class GeoLocation:
    def __init__(self):
        print("Geo Location initialized")
        self.appID = None
        self.city = None
        self.zipcode = None
        self.URL = None
        self.request = None

    def setAppID(self, string):
        print("GeoLocation Class")
        self.appID=string
        print(self.appID)
        writeFile = SaveID()
        writeFile.savePassword(self.appID)

    def byCity(self, city):
        self.city = city
        self.URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(self.city, self.appID)
        #this will contain necessary info to pass to weather (lat lon)
        self.request = requests.get(self.URL).json()
        formattedLocations = [
            f"{loc.get("name")}, {loc.get("state", "")}, {loc.get("country")}".replace(", ,", ",").strip(",")
            for loc in self.request
        ]
        
        self.buttonNames = formattedLocations
        print(self.request)

    def byZipcode(self, zip):
        self.zip = zip
        self.URL = "http://api.openweathermap.org/geo/1.0/zip?zip={}&appid={}".format(self.zip, self.appID)
        self.request = requests.get(self.URL).json()

        # Since the result is a single dictionary, process it accordingly
        formattedLocation = f"{self.request.get('name', 'Unknown')}, {self.request.get('state', '')}, {self.request.get('country', '')}".replace(", ,", ",").strip(",")

        # Ensure this is a list, not a set
        self.buttonNames = [formattedLocation]
        print(self.request)

    def checkExistingID(self):
        macFilePath = "/Users/johnzilka/Documents/JZ/Documents/EZHomeDashboardWeatherID.json"
        print("check for saved file")
        if os.path.exists(macFilePath):
            print("app id exists. getting it now")
            with open(macFilePath, "r") as file:
                data=json.load(file)
            self.appID=data["appID"]

            return "ID Found"
        else:
            return "Enter App ID"

class SaveID:
    def __init__(self):
        print("Save ID initialized")
        self.data = {}

    def savePassword(self, appID):
        self.data = {
            "appID" : appID
        }

        macFilePath = "/Users/johnzilka/Documents/JZ/Documents/EZHomeDashboardWeatherID.json"
        #/Users/johnzilka/Documents/JZ/Documents
        with open(macFilePath, "w") as file:
            json.dump(self.data, file)