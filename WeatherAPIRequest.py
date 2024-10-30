import requests
import os
import json
from datetime import datetime
from pathlib import Path

class WeatherAPIRequest:
    def __init__(self):
        self.city = None
        self.lat = None
        self.lon = None
        self.appID = None
        self.URL = None
        self.request = None
        self.currentTemp = None
        self.Test = False
        print("weather initialized")
        self.checkExistingID()

    def printName(self):
        print(self.city)
        print(self.lat)
        print(self.lon)

    def checkExistingID(self):
        #macFilePath = "/Users/johnzilka/Documents/JZ/Documents/EZHomeDashboardWeatherID.json"
        #documentsPath = Path.home() / "Documents" / "EZHomeDashboard" / "EZHomeDashboardWeatherID.json"
        documentsPath = Path.home() / "Documents" / "EZHomeDashboard"
        filePath = documentsPath / "EZHomeDashboardWeatherID.json"
        print("check for saved file")
        if os.path.exists(filePath):
            print("app id exists. getting it now")
            with open(filePath, "r") as file:
                data=json.load(file)
            self.appID=data["appID"]

            print("ID found")
        else:
            print("No ID saved")

    def requestWeather(self):
        print("WeatherAPI Requesting Weather")
        if not self.Test:
            self.URL = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=imperial&appid={}".format(self.lat, self.lon, self.appID)
            self.request = requests.get(self.URL).json()
        #print(self.appID)
        #print(self.request)
        self.setCurrentWeatherFields()

    def formatTimeStamp(self, timeStamp):
        adjustedTime = datetime.fromtimestamp(timeStamp)
        weekdayIndex = adjustedTime.weekday()
        weekdaysDict = {
            0 : "Monday",
            1 : "Tuesday",
            2 : "Wednesday",
            3 : "Thursday",
            4 : "Friday",
            5 : "Saturday",
            6 : "Sunday"
        }
        if weekdayIndex in weekdaysDict:
            dayOfTheWeek = weekdaysDict[weekdayIndex]
        standardTime = adjustedTime.strftime("%I:%M:%S %p")
        monthDict = {
            "1" : "January",
            "2" : "February",
            "3" : "March",
            "4" : "April",
            "5" : "May",
            "6" : "June",
            "7" : "July",
            "8" : "August",
            "9" : "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"
        }
        monthIndex = str(adjustedTime.month)
        #hour = adjustedTime.strftime("%I %p")
        #hour = adjustedTime.strftime("%I")
        hour = adjustedTime.hour
        month = monthDict[monthIndex]
        date = adjustedTime.day
        year = adjustedTime.year

        dateString = str(f"{month} {date}, {year}")
        #standardHour = str(f"{hour}")
        standardHour = adjustedTime.strftime("%I:%M %p")

        return dayOfTheWeek, standardTime, dateString, standardHour

    def setCurrentWeatherFields(self):
        self.todaySummay = self.request["daily"][0]["summary"]
        self.currentTemp = self.request["current"]["temp"]
        self.expectedHigh = self.request["daily"][0]["temp"]["max"]
        self.expectedLow = self.request["daily"][0]["temp"]["min"]
        self.precipProb = self.request["daily"][0]["pop"]
        self.todayDescription = self.request["daily"][0]["weather"][0]["description"]
        self.todaySunrise = self.formatTimeStamp(self.request["current"]["sunrise"])[1]
        self.todaySunset = self.formatTimeStamp(self.request["current"]["sunset"])[1]
        self.todayMoonrise = self.formatTimeStamp(self.request["daily"][0]["moonrise"])[1]
        self.todayMoonset = self.formatTimeStamp(self.request["daily"][0]["moonset"])[1]
