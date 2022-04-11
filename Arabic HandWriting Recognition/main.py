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

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL VARIABLE
# ///////////////////////////////////////////////////////////////
widgets = None
imagePath = None
original_image = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

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
        widgets.threshHoldSlider.valueChanged.connect(self.number_changed)
        widgets.kernalSlider.valueChanged.connect(self.number_changed)
        widgets.angelSlider.valueChanged.connect(self.changeAngel)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # MENU BUTTONS FUNCTION
    # ///////////////////////////////////////////////////////////////
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
        global imagePath
        thresh_value = int(str(self.ui.threshHoldSlider.value()))
        kernal_value = int(str(self.ui.kernalSlider.value()))
        if kernal_value % 2 == 0:
            kernal_value += 1

        img = cv.imread(imagePath[0])
        x = pp.preprocess(img, thresh_value, kernal_value)
        widgets.label.setPixmap(QPixmap(cv2pxi(x)))

    def selectTheImage(self):
        originalImagePath = r"images/source_image"
        global imagePath
        if not os.path.exists(originalImagePath):
            os.makedirs(originalImagePath)

        widgets.textView.setText("")
        imagePath = QFileDialog.getOpenFileName(self, 'Open file', "", 'Images (*.png, *.xmp *.jpg)')
        if len(imagePath[0]) == 0:
            widgets.textView.setText("no Image Select")
        else:
            newPath=originalImagePath+"/main_image.png"
            img = cv.imread(imagePath[0])
            cv.imwrite(newPath, img)

            widgets.imageView.setPixmap(QPixmap(newPath))
            widgets.label.setPixmap(QPixmap(newPath))

    def changeAngel(self):
        angel_value = int(str(self.ui.angelSlider.value()))
        img = cv.imread(imagePath[0])
        img = pp.rotate_image(img, angel_value)
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
