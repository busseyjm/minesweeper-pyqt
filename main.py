import sys

from PyQt5.QtCore import Qt
from minesweepergame import game
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,
QPushButton, QGridLayout)

MINESWEEPER_GAME_SIZE_X = 30
MINESWEEPER_GAME_SIZE_Y = 16

class mainboard(QWidget):
    gameinst = game()

    def __init__(self):
        super().__init__()
        self.initUI()

    def clickhandler(self):
        sender = self.sender()
        pos_y = sender.property("y_coord")
        pos_x = sender.property("x_coord")

        if QApplication.mouseButtons() & Qt.RightButton:
            self.gameinst.clicked(pos_y, pos_x, True)
        else:
            self.gameinst.clicked(pos_y, pos_x, False)

    def initUI(self):   
        grid = QGridLayout()  
        self.setLayout(grid)

        positions = [(i, j) for i in range(MINESWEEPER_GAME_SIZE_Y) for j in range(MINESWEEPER_GAME_SIZE_X)]

        for position in positions:
            button = QPushButton()

            #set a property containing the coordinates of the button
            button.setProperty("y_coord", position[0])
            button.setProperty("x_coord", position[1])

            #connect to a click handler
            button.clicked.connect(self.clickhandler)

            #allow right clicks on buttons
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(self.clickhandler)

            #add the button to the game
            self.gameinst.addbutton(positions[0],positions[1],button)

            #add the button to the ui
            grid.addWidget(button, *position)

        #self.gameinst.generategame(positions[0], positions[1], .5)
        self.gameinst.generategame("EXPERT")
        self.gameinst.calculatebackend()
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
    ex = mainboard()
    sys.exit(app.exec_())    