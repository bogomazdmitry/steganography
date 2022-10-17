from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import sys
import cv2

from methods import decrypt, encrypt


class Ui(QtWidgets.QMainWindow):
    firstImage = None
    secondImage = None
    KEY_FOR_RANDOM = 1586

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.pushButtonImport.clicked.connect(self.pushButtonImportClick)
        self.pushButtonSave.clicked.connect(self.pushButtonSaveClick)
        self.pushButtonEncrypt.clicked.connect(self.pushButtonEncryptClick)
        self.pushButtonDecrypt.clicked.connect(self.pushButtonDecryptClick)

        self.show()

    def pushButtonImportClick(self):
        path = QFileDialog.getOpenFileName(self, 'Открыть изображение', '.', 'Image files (*.png)')
        if path[0] != '':
            self.firstImage = cv2.imread(path[0])
            QPixmap(path[0])
            self.graphicsViewFirst.setPixmap(self.convertOpenCvImageToQPixmap(self.firstImage))
            self.secondImage = None
            self.labelFirst.setText(path[0])
            self.labelSecond.setText('')
            self.plainTextEditInformation.setPlainText('')
            self.graphicsViewSecond.clear()

    def pushButtonSaveClick(self):
        if self.secondImage is None:
            self.errorBox('Изображения для сохранения нет!')
            return

        path = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'Image files (*.png)')
        if path[0] != '':
            cv2.imwrite(path[0], self.secondImage)
            self.labelSecond.setText(path[0])

    def pushButtonEncryptClick(self):
        if self.firstImage is None:
            self.errorBox('Загрузите изображение!')
            return

        information = self.plainTextEditInformation.toPlainText()
        if information == '':
            self.errorBox('Впишите информацию!')
            return

        newImage = encrypt(self.firstImage,
            self.KEY_FOR_RANDOM,
            self.spinBoxCountRepeat.value(),
            self.doubleSpinBoxBrightness.value(),
            information)

        self.secondImage = newImage
        self.graphicsViewSecond.setPixmap(self.convertOpenCvImageToQPixmap(self.secondImage))

        self.successBox('Информация успешно вставлена')

    def pushButtonDecryptClick(self):
        if self.firstImage is None:
            self.errorBox('Загрузите изображение!')
            return

        information = decrypt(self.firstImage,
            self.KEY_FOR_RANDOM,
            self.spinBoxCountRepeat.value(),
            self.doubleSpinBoxBrightness.value(),
            self.spinBoxSizeBlock.value())

        self.plainTextEditInformation.setPlainText(information)
        self.secondImage = None

        self.successBox('Информация успешно получена')

    def errorBox(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Ошибка!")
        dlg.setText(message)
        dlg.exec()

    def successBox(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Успех!")
        dlg.setText(message)
        dlg.exec()

    def convertOpenCvImageToQPixmap(self, opencvImage):
        height, width, channel = opencvImage.shape
        bytesPerLine = 3 * width
        qImg = QImage(opencvImage.data, width, height, bytesPerLine, QImage.Format.Format_BGR888)
        return QPixmap(qImg)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()