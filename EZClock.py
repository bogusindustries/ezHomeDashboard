import sys
from datetime import datetime
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class Clock(QObject):
    timeSignal = pyqtSignal(str)
    dateSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        
        self.timer = QTimer(self)

        self.startTimer()

    def startTimer(self):
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onTimeInterval)
        self.timer.start()

    def onTimeInterval(self):
        currentTime = datetime.now()
        adjustedTime = currentTime.strftime("%I:%M:%S %p")
        dayIndex = str(currentTime.weekday())
        monthIndex = str(currentTime.month)
        weekdaysDict = {
            "0" : "Monday",
            "1" : "Tuesday",
            "2" : "Wednesday",
            "3" : "Thursday",
            "4" : "Friday",
            "5" : "Saturday",
            "6" : "Sunday"
        }
        
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
        
        month = monthDict[monthIndex]
        day = weekdaysDict[dayIndex]
        date = currentTime.day
        dateString = f"{day} {month}, {date}"
        self.timeSignal.emit(adjustedTime)
        self.dateSignal.emit(dateString)



