from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5 import QtCore, QtWidgets, QtGui

class VerticalEventWidget(QtWidgets.QWidget):
    def __init__(self, summary="eventSummary", start="HH:MM", date = "MM:DD:YY", location = "Location", rgb=[0, 0, 0]):
        super().__init__()
        self.summary = summary
        self.start = start
        self.date = date
        self.location = location
        self.r, self.g, self.b = rgb

        self.createWidgets()
        self.createLayouts()

    def createWidgets(self):
        # Create a container for labels
        self.eventArea = QtWidgets.QWidget()
        self.eventArea.setAutoFillBackground(True)
        self.eventArea.setStyleSheet(
            "QWidget{"
            f"background-color: rgba({self.r}, {self.g}, {self.b}, 1.0);"  # Use a solid background if needed
            "border: 2px solid transparent;"
            "border-radius: 15px;}"
        )

        self.summaryLabel = QtWidgets.QLabel(self.summary)
        self.startLabel = QtWidgets.QLabel(self.start)
        self.dateLabel = QtWidgets.QLabel(self.date)
        self.locationLabel = QtWidgets.QLabel(self.location)

    def createLayouts(self):
        self.eventLayout = QtWidgets.QVBoxLayout()
        self.eventLayout.setContentsMargins(10, 10, 10, 10)  # Adjust margins if necessary
        self.eventLayout.setSpacing(0)
        self.eventLayout.addWidget(self.summaryLabel)
        self.eventLayout.addWidget(self.startLabel)
        self.eventLayout.addWidget(self.dateLabel)
        self.eventLayout.addWidget(self.locationLabel)

        self.eventArea.setLayout(self.eventLayout)

        # Set the main layout for the parent widget
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(5, 30, 5, 5) #argin around outside of each event
        mainLayout.setSpacing(50)
        mainLayout.addWidget(self.eventArea)
        self.setLayout(mainLayout)

class HorizontalEventWidget(QtWidgets.QWidget):
    def __init__(self, summary = "eventSummary", start = "HH:MM", rgb=[0, 0, 0]):
        super().__init__()
        self.summary = summary
        self.start = start
        self.r, self.g, self.b = rgb

        self.createWidgets()
        self.createLayouts()

    def createWidgets(self):
        # Create a container for labels
        self.eventArea = QtWidgets.QWidget()
        self.eventArea.setAutoFillBackground(True)
        self.eventArea.setStyleSheet(
            "QWidget{"
            f"background-color: rgba({self.r}, {self.g}, {self.b}, 1.0);"  # Use a solid background if needed
            "border: 2px solid transparent;"
            "border-radius: 15px;}"
        )

        self.summaryLabel = QtWidgets.QLabel(self.summary)
        self.startLabel = QtWidgets.QLabel(self.start)

    def createLayouts(self):
        self.eventLayout = QtWidgets.QHBoxLayout()
        self.eventLayout.setContentsMargins(5, 5, 5, 5)  # Adjust margins if necessary
        self.eventLayout.setSpacing(0)
        self.eventLayout.addWidget(self.summaryLabel)
        self.eventLayout.addWidget(self.startLabel)

        self.eventArea.setLayout(self.eventLayout)

        # Set the main layout for the parent widget
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.eventArea)
        self.setLayout(mainLayout)