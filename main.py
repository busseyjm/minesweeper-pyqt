import sys

from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QSize
from minesweepergame import game
from PyQt5.QtWidgets import (QAbstractButton, QApplication, QLabel, QWidget, QMessageBox,
QPushButton, QGridLayout)
from PyQt5.QtGui import QIcon

MINESWEEPER_GAME_SIZE_X = 30
MINESWEEPER_GAME_SIZE_Y = 16
MINESWEEPER_GAME_DIFFICULTY = "EXPERT"

#multithreaded board update
class BoardRefresh(QRunnable):
    def __init__(self, buttons, changes):
        self.buttons = buttons
        self.changes = changes
        super().__init__()

    def run(self):
        #for y, x in self.buttons:
        for y, x in self.changes:
            if (self.changes[y,x] == 'U'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_00.png"))
                continue

            if (self.changes[y,x] == 'E'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_01.png"))
                continue

            if (self.changes[y,x] == 'F'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_02.png"))
                continue

            if (self.changes[y,x] == 'B'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_05.png"))
                continue

            if (self.changes[y,x] == 'C'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_06.png"))
                continue

            if (self.changes[y,x] == 'W'):
                self.buttons[y,x].setIcon(QIcon("assets/minesweeper_07.png"))
                continue

            # somewhat hacky way of translating the number into a filename
            #   the '1' icon is _08.png
            #   the '8' icon is _15.png
            iconstr = ""
            if (self.changes[y,x] in range(1,3)):
                iconstr = "0" + str(self.changes[y,x]+7)
            else:
                iconstr = str(self.changes[y,x]+7)
            self.buttons[y,x].setIcon(QIcon("assets/minesweeper_" + iconstr + ".png"))


class mainboard(QWidget):
    buttons = {}
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
        #QApplication.processEvents()
        self.refreshboard()

    def refreshboard(self):
        pool = QThreadPool.globalInstance()
        #refresh = BoardRefresh(self.buttons, self.gameinst.getboardfront())
        refresh = BoardRefresh(self.buttons, self.gameinst.getchanges())
        pool.start(refresh)

    def initUI(self):   
        grid = QGridLayout()  
        self.setLayout(grid)
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)

        positions = [(i, j) for i in range(MINESWEEPER_GAME_SIZE_Y) for j in range(MINESWEEPER_GAME_SIZE_X)]

        for position in positions:
            button = QPushButton()

            #button appearance settings
            button.setMinimumWidth(32)
            button.setMinimumHeight(32)
            button.setFixedHeight(32)
            button.setFixedWidth(32)
            button.setFlat(True)
            button.setIconSize(QSize(32,32))
            button.setIcon(QIcon("assets/minesweeper_00.png"))

            #set a property containing the coordinates of the button
            button.setProperty("y_coord", position[0])
            button.setProperty("x_coord", position[1])
            button.setProperty("coords", position)

            #connect to a click handler
            button.clicked.connect(self.clickhandler)

            #allow right clicks on buttons
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(self.clickhandler)

            #add the button to the game
            #self.gameinst.addbutton(position[0],position[1],button)
            self.buttons[position] = button

            #add the button to the ui
            grid.addWidget(button, *position)

        #self.gameinst.generategame(positions[0], positions[1], .5)
        self.gameinst.generategame(MINESWEEPER_GAME_DIFFICULTY)
        self.move(300, 150)
        self.setWindowTitle('PyQt Minesweeper')  
        #self.setFixedSize(self.size())
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
    mainboard.gameinst.debugprint()
    sys.exit(app.exec_())    