import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,
QPushButton, QGridLayout)



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def msgexternal(self):
        sender = self.sender()
        pos = sender.property("coords")
        print(pos)
        #reply = QMessageBox.question(self, 'Clicked', 'You clicked: ' + str(pos[0]) + ' ' + str(pos[1]),
        #QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def initUI(self):   
        grid = QGridLayout()  
        self.setLayout(grid)

        sizex = 10
        sizey = 10

        positions = [(i, j) for i in range(sizex) for j in range(sizey)]

        #for position, name in zip(positions, names):
        for position in positions:
            button = QPushButton(str(position[0]))
        #  button.clicked.connect(self.close)
            print(id(position))
            button.setProperty("coords", position)
            print(button.property("coords"))
            button.clicked.connect(self.msgexternal)
            #button.clicked.connect(lambda: self.msgexternal(position[0], position[1]))
            grid.addWidget(button, *position)

        self.move(300, 150)
        self.setWindowTitle('PyQt Minesweeper')  
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())    