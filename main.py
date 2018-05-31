# -*- coding: utf-8 -*-

import random
import time
import json

import lib.easyqt as eqt
from PySide import QtCore, QtGui


class Game(object):
    def __init__(self, name, revealedImg, nonRevealedImg):
        self.name = name
        self.revealedImg = revealedImg
        self.nonRevealedImg = nonRevealedImg
        self.revealedPix = QtGui.QPixmap(revealedImg)
        self.nonRevealedPix = QtGui.QPixmap(nonRevealedImg)
        self.revealed = False

    def getDisplay(self):
        if self.revealed:
            return self.revealedPix
        return self.nonRevealedPix


class DefiDuChallengeWindow(eqt.EasyWindow):

    def __init__(self, session):
        super(DefiDuChallengeWindow, self).__init__()
        self.setWindowTitle('Defi du challenge')

        with open(session, 'r') as f:
            session = json.load(f)

        self.games = []
        for k, v in session['games'].iteritems():
            self.games.append(Game(k, v['revealed'], v['nonRevealed']))

        self.currentGameIndex = 0
        self.revealationDuration = 10
        self.mainPix = QtGui.QPixmap(session['main'])

        self.widget = eqt.EasyWidget()
        self.displayText = eqt.EasyLabel('')
        self.displayText.setPixmap(self.mainPix)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.displayGame)
        self.goButton = eqt.EasyPushButton('GO', clicked=self.revealNextGame)
        self.resetButton = eqt.EasyPushButton('RESET', clicked=self.reset)
        self.widget.addWidgets(self.displayText, self.goButton, self.resetButton)
        self.setCentralWidget(self.widget)

        self.show()

    def displayGame(self):

        if time.time() - self.displayStartTime > self.revealationDuration and not self.games[self.currentGameIndex].revealed:

            self.games[self.currentGameIndex].revealed = True
            self.displayText.setPixmap(self.games[self.currentGameIndex].getDisplay())
            self.timer.stop()
            self.goButton.setEnabled(any(not i.revealed for i in self.games))
            QtGui.QSound.play('sounds/reveal.wav')

        else:
            self.displayText.setPixmap(self.games[self.currentGameIndex].getDisplay())
            self.currentGameIndex = (self.currentGameIndex + 1) % len(self.games)
            self.timer.setInterval(self.timer.interval() * 1.1)
            QtGui.QSound.play('sounds/tick.wav')

    def revealNextGame(self):
        self.displayStartTime = time.time()
        self.currentGameIndex = random.randint(0, len(self.games) - 1)
        self.goButton.setEnabled(False)
        self.timer.start(300)

    def reset(self):
        for i in self.games:
            i.revealed = False
        self.goButton.setEnabled(True)
        self.timer.stop()
        self.displayText.setPixmap(self.mainPix)


if __name__ == '__main__':
    app = eqt.EasyApplication()
    window = DefiDuChallengeWindow('sessions/session1.json')
    app.exec_()



