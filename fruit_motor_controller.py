#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
___  ____  _____   ____  _____ ____ _ __ _____
\  \/ (__)/ .___>_/    \/   . >    | |  | ____>
 \    |  | <_<    > <> |     <  <> | |  |___  \
  \   |__|____   |\____|__|\  \____|    |      >
   \_/        `--'          `--'    `---'\____/
        P  R  o  G  R  A  M  M  i  N  G
<========================================[KCS]=>
  Developer: David Meyer
  Project  : Hexbug Vex Motor Controller Widget
  Purpose  : Basic Adafruit HAT Controller GUI for testing and casual use
  Version  : 1.0.0
<=================================[02/08/2017]=>

    This code is the same as the L298N code but uses the Adafruit_MotorHAT...
    which is much easier to use than the GPIO features.

"""

import sys
from PyQt4 import QtCore, QtGui, uic
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

myMotor01 = mh.getMotor(1)
myMotor02 = mh.getMotor(2)
myMotor03 = mh.getMotor(3)
myMotor04 = mh.getMotor(4)


# Set QT Creator File Name and Load
qtCreatorFile = "fruit_motor_controller.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#[Classes]##############################################################
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)        
        self.centerOnScreen()
        
        self.motor01_btn_val = 0 # 0=off    / 1=on
        self.motor01_ssu_val = 0 # 0=slider / 1=spinner 
        self.motor02_btn_val = 0 # 0=off    / 1=on
        self.motor02_ssu_val = 0 # 0=slider / 1=spinner 
        self.motor03_btn_val = 0 # 0=off    / 1=on
        self.motor03_ssu_val = 0 # 0=slider / 1=spinner              
        self.motor04_btn_val = 0 # 0=off    / 1=on
        self.motor04_ssu_val = 0 # 0=slider / 1=spinner 


        #[Widget Events]################################################
        self.pushButtonQuit.clicked.connect(self.quit_controller)

        #-Motor 1-#
        self.pushButtonMotor1.clicked.connect(self.motor01_btn_clk)
        self.verticalSliderMotor1.valueChanged.connect(self.motor01_sld_use)
        self.verticalSliderMotor1.sliderReleased.connect(self.motor01_sld_spring)
        self.spinBoxMotor1.valueChanged.connect(self.motor01_spn_use)
        self.checkBoxMotor1.stateChanged.connect(self.motor01_spring)
        
        #-Motor 2-#
        self.pushButtonMotor2.clicked.connect(self.motor02_btn_clk)
        self.verticalSliderMotor2.valueChanged.connect(self.motor02_sld_use)
        self.verticalSliderMotor2.sliderReleased.connect(self.motor02_sld_spring)
        self.spinBoxMotor2.valueChanged.connect(self.motor02_spn_use)
        self.checkBoxMotor2.stateChanged.connect(self.motor02_spring)        

        #-Motor 3-#
        self.pushButtonMotor3.clicked.connect(self.motor03_btn_clk)
        self.verticalSliderMotor3.valueChanged.connect(self.motor03_sld_use)
        self.verticalSliderMotor3.sliderReleased.connect(self.motor03_sld_spring)
        self.spinBoxMotor3.valueChanged.connect(self.motor03_spn_use)
        self.checkBoxMotor3.stateChanged.connect(self.motor03_spring)

        #-Motor 4-#
        self.pushButtonMotor4.clicked.connect(self.motor04_btn_clk)
        self.verticalSliderMotor4.valueChanged.connect(self.motor04_sld_use)
        self.verticalSliderMotor4.sliderReleased.connect(self.motor04_sld_spring)
        self.spinBoxMotor4.valueChanged.connect(self.motor04_spn_use)
        self.checkBoxMotor4.stateChanged.connect(self.motor04_spring)


#[Functions]############################################################
    def centerOnScreen(self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
    
    def quit_controller(self):
        print ("Shutdown Motors and Exit...")
        self.turnOffMotors()
        self.close()

    #-Motor 1-#
    def motor01_spring(self):
        if self.checkBoxMotor1.isChecked():
            self.spinBoxMotor1.setEnabled(False)
            self.motor01_sld_spring()
        else:
            self.spinBoxMotor1.setEnabled(True)
    
    def motor01_sld_spring(self):
        if self.checkBoxMotor1.isChecked():
            self.verticalSliderMotor1.setValue(0)
            self.motor01_runtime()
    
    def motor01_sld_use(self):
        if self.motor01_ssu_val == 1:
            self.motor01_ssu_val = 0
        else:
            self.motor01_runtime()
    
    def motor01_spn_use(self):
        if self.motor01_ssu_val == 0:
            self.motor01_ssu_val = 1
        else:
            self.motor01_runtime()
    
    def motor01_btn_clk(self):
        if self.motor01_btn_val == 0:
            self.motor01_btn_val = 1
            self.pushButtonMotor1.setText("Off")
            self.motor01_runtime()
        else:
            self.motor01_btn_val = 0
            myMotor01.run(Adafruit_MotorHAT.RELEASE);
            self.pushButtonMotor1.setText("On")
    
    def motor01_runtime(self):
        if self.motor01_ssu_val == 0:
            power = self.verticalSliderMotor1.value()
            self.spinBoxMotor1.setValue(power)
        else:
            power = self.spinBoxMotor1.value()
            self.verticalSliderMotor1.setValue(power)
        if self.motor01_btn_val == 1:
            if power >= 0:
                myMotor01.run(Adafruit_MotorHAT.FORWARD)
                myMotor01.setSpeed(power)
            if power < 0:
                myMotor01.run(Adafruit_MotorHAT.BACKWARD)
                myMotor01.setSpeed(power * -1)

    #-Motor 2-#
    def motor02_spring(self):
        if self.checkBoxMotor2.isChecked():
            self.spinBoxMotor2.setEnabled(False)
            self.motor02_sld_spring()
        else:
            self.spinBoxMotor2.setEnabled(True)
    
    def motor02_sld_spring(self):
        if self.checkBoxMotor2.isChecked():
            self.verticalSliderMotor2.setValue(0)
            self.motor02_runtime()
    
    def motor02_sld_use(self):
        if self.motor02_ssu_val == 1:
            self.motor02_ssu_val = 0
        else:
            self.motor02_runtime()
    
    def motor02_spn_use(self):
        if self.motor02_ssu_val == 0:
            self.motor02_ssu_val = 1
        else:
            self.motor02_runtime()
    
    def motor02_btn_clk(self):
        if self.motor02_btn_val == 0:
            self.motor02_btn_val = 1
            self.pushButtonMotor2.setText("Off")
            self.motor02_runtime()
        else:
            self.motor02_btn_val = 0
            myMotor02.run(Adafruit_MotorHAT.RELEASE);
            self.pushButtonMotor2.setText("On")
    
    def motor02_runtime(self):
        if self.motor02_ssu_val == 0:
            power = self.verticalSliderMotor2.value()
            self.spinBoxMotor2.setValue(power)
        else:
            power = self.spinBoxMotor2.value()
            self.verticalSliderMotor2.setValue(power)
        if self.motor02_btn_val == 1:
            if power >= 0:
                myMotor02.run(Adafruit_MotorHAT.FORWARD)
                myMotor02.setSpeed(power)
            if power < 0:
                myMotor02.run(Adafruit_MotorHAT.BACKWARD)
                myMotor02.setSpeed(power * -1)

    #-Motor 3-#
    def motor03_spring(self):
        if self.checkBoxMotor3.isChecked():
            self.spinBoxMotor3.setEnabled(False)
            self.motor03_sld_spring()
        else:
            self.spinBoxMotor3.setEnabled(True)
    
    def motor03_sld_spring(self):
        if self.checkBoxMotor3.isChecked():
            self.verticalSliderMotor3.setValue(0)
            self.motor03_runtime()
    
    def motor03_sld_use(self):
        if self.motor03_ssu_val == 1:
            self.motor03_ssu_val = 0
        else:
            self.motor03_runtime()
    
    def motor03_spn_use(self):
        if self.motor03_ssu_val == 0:
            self.motor03_ssu_val = 1
        else:
            self.motor03_runtime()
    
    def motor03_btn_clk(self):
        if self.motor03_btn_val == 0:
            self.motor03_btn_val = 1
            self.pushButtonMotor3.setText("Off")
            self.motor03_runtime()
        else:
            self.motor03_btn_val = 0
            myMotor03.run(Adafruit_MotorHAT.RELEASE);
            self.pushButtonMotor3.setText("On")
    
    def motor03_runtime(self):
        if self.motor03_ssu_val == 0:
            power = self.verticalSliderMotor3.value()
            self.spinBoxMotor3.setValue(power)
        else:
            power = self.spinBoxMotor3.value()
            self.verticalSliderMotor3.setValue(power)
        if self.motor03_btn_val == 1:
            if power >= 0:
                myMotor03.run(Adafruit_MotorHAT.FORWARD)
                myMotor03.setSpeed(power)
            if power < 0:
                myMotor03.run(Adafruit_MotorHAT.BACKWARD)
                myMotor03.setSpeed(power * -1)

    #-Motor 4-#
    def motor04_spring(self):
        if self.checkBoxMotor4.isChecked():
            self.spinBoxMotor4.setEnabled(False)
            self.motor04_sld_spring()
        else:
            self.spinBoxMotor4.setEnabled(True)
    
    def motor04_sld_spring(self):
        if self.checkBoxMotor4.isChecked():
            self.verticalSliderMotor4.setValue(0)
            self.motor04_runtime()
    
    def motor04_sld_use(self):
        if self.motor04_ssu_val == 1:
            self.motor04_ssu_val = 0
        else:
            self.motor04_runtime()
    
    def motor04_spn_use(self):
        if self.motor04_ssu_val == 0:
            self.motor04_ssu_val = 1
        else:
            self.motor04_runtime()
    
    def motor04_btn_clk(self):
        if self.motor04_btn_val == 0:
            self.motor04_btn_val = 1
            self.pushButtonMotor4.setText("Off")
            self.motor04_runtime()
        else:
            self.motor04_btn_val = 0
            myMotor04.run(Adafruit_MotorHAT.RELEASE);
            self.pushButtonMotor4.setText("On")
    
    def motor04_runtime(self):
        if self.motor04_ssu_val == 0:
            power = self.verticalSliderMotor4.value()
            self.spinBoxMotor4.setValue(power)
        else:
            power = self.spinBoxMotor4.value()
            self.verticalSliderMotor4.setValue(power)
        if self.motor04_btn_val == 1:
            if power >= 0:
                myMotor04.run(Adafruit_MotorHAT.FORWARD)
                myMotor04.setSpeed(power)
            if power < 0:
                myMotor04.run(Adafruit_MotorHAT.BACKWARD)
                myMotor04.setSpeed(power * -1)

    def turnOffMotors(SELF):
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


if __name__ == "__main__":
    print ("Starting Robotic Arm Controller...")
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


