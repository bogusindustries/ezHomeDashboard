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
        self.precipProb = self.processPrecipPercent(self.request["daily"][0]["pop"])
        self.todayDescription = self.request["daily"][0]["weather"][0]["description"]
        self.currentWeatherIcon = self.processCurrentIcon(self.request["daily"][0]["weather"][0]["icon"])
        self.currentMoonIcon = self.processMoonPhase(self.request["daily"][0]["moon_phase"])
        self.todaySunrise = self.formatTimeStamp(self.request["current"]["sunrise"])[1]
        self.todaySunset = self.formatTimeStamp(self.request["current"]["sunset"])[1]
        self.todayMoonrise = self.formatTimeStamp(self.request["daily"][0]["moonrise"])[1]
        self.todayMoonset = self.formatTimeStamp(self.request["daily"][0]["moonset"])[1]
        self.processMinutely()
        self.processHourly()
        #self.weatherAlert = self.request.get("alerts", "")
        if "alerts" in self.request:
            #self.weatherAlert = self.request["alerts"][0]["event"]
            self.weatherAlert = "None"
            self.weatherAlertTag = self.request["alerts"][0]["tags"][0]
            startDay, startTime = self.formatTimeStamp(self.request["alerts"][0]["start"])[0],self.formatTimeStamp(self.request["alerts"][0]["start"])[3]
            self.weatherAlertStart = f"{startDay} {startTime}"
            endDay, endTime = self.formatTimeStamp(self.request["alerts"][0]["end"])[0],self.formatTimeStamp(self.request["alerts"][0]["end"])[3]
            self.weatherAlertEnd = f"{endDay} {endTime}"
            #print(f"alert start: {self.weatherAlertStart}")
        else:
            self.weatherAlert = "None"
            self.weatherAlertTag = ""
            self.weatherAlertStart = ""
            self.weatherAlertEnd = ""



    def processMinutely(self):
        self.precipProbArray = []
        for i in self.request["minutely"]:
            #processedPercent = self.processPrecipPercent(i["precipitation"])
            mm = i["precipitation"]
            precip = (f"{mm / 25.4:.2f}")
            self.precipProbArray.append(float(precip))

    def processHourly(self):
        self.precipProbHourlyArray = []
        for i in self.request["hourly"]:
            processedPercent = self.processPrecipPercent(i["pop"])
            self.precipProbHourlyArray.append(float(processedPercent))


    def processPrecipPercent(self, pop):
        percent = (f"{pop * 100:.1f}")
        return percent

    
    def processCurrentIcon(self, image):
        imageName = image
        iconPath = f"icons/WeatherIcons/{imageName}.png"
        return iconPath
    
    # takes weather request return moon_phase (0.00-1) and returns a file path for icon
    def processMoonPhase(self, moonPhase):
        if moonPhase == 0:
            iconPath = "icons/weatherIcons/newMoon.png"
            phaseName = "New Moon"
        
        elif moonPhase > 0 and moonPhase <= 0.24:
            iconPath = "icons/weatherIcons/waxingCrescent.png"
            phaseName = "Waxing Crescent"
        
        elif moonPhase == 0.25:
            iconPath = "icons/weatherIcons/firstQuarterMoon.png"
            phaseName = "First Quarter"
        
        elif moonPhase > 0.25 and moonPhase <= 0.49:
            iconPath = "icons/weatherIcons/waxingGibbous.png"
            phaseName = "Waxing Gibbous"
        
        elif moonPhase == 0.5:
            iconPath = "icons/weatherIcons/fullMoon.png"
            phaseName = "Full Moon"
        
        elif moonPhase > 0.5 and moonPhase <= 0.74:
            iconPath = "icons/weatherIcons/waningGibbous.png"
            phaseName = "Waning Gibbous"
        
        elif moonPhase == 0.75:
            iconPath = "icons/weatherIcons/thirQuarterMoon.png"
            phaseName = "Third Quarter"
        
        elif moonPhase > 0.75 and moonPhase < 1:
            iconPath = "icons/weatherIcons/waningCrescent.png"
            phaseName = "Waning Crescent"

        elif moonPhase == 1:
            iconPath = "icons/weatherIcons/fullMoon.png"
            phaseName = "Full Moon"
        
        else:
            iconPath = "icons/weatherIcons/fullMoon.png"
            phaseName = "Unknown Phase"

        return iconPath, phaseName
