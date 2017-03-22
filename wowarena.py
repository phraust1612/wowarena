import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests as rq

class wowLadder(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = 0
        self.totalNo = 0
        self.initUI()
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
        self.choice.move(50,50)
        self.choice.activated[str].connect(self.Choose)

        self.fr = []
        self.tx = []
        self.pg = []
        for i in range(0,10):
            self.fr.append(QFrame(self))
            self.tx.append(QLabel(self))
            self.pg.append(QPushButton(self))
            self.fr[i].resize(500,48)
            self.fr[i].move(200,20 + 50*i)
            self.tx[i].move(220,30 + 50*i)
            self.pg[i].resize(20,20)
            self.pg[i].move(215 + 50*i, 520)
            self.pg[i].setText(str(i+1))
            self.pg[i].setStyleSheet("border: 0px")
            self.fr[i].setStyleSheet("QFrame { background-color: white; border: 1px solid black }")
        self.pg[0].clicked.connect(lambda: self.PageChoose(0))
        self.pg[1].clicked.connect(lambda: self.PageChoose(1))
        self.pg[2].clicked.connect(lambda: self.PageChoose(2))
        self.pg[3].clicked.connect(lambda: self.PageChoose(3))
        self.pg[4].clicked.connect(lambda: self.PageChoose(4))
        self.pg[5].clicked.connect(lambda: self.PageChoose(5))
        self.pg[6].clicked.connect(lambda: self.PageChoose(6))
        self.pg[7].clicked.connect(lambda: self.PageChoose(7))
        self.pg[8].clicked.connect(lambda: self.PageChoose(8))
        self.pg[9].clicked.connect(lambda: self.PageChoose(9))
        self.pg[0].setStyleSheet("color: red; border: 0px")
        self.currentPageNo = 0
        self.show()
        self.mode = 1
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def Choose(self,text):
        if text == "2v2":
            self.mode = 1
        elif text == "3v3":
            self.mode = 2
        elif text == "평전":
            self.mode = 3
        else:
            self.mode = 0
            return
        self.Reload()
    def PageChoose(self,no):
        i = int(self.pg[no].text())
        if i<5:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.pg[no].setStyleSheet("color: red; border: 0px")
            self.currentPageNo = no
        elif i>=5 and i<self.maxPageNo-6:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.pg[3].setStyleSheet("color: red; border: 0px")
            self.currentPageNo = 3
            self.pg[1].setText("...")
            self.pg[2].setText(str(i-1))
            self.pg[3].setText(str(i))
            self.pg[4].setText(str(i+1))
            self.pg[5].setText(str(i+2))
            self.pg[6].setText(str(i+3))
            self.pg[7].setText(str(i+4))
            self.pg[8].setText("...")
            self.pg[9].setText(str(self.maxPageNo))
        else:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.pg[no].setStyleSheet("color: red; border: 0px")
            
        self.ShowPage(i)
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
            self.totalNo = len(self.ladder['rows'])
            self.maxPageNo = int((self.totalNo-1)/10)+1
            self.ShowPage(1)
            return 0
        else:
            return -2
    def ShowPage(self,no):
        try:
            self.ladder
        except AttributeError:
            return
        i = no - 1
        i *= 10
        count = 0
        while count<10 and i<self.totalNo:
            tmp = "랭킹 "
            tmp += str(self.ladder['rows'][i]['ranking'])
            tmp += " 위      레이팅 : "
            tmp += str(self.ladder['rows'][i]['rating'])
            tmp += "\n서버 : "
            tmp += self.ladder['rows'][i]['realmName']
            tmp += "          "
            tmp += self.ClassName(self.ladder['rows'][i]['classId'])
            tmp += "    "
            tmp += self.ladder['rows'][i]['name']
            self.tx[count].setText(tmp)
            self.tx[count].adjustSize()
            count += 1
            i += 1
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
            return str(no)
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
            return str(no)

app = QApplication(sys.argv)
MD = wowLadder()
sys.exit(app.exec_())
