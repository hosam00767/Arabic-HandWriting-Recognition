import sys
import os
import cv2 as cv
import platform
import numpy as np
import shutil

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from imageManipultation import preprocessing as pp
from imageManipultation import segmentaion_to_paws as stp

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL VARIABLE
# ///////////////////////////////////////////////////////////////
widgets = None
originalImagePath = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        for x in range(1,10):#display lines
          self.createNewWidgets()

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # LEFT MENU BUTTONS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_preprocessing.clicked.connect(self.buttonClick)
        widgets.btn_segmentation.clicked.connect(self.buttonClick)

        widgets.btn_select.clicked.connect(self.selectTheImage)

        widgets.btn_revertRotaion.clicked.connect(self.changeAngel)
        widgets.btn_applyRotation.clicked.connect(self.changeAngel)
        widgets.threshHoldSlider.valueChanged.connect(self.number_changed)
        widgets.kernalSlider.valueChanged.connect(self.number_changed)
        widgets.angelSlider.valueChanged.connect(self.changeAngel)

        widgets.dotsSlider.valueChanged.connect(self.changeDotArea)

        # SETTING THE VALUE OF THE SLIDERS
        thresh_value = int(str(self.ui.threshHoldSlider.value()))
        kernal_value = int(str(self.ui.kernalSlider.value()))
        dotsArea_value = int(str(self.ui.dotsSlider.value()))

        widgets.thresh_value.setText(str(thresh_value))
        widgets.blur_value.setText(str(kernal_value))
        widgets.dot_value.setText(str(dotsArea_value))
        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # MENU BUTTONS FUNCTION
    # ///////////////////////////////////////////////////////////////
    def createNewWidgets(self):#display lines#
      self.frame_9 = QFrame(self.ui.scrollAreaWidgetContents)
      self.frame_9.setObjectName(u"frame_9")
      #sizePolicy1.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
     # self.frame_9.setSizePolicy(sizePolicy1)
      self.frame_9.setMinimumSize(QSize(0, 100))
      self.frame_9.setFrameShape(QFrame.StyledPanel)
      self.frame_9.setFrameShadow(QFrame.Raised)
      self.horizontalLayout_12 = QHBoxLayout(self.frame_9)
      self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
      self.pushButton = QPushButton(self.frame_9)
      self.pushButton.setObjectName(u"pushButton")
      sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
      sizePolicy6.setHorizontalStretch(0)
      sizePolicy6.setVerticalStretch(0)
      sizePolicy6.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
      self.pushButton.setSizePolicy(sizePolicy6)
      self.pushButton.setMinimumSize(QSize(35, 35))
      icon3 = QIcon()
      icon3.addFile(u"images/icons/cil-cut.png", QSize(), QIcon.Normal, QIcon.Off)
      self.pushButton.setIcon(icon3)
      self.horizontalLayout_12.addWidget(self.pushButton)
      self.label_6 = QLabel(self.frame_9)
      self.label_6.setObjectName(u"label_6")
      sizePolicy7 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
      sizePolicy7.setHorizontalStretch(0)
      sizePolicy7.setVerticalStretch(0)
      sizePolicy7.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
      self.label_6.setSizePolicy(sizePolicy7)
      self.label_6.setMinimumSize(QSize(0, 100))
      self.label_6.setPixmap(QPixmap(u"images/Capture.PNG"))
      self.label_6.setScaledContents(True)
      self.horizontalLayout_12.addWidget(self.label_6)
      self.ui.verticalLayout_13.addWidget(self.frame_9)
######################################################################################
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW PREPROCESSING PAGE
        if btnName == "btn_preprocessing":
            widgets.stackedWidget.setCurrentWidget(widgets.preprocessing_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW THE SEGMENTATION PAGE
        if btnName == "btn_segmentation":
            widgets.stackedWidget.setCurrentWidget(widgets.segmentation_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # DRAG THE APPLICATION FUNCTION
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def number_changed(self):

        global originalImagePath
        thresh_value = int(str(self.ui.threshHoldSlider.value()))
        kernal_value = int(str(self.ui.kernalSlider.value()))
        dotsArea_value = int(str(self.ui.dotsSlider.value()))
        if kernal_value % 2 == 0:
            kernal_value += 1
            self.ui.kernalSlider.setValue(kernal_value)

        widgets.thresh_value.setText(str(thresh_value))
        widgets.blur_value.setText(str(kernal_value))

        img = cv.imread(originalImagePath)
        x = pp.preprocess(img, thresh_value, kernal_value)
        widgets.label.setPixmap(QPixmap(cv2pxi(x)))

    def selectTheImage(self):
        global originalImagePath
        originalImagePath = r"images/source_image"

        # MAKES THE DIRECTORY TO STORE OUR IMAGE IN THE PROJECT
        if not os.path.exists(originalImagePath):
            os.makedirs(originalImagePath)

        widgets.textView.setText("")
        imagePath = QFileDialog.getOpenFileName(self, 'Open file', "", 'Images ( *.png, *.xmp *.jpg)')
        if len(imagePath[0]) == 0:
            widgets.textView.setText("no Image Select")
        else:
            originalImagePath = originalImagePath + "/main_image.png"
            img = cv.imread(imagePath[0])
            cv.imwrite(originalImagePath, img)
            widgets.imageView.setPixmap(QPixmap(originalImagePath))
            widgets.label.setPixmap(QPixmap(originalImagePath))

    # CHANGES THE ANGLE OF THE INPUT IMAGE
    def changeAngel(self):
        angel_value = int(str(self.ui.angelSlider.value()))
        btn = self.sender()
        btnName = btn.objectName()
        img = cv.imread(originalImagePath)

        if btnName == "angelSlider":
            img = pp.rotate_image(img, angel_value)
            widgets.label.setPixmap(QPixmap(cv2pxi(img)))

        elif btnName == "btn_applyRotation":
            img = pp.rotate_image(img, angel_value)
            cv.imwrite(originalImagePath, img)

        elif btnName == "btn_revertRotaion":
            img = pp.rotate_image(img, 0)
            widgets.label.setPixmap(QPixmap(cv2pxi(img)))
            self.ui.angelSlider.setValue(0)

    def changeDotArea(self):
        thresh_value = int(str(self.ui.threshHoldSlider.value()))
        kernal_value = int(str(self.ui.kernalSlider.value()))
        dotsArea_value = int(str(self.ui.dotsSlider.value()))
        widgets.dot_value.setText(str(dotsArea_value))
        img = cv.imread(originalImagePath)
        img = pp.showDots(img, thresh_value, kernal_value, dotsArea_value)
        widgets.label.setPixmap(QPixmap(cv2pxi(img)))


# RECONSTRUCT THE IMAGE FROM NUMPY ARRAY TO PXI IMAGE
# ///////////////////////////////////////////////////////////////
def cv2pxi(img):
    if len(img.shape) < 3:
        frame = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    else:
        frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    bytesPerLine = 3 * w
    img = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
    return img


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
