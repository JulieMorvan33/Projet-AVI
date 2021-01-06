from PyQt5 import QtCore, QtGui, QtWidgets

TOT_WIDTH = 1400
TOT_HEIGHT = 900

WIDTH = 800
HEIGHT = 800

class Ui_MainWindow(object):
    def __init__(self, param_view, view, compass_view, aircraft_view, sim):
        super().__init__()
        self.graphicsView = param_view # QGraphicView pour les paramètres de vol (DTWPT...)
        self.graphicsView_2 = view
        self.graphicsView_3 = compass_view
        self.graphicsView_4 = aircraft_view
        self.sim = sim

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(TOT_WIDTH, TOT_HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, TOT_WIDTH, TOT_HEIGHT))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setGeometry(QtCore.QRect(0, 0, WIDTH, TOT_HEIGHT))

        # QGraphicView pour les paramètres de vol (DTWPT...)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setFixedSize(QtCore.QSize(WIDTH, TOT_HEIGHT-HEIGHT))
        self.verticalLayout_6.addWidget(self.graphicsView)

        self.stackedLayout = QtWidgets.QStackedLayout(self.verticalLayout_6)
        self.stackedLayout.setObjectName("stackedLayout")
        self.stackedLayout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        # QGraphicsView pour le compas
        self.graphicsView_3.setFixedSize(QtCore.QSize(WIDTH, HEIGHT))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.graphicsView_3.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(1, self.graphicsView_3)
        self.graphicsView_3.setRenderHint(QtGui.QPainter.Antialiasing)  # enable anti-aliasing

        # QGraphicsView pour la visualisation de l'avion
        self.graphicsView_4.setFixedSize(QtCore.QSize(WIDTH, HEIGHT))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_4.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(2, self.graphicsView_4)

        # QGraphicsView pour la visualisation de la trajectoire
        self.graphicsView_2.setFixedSize(QtCore.QSize(WIDTH, HEIGHT))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.setStyleSheet("background:transparent;")
        self.stackedLayout.insertWidget(3, self.graphicsView_2)


        self.verticalLayout_6.addLayout(self.stackedLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_6)


        # Partie droite de la fenêtre

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.tabWidget = QtWidgets.QTabWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setFixedSize(QtCore.QSize(TOT_WIDTH-WIDTH, TOT_HEIGHT))
        self.tabWidget.setStyleSheet("background-color: rgb(223, 223, 223);")
        self.tabWidget.setObjectName("tabWidget")
        self.Flight_Param = QtWidgets.QWidget()
        self.Flight_Param.setWhatsThis("")
        self.Flight_Param.setObjectName("Flight_Param")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.Flight_Param)
        self.verticalLayoutWidget_3.setFixedSize(QtCore.QSize(TOT_WIDTH-WIDTH-100, TOT_HEIGHT-200))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_7.setContentsMargins(50, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_7.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_7.addWidget(self.line_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(125, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(8, 8))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_7.addWidget(self.line_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        #spacerItem2 = QtWidgets.QSpacerItem(85, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_6.addItem(spacerItem2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        #spacerItem4 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        #self.verticalLayout_7.addItem(spacerItem4)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_7.addWidget(self.line_4)
        #spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        #self.verticalLayout_7.addItem(spacerItem5)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.define_flight_param)
        self.verticalLayout_7.addWidget(self.pushButton)
        self.tabWidget.addTab(self.Flight_Param, "")
        self.PFD_Param = QtWidgets.QWidget()
        self.PFD_Param.setObjectName("PFD_Param")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.PFD_Param)
        self.verticalLayoutWidget_4.setFixedSize(QtCore.QSize(TOT_WIDTH-WIDTH, TOT_HEIGHT-200))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_8.setContentsMargins(50, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_8.addWidget(self.line_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        spacerItem6 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_8.addWidget(self.line_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_10.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_10.addWidget(self.label_12)
        spacerItem7 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_8.addLayout(self.horizontalLayout_10)
        self.line_7 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_8.addWidget(self.line_7)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")


        #spacerItem8 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_11.addItem(spacerItem8)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_11.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_11.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_11.addWidget(self.label_15)
        #spacerItem9 = QtWidgets.QSpacerItem(235, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_11.addItem(spacerItem9)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.line_8 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_8.addWidget(self.line_8)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")

        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem10)
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_12.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_12.addWidget(self.label_17)
        spacerItem11 = QtWidgets.QSpacerItem(280, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem11)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.line_9 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.verticalLayout_8.addWidget(self.line_9)
        self.tabWidget.addTab(self.PFD_Param, "")
        self.Mode_Param = QtWidgets.QWidget()
        self.Mode_Param.setObjectName("Mode_Param")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.Mode_Param)
        self.verticalLayoutWidget_5.setFixedSize(QtCore.QSize(TOT_WIDTH-WIDTH-100, TOT_HEIGHT-200))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.line_11 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.verticalLayout_9.addWidget(self.line_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_18 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_13.addWidget(self.label_18)
        self.label_19 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_13.addWidget(self.label_19)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem12)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.line_10 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.verticalLayout_9.addWidget(self.line_10)
        spacerItem13 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_9.addItem(spacerItem13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_20 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_14.addWidget(self.label_20)
        self.horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(120)
        self.horizontalSlider.setSingleStep(20)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_14.addWidget(self.horizontalSlider)
        spacerItem14 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem14)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        spacerItem15 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_9.addItem(spacerItem15)
        self.line_12 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.verticalLayout_9.addWidget(self.line_12)
        self.tabWidget.addTab(self.Mode_Param, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sim.update_param_1.connect(self.update_labels)
        self.sim.AP_mode_signal.connect(self.update_AP_mode)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setAccessibleName(_translate("MainWindow", "Param"))
        self.label.setText(_translate("MainWindow", "CRUISE ALTITUDE :"))
        self.label_2.setText(_translate("MainWindow", "ft"))
        self.label_3.setText(_translate("MainWindow", "WIND :"))
        self.label_4.setText(_translate("MainWindow", "°"))
        self.label_5.setText(_translate("MainWindow", "kts"))
        self.label_6.setText(_translate("MainWindow", "COST INDEX :"))
        self.pushButton.setText(_translate("MainWindow", "VALIDATE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Flight_Param), _translate("MainWindow", "Tab 1"))
        self.label_7.setText(_translate("MainWindow", "XTK :"))
        self.label_8.setText(_translate("MainWindow", "..."))
        self.label_9.setText(_translate("MainWindow", "NM"))
        self.label_10.setText(_translate("MainWindow", "TAE :"))
        self.label_11.setText(_translate("MainWindow", "..."))
        self.label_12.setText(_translate("MainWindow", "°"))
        self.label_13.setText(_translate("MainWindow", "ALDTWPT : "))
        self.label_14.setText(_translate("MainWindow", "..."))
        self.label_15.setText(_translate("MainWindow", "NM"))
        self.label_16.setText(_translate("MainWindow", "FL_OPTI : "))
        self.label_17.setText(_translate("MainWindow", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PFD_Param), _translate("MainWindow", "Page"))
        self.label_18.setText(_translate("MainWindow", "MODE : "))
        self.label_19.setText(_translate("MainWindow", "MANAGE"))
        self.label_20.setText(_translate("MainWindow", "ZOOM : "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Mode_Param), _translate("MainWindow", "Tab 2"))

    def update_labels(self):
        dict = self.sim.SEQParam
        xtk, tae, aldtwpt = dict["XTK"], dict["TAE"], dict["ALDTWPT"]
        self.label_8.setText(str(xtk))
        self.label_11.setText(str(tae))
        self.label_14.setText(str(aldtwpt))

    def define_flight_param(self):
        crz_alt = int(self.lineEdit.text())
        wind_dir = int(self.lineEdit_2.text())
        wind_speed = int(self.lineEdit_3.text())
        wind = (wind_dir, wind_speed)
        ci = int(self.lineEdit_4.text())
        print("Paramètres de vol validés : CRZ_ALT=", crz_alt,"ft WIND=", str(wind), "kts CI=", ci)
        self.sim.defineFlightParam(crz_alt, ci, wind)

    def update_AP_mode(self):
        self.label_19.setText(self.sim.AP_mode)
        print("Nouveau AP mode :", self.sim.AP_mode)

class mywindow(QtWidgets.QMainWindow):
    def __init__(self, param_view, view, compass_view, aircraft_view, sim):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow(param_view, view, compass_view, aircraft_view, sim)
        self.ui.setupUi(self)
