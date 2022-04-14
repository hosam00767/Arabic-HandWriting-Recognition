import sys
import os
import cv2 as cv
import platform
import numpy as np
import glob
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide6 import QtGui

from modules import *
from widgets import *
from imageManipultation import preprocessing as pp
from imageManipultation import segmentaion_to_paws as stp
from imageManipultation import segmentation_to_lines as stl

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL VARIABLE
# ///////////////////////////////////////////////////////////////
widgets = None
originalImagePath = None

# IMAGE ATTRIBUTE VALUES
# ///////////////////////////////////////////////////////////////
THRESHOLD_VALUE = 127
DOT_AREA_VALUE = 50
BLUR_KERNEL_VALUE = 3




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
        widgets.btn_home.clicked.connect(self.leftMenuButtonPressed)
        widgets.btn_preprocessing.clicked.connect(self.leftMenuButtonPressed)
        widgets.btn_segmentation.clicked.connect(self.leftMenuButtonPressed)

        widgets.btn_select.clicked.connect(self.selectTheImage)

        widgets.btn_revertRotaion.clicked.connect(self.changeAngel)
        widgets.btn_applyRotation.clicked.connect(self.changeAngel)
        widgets.thresholdSlider.valueChanged.connect(self.number_changed)
        widgets.kernelSlider.valueChanged.connect(self.number_changed)
        widgets.angelSlider.valueChanged.connect(self.changeAngel)
        widgets.dotsSlider.valueChanged.connect(self.changeDotArea)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # MENU BUTTONS FUNCTION
    # ///////////////////////////////////////////////////////////////

    def allInOne(self):
        global originalImagePath
        global DOT_AREA_VALUE
        image = cv.imread(originalImagePath)
        preprocessedOriginal = pp.preprocess(image, THRESHOLD_VALUE, BLUR_KERNEL_VALUE)
        stl.segment_to_line(image)
        paths = glob.glob('images/lines/*')
        for path in paths:
            self.createLinesListItem(path)
            lineNo = getFileName(path)
            stp.segment_img_to_PAWS(path, lineNo, DOT_AREA_VALUE)


    def createLinesListItem(self, linePath):

        lineNum = getFileName(linePath)
        # CREATING THE FRAME AND ITS ATTRIBUTES
        self.listItemFrame = QFrame(self.ui.scrollAreaWidgetContents)
        self.listItemFrame.setObjectName(u"frame_9")
        self.listItemFrame.setMinimumSize(QSize(0, 100))
        self.listItemFrame.setFrameShape(QFrame.StyledPanel)
        self.listItemFrame.setFrameShadow(QFrame.Raised)

        # CREATING THE LAYOUT INSIDE THE FRAME
        self.frameLayout = QHBoxLayout(self.listItemFrame)
        self.frameLayout.setObjectName(u"horizontalLayout_12")

        self.label_6 = QLabel(self.listItemFrame)
        self.label_6.setObjectName(u"label_6")
        sizePolicy7 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy7)
        self.label_6.setMinimumSize(QSize(0, 100))
        self.label_6.setPixmap(QPixmap(linePath))
        self.label_6.setScaledContents(True)
        self.frameLayout.addWidget(self.label_6)

        # CREATING THE SEGMENTATION TO WORDS BUTTON IN THE LIST ITEM
        self.btn_sgmnt2Words = QPushButton(self.listItemFrame)
        self.btn_sgmnt2Words.setObjectName(u"seg_btn_" + str(lineNum))
        self.btn_sgmnt2Words.clicked.connect(self.word_sgmnt_clicked)
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btn_sgmnt2Words.sizePolicy().hasHeightForWidth())
        self.btn_sgmnt2Words.setSizePolicy(sizePolicy6)
        self.btn_sgmnt2Words.setMinimumSize(QSize(35, 35))
        icon3 = QIcon()
        icon3.addFile(u"images/icons/cil-cut.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_sgmnt2Words.setIcon(icon3)
        self.frameLayout.addWidget(self.btn_sgmnt2Words)

        self.ui.verticalLayout_13.addWidget(self.listItemFrame)

    def word_sgmnt_clicked(self):

        btn = self.sender()
        btnName = btn.objectName()

        lineNo = int(''.join(filter(str.isdigit, btnName)))
        print("you Pressed line " + str(lineNo))

    # CHANGES THE PAGE TO THE SELECTED FROM MENU BUTTON
    # ///////////////////////////////////////////////////////////////
    def leftMenuButtonPressed(self):

        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_home":  # SHOW HOME PAGE
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        elif btnName == "btn_preprocessing":  # SHOW PREPROCESSING PAGE
            widgets.stackedWidget.setCurrentWidget(widgets.preprocessing_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        elif btnName == "btn_segmentation":  # SHOW THE SEGMENTATION PAGE
            widgets.stackedWidget.setCurrentWidget(widgets.segmentation_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # DRAG THE APPLICATION FUNCTION
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def number_changed(self):

        global BLUR_KERNEL_VALUE, DOT_AREA_VALUE, THRESHOLD_VALUE
        global originalImagePath

        slider = self.sender()
        sliderName = slider.objectName()

        if sliderName == "kernelSlider":
            kernel_value = int(str(self.ui.thresholdSlider.value()))
            if kernel_value % 2 == 0:
                kernel_value += 1
                BLUR_KERNEL_VALUE = kernel_value
                self.ui.kernalSlider.setValue(kernel_value)

        elif sliderName == "thresholdSlider":
            THRESHOLD_VALUE = int(str(self.ui.thresholdSlider.value()))

        widgets.thresh_value.setText(str(THRESHOLD_VALUE))
        widgets.blur_value.setText(str(BLUR_KERNEL_VALUE))

        img = cv.imread(originalImagePath)
        preProcessedImg = pp.preprocess(img, THRESHOLD_VALUE, BLUR_KERNEL_VALUE)
        widgets.label.setPixmap(QPixmap(cv2pxi(preProcessedImg)))

    # SELECT IMAGE BUTTON FUNCTION FROM THE MAIN PAGE
    # ///////////////////////////////////////////////////////////////
    def selectTheImage(self):
        global originalImagePath
        originalImagePath = r"images/source_image"

        if not os.path.exists(originalImagePath):  # MAKES THE DIRECTORY TO STORE OUR IMAGE IN THE PROJECT
            os.makedirs(originalImagePath)

        imagePath = QFileDialog.getOpenFileName(self, 'Open file', "", 'Images ( *.png, *.xmp *.jpg)')
        if imagePath[0] == "":
            QMessageBox.warning(self, 'NO IMAGE IS SELECTED', 'Please select an Image')
        else:

            originalImagePath = originalImagePath + "/main_image.png"
            img = cv.imread(imagePath[0])
            cv.imwrite(originalImagePath, img)

            self.allInOne()
            widgets.imageView.setPixmap(QPixmap(originalImagePath))
            widgets.label.setPixmap(QPixmap(originalImagePath))

    # CHANGES THE ANGLE OF THE INPUT IMAGE
    # ///////////////////////////////////////////////////////////////
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
        global BLUR_KERNEL_VALUE, DOT_AREA_VALUE, THRESHOLD_VALUE

        DOT_AREA_VALUE = int(str(self.ui.dotsSlider.value()))
        widgets.dot_value.setText(str(DOT_AREA_VALUE))
        img = cv.imread(originalImagePath)
        img = pp.showDots(img, THRESHOLD_VALUE, BLUR_KERNEL_VALUE, DOT_AREA_VALUE)
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


# RETURN THE FILE PATH FROM A CERTAIN DIRECTORY
# ///////////////////////////////////////////////////////////////
def getFilesDirectories(dir_path):
    pathes = []
    for path in os.listdir(dir_path):
        full_path = os.path.join(dir_path, path)
        if os.path.isfile(full_path):
            pathes.append(full_path)
    return pathes


# DELETE ALL THE IMAGE IN IMAGES , PAWS , LINES DIRECTORIES
# ///////////////////////////////////////////////////////////////
def clearDirectories():
    files = glob.glob('images/lines/*')
    files.extend(glob.glob('images/source_image/*'))
    files.extend(glob.glob('images/paws/*'))
    for f in files:
        os.remove(f)


# GET FILE NAME FROM A PATH
# ///////////////////////////////////////////////////////////////
def getFileName(path):
    pathOnly, _ = os.path.splitext(path)
    fileName = os.path.basename(pathOnly)
    return fileName


if __name__ == "__main__":
    clearDirectories()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())

# WARNING BOX SAVED FOR LATE IMPLEMENTAION
