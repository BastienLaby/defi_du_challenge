# -*- coding: utf-8 -*-

import random
import time

import lib.easyqt as eqt
from PySide import QtCore


class Game(object):
    def __init__(self, name):
        self.name = name
        self.revealed = False

    def getDisplay(self):
        if self.revealed:
            return self.name
        return ''.join(['_ ' if i != ' ' else ' ' for i in self.name])


class DefiDuChallengeWindow(eqt.EasyWindow):

    def __init__(self):
        super(DefiDuChallengeWindow, self).__init__()
        self.setWindowTitle('Defi du challenge')

        self.games = []
        self.games.append(Game('MARIO KART DOUBLE DASH'))
        self.games.append(Game('GENITAL JOUSTING'))
        self.games.append(Game('BASKHEAD'))
        self.currentGameIndex = 0

        self.widget = eqt.EasyWidget()

        self.displayText = eqt.EasyLabel('DEFI DU CHALLENGE !')
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.displayGame)

        self.goButton = eqt.EasyPushButton('GO', clicked=self.revealNextGame)
        self.resetButton = eqt.EasyPushButton('RESET', clicked=self.reset)

        self.widget.addWidgets(self.displayText, self.goButton, self.resetButton)

        self.setCentralWidget(self.widget)

        self.show()

    def displayGame(self):

        if time.time() - self.displayStartTime > 3 and not self.games[self.currentGameIndex].revealed:

            self.games[self.currentGameIndex].revealed = True
            self.displayText.setText('>>' + self.games[self.currentGameIndex].getDisplay() + ' !!')
            self.timer.stop()
            self.goButton.setEnabled(any(not i.revealed for i in self.games))

        else:

            self.displayText.setText(self.games[self.currentGameIndex].getDisplay())
            self.currentGameIndex = (self.currentGameIndex + 1) % len(self.games)
            self.timer.setInterval(self.timer.interval() * 1.1)


    def revealNextGame(self):
        self.displayStartTime = time.time()
        self.currentGameIndex = random.randint(0, len(self.games) - 1)
        self.goButton.setEnabled(False)
        self.timer.start(500)

    def reset(self):
        for i in self.games:
            i.revealed = False
        self.goButton.setEnabled(True)



if __name__ == '__main__':
    app = eqt.EasyApplication()
    window = DefiDuChallengeWindow()
    app.exec_()



