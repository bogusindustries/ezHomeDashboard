# version 00001

import sys

# from PyQt5 import QtWidgets
# from PyQt5 import QtGui
# from PyQt5.QtCore import Qt

from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6.QtCore import Qt

import EventWidgets as eventWidgets
import EZClock as clock
import ApplicationSettings as settings
import GoogleCalendarAPI as calendar

class EZHomeDashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EZ Home Dashboard v 0.0.001")
        self.setGeometry(0, 0, 960, 540)

        self.defaultIcon = QtGui.QPixmap("icons/default.png")
        self.defaultFont = "Avenir"
        self.secondaryFont = "Roboto"

        self.clock = clock.Clock()
        self.weatherSettingsWindow = settings.WeatherSettingsWindow(self)
        self.weather = self.weatherSettingsWindow.weatherRequester
        self.calendar = calendar.GoogleCalenderAPI()
        

        self.createMenus()
        self.createPalettes()
        self.createDateTimeSection()
        self.createWeatherSection()
        self.createTopSection()
        self.createScheduleSection()
        self.createBottomsection()
        self.createMainLayouts()
        self.connectUI()
        self.runClock()

    def runClock(self):
        self.clock.timeSignal.connect(self.updateClock)
        self.clock.dateSignal.connect(self.updateDate)

    def updateClock(self, currentTime):
        self.timeLabel.setText(currentTime)

    def updateDate(self, currentDate):
        self.dateLabel.setText(currentDate)

    def createMenus(self):
        self.menu = self.menuBar()

        self.fileMenu = self.menu.addMenu("File")
        #self.exitAction = QtWidgets.QAction("Close")
        self.exitAction = QtGui.QAction("Close")
        self.fileMenu.addAction(self.exitAction)

        self.settingsMenu = self.menu.addMenu("Settings")
        #self.weatherSettingsAction = QtWidgets.QAction("Weather Settings")
        self.weatherSettingsAction = QtGui.QAction("Weather Settings")
        self.settingsMenu.addAction(self.weatherSettingsAction)
        #self.scheduleSettingsAction = QtWidgets.QAction("Schedule Settings")
        self.scheduleSettingsAction = QtGui.QAction("Schedule Settings")
        self.settingsMenu.addAction(self.scheduleSettingsAction)

        self.windowsMenu = self.menu.addMenu("Windows")
        self.windowsMenu.addAction("Home")
        #self.weatherWindowAction = QtWidgets.QAction("Weather")
        self.weatherWindowAction = QtGui.QAction("Weather")
        self.windowsMenu.addAction(self.weatherWindowAction)
        #self.scheduleWindowAction = QtWidgets.QAction("Schedule")
        self.scheduleWindowAction = QtGui.QAction("Schedule")
        self.windowsMenu.addAction(self.scheduleWindowAction)

    def createPalettes(self):
        self.blackPalette = QtGui.QPalette()
        self.blackPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))

        self.darkGrayPalette = QtGui.QPalette()
        self.darkGrayPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(40, 40, 40))

        self.midGrayPalette = QtGui.QPalette()
        self.midGrayPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 50, 50))

        self.lightGrayPalette = QtGui.QPalette()
        self.lightGrayPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(70, 70, 70))

        #120, 32, 76
        self.magentaPalette = QtGui.QPalette()
        self.magentaPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(120, 32, 76))

    def createDateTimeSection(self):
        self.timeArea = QtWidgets.QWidget()
        self.timeArea.setAutoFillBackground(True)
        self.timeArea.setPalette(self.blackPalette)
        self.timeArea.setStyleSheet(
            "QWidget {"
                "background-color: rgba(0,0,0,1.0);"
                "border: 2px solid transparent;"
                "border-radius: 15px;"
            "}"
            "QLabel {"
                "color: white;"
            "}"
        )

        self.timeLabel = QtWidgets.QLabel("HH:MM %p")
        self.timeLabel.setFont(QtGui.QFont(self.defaultFont, 45))
        self.timeLabel.setAlignment(Qt.AlignCenter)

        self.dateLabel = QtWidgets.QLabel("Day, Month ##")
        self.dateLabel.setFont(QtGui.QFont(self.defaultFont, 12))
        self.dateLabel.setAlignment(Qt.AlignCenter)

        self.timeAreaLayout = QtWidgets.QVBoxLayout()
        self.timeAreaLayout.setContentsMargins(10,100,10,100)
        self.timeAreaLayout.setSpacing(0)
        self.timeAreaLayout.addWidget(self.timeLabel)
        self.timeAreaLayout.addWidget(self.dateLabel)

        self.timeArea.setLayout(self.timeAreaLayout)

    def createWeatherSection(self):
        self.weatherArea = QtWidgets.QWidget()
        self.weatherArea.setAutoFillBackground(True)
        self.weatherArea.setPalette(self.midGrayPalette)
        self.weatherArea.setStyleSheet(
            "QWidget {"
                "background-color: rgba(40, 40, 40, 1.0);"
                "border: 2px solid transparent;"
                "border-radius: 15px;"
            "}"
            "QLabel {"
                "color : white;"
            "}"
        )

        self.weatherSummaryLabel = QtWidgets.QLabel("Summary")
        self.weatherSummaryLabel.setAlignment(Qt.AlignCenter)

        self.currentTempLabel = QtWidgets.QLabel("XX °F")
        self.currentTempLabel.setFont(QtGui.QFont(self.defaultFont, 90))
        self.currentTempLabel.setAlignment(Qt.AlignCenter)

        self.expectedHighLabel = QtWidgets.QLabel("H: XX °F")
        self.expectedLowLabel = QtWidgets.QLabel("L: XX °F")
        self.precipProbLabel = QtWidgets.QLabel("XX%")

        self.currentWeatherImageWidget = QtWidgets.QLabel()
        self.currentWeatherImageWidget.setPixmap(self.defaultIcon)
        self.currentWeatherImageWidget.setAlignment(Qt.AlignCenter)
        self.currentWeatherDescriptionLabel = QtWidgets.QLabel("Description")
        self.currentWeatherDescriptionLabel.setAlignment(Qt.AlignCenter)
        self.currentMoonImageWidget = QtWidgets.QLabel()
        self.currentMoonImageWidget.setPixmap(self.defaultIcon)
        self.currentMoonPhaseLabel = QtWidgets.QLabel("Moon Phase")
        self.todaySunriseLabel = QtWidgets.QLabel("Sunrise: HH:MM %p")
        self.todaySunsetLabel = QtWidgets.QLabel("Sunset: HH:MM %p")
        self.todayMoonriseLabel = QtWidgets.QLabel("Moonrise: HH:MM %p")
        self.todayMoonsetLabel = QtWidgets.QLabel("Moonset: HH:MM %p")

        self.expectedWeatherLayout = QtWidgets.QHBoxLayout()
        self.expectedWeatherLayout.setAlignment(Qt.AlignCenter)
        self.expectedWeatherLayout.addWidget(self.expectedHighLabel)
        self.expectedWeatherLayout.addWidget(self.expectedLowLabel)
        self.expectedWeatherLayout.addWidget(self.precipProbLabel)

        self.weatherOverviewLayout = QtWidgets.QVBoxLayout()
        self.weatherOverviewLayout.setAlignment(Qt.AlignCenter)
        self.weatherOverviewLayout.setSpacing(15)
        self.weatherOverviewLayout.setContentsMargins(10,10,10, 10)
        self.weatherOverviewLayout.addWidget(self.weatherSummaryLabel)
        self.weatherOverviewLayout.addWidget(self.currentTempLabel)
        self.weatherOverviewLayout.addLayout(self.expectedWeatherLayout)

        self.sunLayout = QtWidgets.QVBoxLayout()
        self.sunLayout.setAlignment(Qt.AlignCenter)
        self.sunLayout.setContentsMargins(10, 10, 10, 10)
        self.sunLayout.setSpacing(30)
        self.sunLayout.addWidget(self.currentWeatherImageWidget)
        self.sunLayout.addWidget(self.currentWeatherDescriptionLabel)
        self.sunLayout.addWidget(self.todaySunriseLabel)
        self.sunLayout.addWidget(self.todaySunsetLabel)

        self.moonLayout = QtWidgets.QVBoxLayout()
        self.moonLayout.setAlignment(Qt.AlignCenter)
        self.moonLayout.setContentsMargins(10, 10, 10, 10)
        self.moonLayout.setSpacing(30)
        self.moonLayout.addWidget(self.currentMoonImageWidget)
        self.moonLayout.addWidget(self.currentMoonPhaseLabel)
        self.moonLayout.addWidget(self.todayMoonriseLabel)
        self.moonLayout.addWidget(self.todayMoonsetLabel)

        self.weatherAreaLayout = QtWidgets.QHBoxLayout()
        self.weatherAreaLayout.addLayout(self.weatherOverviewLayout)
        self.weatherAreaLayout.addLayout(self.sunLayout)
        self.weatherAreaLayout.addLayout(self.moonLayout)

        self.weatherArea.setLayout(self.weatherAreaLayout)

    def createTopSection(self):
        self.homeTopSectionLayout = QtWidgets.QHBoxLayout()
        self.homeTopSectionLayout.addWidget(self.timeArea)
        self.homeTopSectionLayout.addWidget(self.weatherArea)

    def createScheduleSection(self):
        self.scheduleArea = QtWidgets.QWidget()
        self.scheduleArea.setObjectName("scheduleArea")
        self.scheduleArea.setContentsMargins(10, 10, 10, 10)
        #self.scheduleArea.setAutoFillBackground(True)

        #self.scheduleArea.setPalette(self.magentaPalette)
        self.scheduleArea.setStyleSheet(
            "#scheduleArea{"
                "background-color: rgba(70, 70, 70, 1.0);"
                "border: 2px solid transparent;"
                "border-radius: 15px;"
            "}"
            "QLabel {"
                "color: white;"
            "}"
        )

        self.todayScheduleLabel = QtWidgets.QLabel("Today's Events")
        self.todayScheduleLabel.setFixedHeight(30)

        self.todayEventsLayout = QtWidgets.QHBoxLayout()
        self.todayEventsLayout.setContentsMargins(0, 0, 0, 0)
        self.todayEventsLayout.setSpacing(0)

        if self.calendar.todayEvents:
            for each in self.calendar.todayEvents:
                event = eventWidgets.VerticalEventWidget(each["summary"], each["time"], each["date"], each["location"])
                self.todayEventsLayout.addWidget(event)
        else:
            event = eventWidgets.EmptyVerticalEventWidget()
            self.todayEventsLayout.addWidget(event)

        self.futureScheduleLabel = QtWidgets.QLabel("Upcoming Events")
        
        self.futureEventsLayout = QtWidgets.QVBoxLayout()
        self.futureEventsLayout.setContentsMargins(0,0,0,0)
        self.futureEventsLayout.setSpacing(0)

        for each in self.calendar.futureEvents:
            event = eventWidgets.HorizontalEventWidget(each["summary"], each["time"], each["date"], each["location"])
            self.futureEventsLayout.addWidget(event)

        # Holds today schedule title and events
        self.todayScheduleLayout = QtWidgets.QVBoxLayout()
        self.todayScheduleLayout.setContentsMargins(10, 10, 10, 10)
        self.todayScheduleLayout.setSpacing(10)
        self.todayScheduleLayout.addWidget(self.todayScheduleLabel)
        self.todayScheduleLayout.addLayout(self.todayEventsLayout)

        # Holds future schedule title and events
        self.futureScheduleLayout = QtWidgets.QVBoxLayout()
        self.futureScheduleLayout.addWidget(self.futureScheduleLabel)
        self.futureScheduleLayout.addLayout(self.futureEventsLayout)

        self.allScheduleLayout = QtWidgets.QHBoxLayout()
        self.allScheduleLayout.addLayout(self.todayScheduleLayout)
        self.allScheduleLayout.addLayout(self.futureScheduleLayout)
 
        self.scheduleArea.setLayout(self.allScheduleLayout)

    def createBottomsection(self):
        self.homeBottomSectionLayout = QtWidgets.QHBoxLayout()
        self.homeBottomSectionLayout.addWidget(self.scheduleArea)

    def createMainLayouts(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.homeTopSectionLayout)
        self.mainLayout.addLayout(self.homeBottomSectionLayout)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def connectUI(self):
        self.exitAction.triggered.connect(lambda:self.exitApplication())
        self.weatherSettingsAction.triggered.connect(lambda: self.openWeatherSettings())

    def openWeatherSettings(self):
        self.weatherSettingsWindow.show()

    def updateUI(self):
        self.weatherSummaryLabel.setText(f"{self.weather.todaySummay}")
        self.currentTempLabel.setText(f"{self.weather.currentTemp} °F")
        self.expectedHighLabel.setText(f"{self.weather.expectedHigh} °F")
        self.expectedLowLabel.setText(f"{self.weather.expectedLow} °F")
        self.precipProbLabel.setText(f"{self.weather.precipProb} %")
        self.currentWeatherDescriptionLabel.setText(f"{self.weather.todayDescription}")
        self.todaySunriseLabel.setText(f"{self.weather.todaySunrise}")
        self.todaySunsetLabel.setText(f"{self.weather.todaySunset}")
        self.todayMoonriseLabel.setText(f"{self.weather.todayMoonrise}")
        self.todayMoonsetLabel.setText(f"{self.weather.todayMoonset}")

    def updateCalendarUI(self):
        # Clear all widgets in `todayEventsLayout`
        while self.todayEventsLayout.count() > 0:
            item = self.todayEventsLayout.takeAt(0)  # Take the item from layout
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Delete the widget to free memory

        # Clear all widgets in `futureEventsLayout`
        while self.futureEventsLayout.count() > 0:
            item = self.futureEventsLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Request calendar updates
        self.calendar.requestCalendar()

        # Add updated widgets to `todayEventsLayout`
        if self.calendar.todayEvents:
            for each in self.calendar.todayEvents:
                event = eventWidgets.VerticalEventWidget(
                    each["summary"], each["time"], each["date"], each["location"]
                )
                self.todayEventsLayout.addWidget(event)
        else:
            event = eventWidgets.EmptyVerticalEventWidget()
            self.todayEventsLayout.addWidget(event)

        # Add updated widgets to `futureEventsLayout`
        for each in self.calendar.futureEvents:
            event = eventWidgets.HorizontalEventWidget(
                each["summary"], each["time"], each["date"], each["location"]
            )
            self.futureEventsLayout.addWidget(event)

           

    def exitApplication(self):
        self.close()
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    EZHomeDashboardInstance = EZHomeDashboard()
    EZHomeDashboardInstance.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()