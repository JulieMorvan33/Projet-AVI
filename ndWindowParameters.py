# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\NDmodif.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, param_view, view, compass_view, aircraft_view):
        super().__init__()
        self.graphicsView = param_view # QGraphicView pour les paramètres de vol (DTWPT...)
        self.graphicsView_2 = view
        self.graphicsView_3 = compass_view
        self.graphicsView_4 = aircraft_view


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 837)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 811, 821))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # QGraphicView pour les paramètres de vol (DTWPT...)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setFixedSize(QtCore.QSize(811, 100))
        self.verticalLayout.addWidget(self.graphicsView)

        self.stackedLayout = QtWidgets.QStackedLayout(self.verticalLayoutWidget)
        self.stackedLayout.setObjectName("stackedLayout")
        self.stackedLayout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        # QGraphicsView pour le compas
        self.graphicsView_3.setGeometry(QtCore.QRect(0, 0, 811, 701))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.graphicsView_3.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(1, self.graphicsView_3)
        self.graphicsView_3.setRenderHint(QtGui.QPainter.Antialiasing) # enable anti-aliasing

        # QGraphicsView pour la visualisation de l'avion
        self.graphicsView_4.setGeometry(QtCore.QRect(0, 0, 811, 701))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_4.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(2, self.graphicsView_4)

        # QGraphicsView pour la visualisation de la trajectoire
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 811, 701))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(3, self.graphicsView_2)


        #self.stackedLayout.setCurrentWidget(self.graphicsView_4)

        self.verticalLayout.addLayout(self.stackedLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        # self.stackedLayout.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class mywindow(QtWidgets.QMainWindow):
    def __init__(self, param_view, view, compass_view, aircraft_view):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow(param_view, view, compass_view, aircraft_view)
        self.ui.setupUi(self)
