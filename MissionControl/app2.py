#Pyside App test

import sys
import PySide as pyside
from PySide.QtGui import QApplication
from PySide.QtGui import QMessageBox


app = QApplication(sys.argv)

msgBox = QMessageBox()
msgBox.setText("Hello World!")
msgBox.exec_()