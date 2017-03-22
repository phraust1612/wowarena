import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests as rq

class wowLadder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = 1
        self.apikey = "ks3xtugk5fdjdvp45h9yyq7756jszzg2"
        self.Reload()
    def initUI(self):
        self.setFixedSize(890,550)
        self.center()
        self.setWindowTitle('wowLadder')
        self.setWindowIcon(QIcon('m2.ico'))
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowTitleHint)

        self.choice = QComboBox(self)
        self.choice.addItem("2v2")
        self.choice.addItem("3v3")
        self.choice.addItem("평전")
        self.choice.addItem("연투")
        self.choice.move(50,50)
        self.choice.activated[str].connect(self.Choose)

        self.fr = []
        self.tx = []
        for i in range(0,10):
            self.fr.append(QFrame(self))
            self.tx.append(QLabel(self))
            self.fr[i].resize(500,48)
            self.fr[i].move(200,20 + 50*i)
            self.tx[i].move(220,28 + 50*i)
            self.fr[i].setStyleSheet("QFrame { background-color: white; border: 1px solid black }")
        self.ShowPage(0)
        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def Choose(self,text):
        if text == "2v2":
            self.mode = 1
            self.ShowPage(0)
        elif text == "3v3":
            self.mode = 2
            self.ShowPage(0)
        elif text == "평전":
            self.mode = 3
            self.ShowPage(0)
        else:
            self.mode = 0
    def Reload(self):
        url = ""
        if self.mode == 1:
            url = "https://kr.api.battle.net/wow/leaderboard/2v2?locale=ko_KR&apikey="
        elif self.mode == 2:
            url = "https://kr.api.battle.net/wow/leaderboard/3v3?locale=ko_KR&apikey="
        elif self.mode == 3:
            url = "https://kr.api.battle.net/wow/leaderboard/rbg?locale=ko_KR&apikey="
        else:
            return -1
        url += self.apikey
        res = rq.get(url)
        if res.status_code >= 200 and res.status_code<300:
            self.ladder = res.json()
            return 0
        else:
            return -2
    def ShowPage(self,no):
        for i in range(0,10):
            tmp = "랭킹 "
            tmp += str(self.ladder['rows'][i]['ranking'])
            tmp += " 위      레이팅 : "
            tmp += str(self.ladder['rows'][i]['rating'])
            tmp += "\n서버 : "
            tmp += self.ladder['rows'][i]['realmName']
            tmp += "    "
            tmp += self.ClassName(self.ladder['rows'][i]['classId'])
            tmp += "    "
            tmp += self.ladder['rows'][i]['name']
            self.tx[i].setText(tmp)
    def ClassName(self, no):
        if no == 1:
            return "전사"
        elif no == 2:
            return "성기사"
        elif no == 3:
            return "사냥꾼"
        elif no == 4:
            return "도적"
        elif no == 5:
            return "사제"
        elif no == 6:
            return "죽음의 기사"
        elif no == 7:
            return "주술사"
        elif no == 8:
            return "마법사"
        elif no == 9:
            return "흑마법사"
        elif no == 10:
            return "수도사"
        elif no == 11:
            return "드루이드"
        elif no == 12:
            return "악마사냥꾼"
        else:
            return "알 수 없음"
    def RaceName(self, no):
        if no == 1:
            return "인간"
        elif no == 2:
            return "오크"
        elif no == 3:
            return "드워프"
        elif no == 4:
            return "나이트 엘프"
        elif no == 5:
            return "언데드"
        elif no == 6:
            return "타우렌"
        elif no == 7:
            return "노움"
        elif no == 8:
            return "트롤"
        elif no == 9:
            return "고블린"
        elif no == 10:
            return "블러드 엘프"
        elif no == 11:
            return "드레나이"
        elif no == 22:
            return "늑대인간"
        elif no == 24 or 25 or 26:
            return "판다렌"
        else:
            return "알 수 없음"

app = QApplication(sys.argv)
MD = wowLadder()
sys.exit(app.exec_())
