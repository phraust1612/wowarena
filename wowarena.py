import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests as rq
import urllib.request
import time

class wowLadder(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = 0
        self.totalNo = 0
        self.indexNo = 0
        self.initUI()
        self.apikey = "ks3xtugk5fdjdvp45h9yyq7756jszzg2"
    def initUI(self):
        self.setFixedSize(720,550)
        self.center()
        self.setWindowTitle('wowLadder')
        self.setWindowIcon(QIcon('img/m2.ico'))
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowTitleHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.choice = QComboBox(self)
        self.choice.addItem("선택하세요")
        self.choice.addItem("2v2")
        self.choice.addItem("3v3")
        self.choice.addItem("평전")
        self.choice.move(50,50)
        self.choice.activated[str].connect(self.Choose)

        self.searchName = QLineEdit(self)
        self.searchName.move(20,280)
        self.searchName.resize(120,20)
        self.searchGo = QPushButton(self)
        self.searchGo.move(140,280)
        self.searchGo.resize(40,20)
        self.searchGo.setText("검색")
        self.searchGo.clicked.connect(self.Search)

        self.fr = []
        self.tx = []
        self.pg = []
        self.profile = QPushButton(self)
        self.profile.resize(500,500)
        self.profile.move(200,20)
        self.profile.setStyleSheet("background-color: white; border: 1px solid black")
        self.profile.hide()
        self.prbg = QLabel(self.profile)
        self.prbg.resize(500,500)
        self.prtitle = QLabel(self.profile)
        self.prtitle.move(20,65)
        self.prtitle.setStyleSheet("background-color: rgba(255,255,255,0.5) ;font: 24px arial bold ; border: 0")
        self.prredtitle = QLabel(self.profile)
        self.prredtitle.move(20,20)
        self.prredtitle.setStyleSheet("background-color: rgba(255,255,255,0.5) ; color: red; font: 30px arial bold ; border: 0")
        self.prbluetitle = QLabel(self.profile)
        self.prbluetitle.move(250,65)
        self.prbluetitle.setStyleSheet("background-color: rgba(255,255,255,0.5) ; color: blue; font: 24px arial bold ; border: 0")
        self.prtext = QLabel(self.profile)
        self.prtext.move(20,100)
        self.prtext.setStyleSheet("background-color: rgba(255,255,255,0.5) ;font: 14px arial ; border: 0")
        self.thumbnail = QLabel(self)
        self.thumbnail.move(50,100)
        self.thumbnail.resize(84,84)
        
        for i in range(0,10):
            self.fr.append(QPushButton(self))
            self.tx.append(QLabel(self.fr[i]))
            self.pg.append(QPushButton(self))
            self.fr[i].resize(500,48)
            self.fr[i].move(200,20 + 50*i)
            self.tx[i].move(5,10)
            self.pg[i].resize(20,20)
            self.pg[i].move(215 + 50*i, 520)
            self.pg[i].setText("")
            self.pg[i].setStyleSheet("border: 0px")
            self.tx[i].setStyleSheet("border: 0px")
            self.fr[i].setStyleSheet("background-color: white; border: 1px solid black")
            self.fr[i].hide()
            
        self.pg[0].setStyleSheet("color: red; border: 0px")
        self.currentPageNo = 0
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
        self.fr[0].clicked.connect(lambda: self.SeeProfile(0))
        self.fr[1].clicked.connect(lambda: self.SeeProfile(1))
        self.fr[2].clicked.connect(lambda: self.SeeProfile(2))
        self.fr[3].clicked.connect(lambda: self.SeeProfile(3))
        self.fr[4].clicked.connect(lambda: self.SeeProfile(4))
        self.fr[5].clicked.connect(lambda: self.SeeProfile(5))
        self.fr[6].clicked.connect(lambda: self.SeeProfile(6))
        self.fr[7].clicked.connect(lambda: self.SeeProfile(7))
        self.fr[8].clicked.connect(lambda: self.SeeProfile(8))
        self.fr[9].clicked.connect(lambda: self.SeeProfile(9))
        self.profile.clicked.connect(lambda: self.PageChoose(self.currentPageNo))
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
        try:
            i = int(self.pg[no].text())
        except ValueError:
            i=1
        self.profile.hide()
        if i<6:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.currentPageNo = i-1
            self.pg[self.currentPageNo].setStyleSheet("color: red; border: 0px")
            self.pg[0].setText(str(1))
            self.pg[1].setText(str(2))
            self.pg[2].setText(str(3))
            self.pg[3].setText(str(4))
            self.pg[4].setText(str(5))
            self.pg[5].setText(str(6))
            self.pg[6].setText(str(7))
            self.pg[7].setText(str(8))
            self.pg[8].setText("...")
            self.pg[9].setText(str(self.maxPageNo))
        elif i>=6 and i<self.maxPageNo-6:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.currentPageNo = 4
            self.pg[self.currentPageNo].setStyleSheet("color: red; border: 0px")
            self.pg[0].setText(str(1))
            self.pg[1].setText("...")
            self.pg[2].setText(str(i-2))
            self.pg[3].setText(str(i-1))
            self.pg[4].setText(str(i))
            self.pg[5].setText(str(i+1))
            self.pg[6].setText(str(i+2))
            self.pg[7].setText(str(i+3))
            self.pg[8].setText("...")
            self.pg[9].setText(str(self.maxPageNo))
        else:
            self.pg[self.currentPageNo].setStyleSheet("color: black; border: 0px")
            self.currentPageNo = 9 - self.maxPageNo + i
            self.pg[self.currentPageNo].setStyleSheet("color: red; border: 0px")
            self.pg[0].setText(str(1))
            self.pg[1].setText("...")
            self.pg[2].setText(str(self.maxPageNo-7))
            self.pg[3].setText(str(self.maxPageNo-6))
            self.pg[4].setText(str(self.maxPageNo-5))
            self.pg[5].setText(str(self.maxPageNo-4))
            self.pg[6].setText(str(self.maxPageNo-3))
            self.pg[7].setText(str(self.maxPageNo-2))
            self.pg[8].setText(str(self.maxPageNo-1))
            self.pg[9].setText(str(self.maxPageNo))
        self.ShowPage(i)
    def SeeProfile(self,no):
        for i in range(0,10):
            self.fr[i].hide()
        i = int(self.pg[self.currentPageNo].text())
        index = (i-1) * 10 + no
        
        name = self.ladder['rows'][index]['name']
        realm = self.ladder['rows'][index]['realmName']
        classno = self.ladder['rows'][index]['classId']
        classname = self.ClassName(classno)
        classimg = self.ClassRoute(classno)
        raceno = self.ladder['rows'][index]['raceId']
        race = self.RaceName(raceno)
        specno = self.ladder['rows'][index]['specId']
        spec = self.SpecName(specno)
        rating = self.ladder['rows'][index]['rating']
        ranking = self.ladder['rows'][index]['ranking']

        tmpstr = "랭킹 "+str(ranking)+" 위!!!"
        self.prredtitle.setText(tmpstr)
        self.prredtitle.adjustSize()

        tmpstr = spec+" "+classname
        tmplen = len(tmpstr) - 0.5
        if classno==6:
            tmplen -= 0.5
        self.prtitle.setText(tmpstr)
        self.prtitle.adjustSize()

        self.prbluetitle.move(20+24*tmplen,65)
        self.prbluetitle.setText(name)
        self.prbluetitle.adjustSize()

        url = "https://kr.api.battle.net/wow/character/"
        url += realm +"/" + name + "?fields=pvp&locale=ko_KR&apikey=" + self.apikey
        res = rq.get(url)
        if res.status_code >= 200 and res.status_code<300:
            js = res.json()
            lasttime = js['lastModified']
            lasttime /= 1000
            tstruct = time.localtime(lasttime)
            date = self.TimeStr(tstruct)
            kills = js['totalHonorableKills']
            achiev = js['achievementPoints']
            
            rating22 = js['pvp']['brackets']['ARENA_BRACKET_2v2']['rating']
            weekP22 = js['pvp']['brackets']['ARENA_BRACKET_2v2']['weeklyPlayed']
            weekW22 = js['pvp']['brackets']['ARENA_BRACKET_2v2']['weeklyWon']
            seasonP22 = js['pvp']['brackets']['ARENA_BRACKET_2v2']['seasonPlayed']
            seasonW22 = js['pvp']['brackets']['ARENA_BRACKET_2v2']['seasonWon']
            try:
                weekR22 = round(100 * weekW22 / weekP22, 2)
            except ZeroDivisionError:
                weekR22 = 0
            try:
                seasonR22 = round(100 * seasonW22 / seasonP22, 2)
            except ZeroDivisionError:
                seasonR22 = 0
            
            rating33 = js['pvp']['brackets']['ARENA_BRACKET_3v3']['rating']
            weekP33 = js['pvp']['brackets']['ARENA_BRACKET_3v3']['weeklyPlayed']
            weekW33 = js['pvp']['brackets']['ARENA_BRACKET_3v3']['weeklyWon']
            seasonP33 = js['pvp']['brackets']['ARENA_BRACKET_3v3']['seasonPlayed']
            seasonW33 = js['pvp']['brackets']['ARENA_BRACKET_3v3']['seasonWon']
            try:
                weekR33 = round(100 * weekW33 / weekP33, 2)
            except ZeroDivisionError:
                weekR33 = 0
            try:
                seasonR33 = round(100 * seasonW33 / seasonP33, 2)
            except ZeroDivisionError:
                seasonR33 = 0
            
            ratingRBG = js['pvp']['brackets']['ARENA_BRACKET_RBG']['rating']
            weekPRBG = js['pvp']['brackets']['ARENA_BRACKET_RBG']['weeklyPlayed']
            weekWRBG = js['pvp']['brackets']['ARENA_BRACKET_RBG']['weeklyWon']
            seasonPRBG = js['pvp']['brackets']['ARENA_BRACKET_RBG']['seasonPlayed']
            seasonWRBG = js['pvp']['brackets']['ARENA_BRACKET_RBG']['seasonWon']
            try:
                weekRRBG = round(100 * weekWRBG / weekPRBG, 2)
            except ZeroDivisionError:
                weekRRBG = 0
            try:
                seasonRRBG = round(100 * seasonWRBG / seasonPRBG, 2)
            except ZeroDivisionError:
                seasonRRBG = 0
            
            ratingSKR = js['pvp']['brackets']['ARENA_BRACKET_2v2_SKIRMISH']['rating']
            weekPSKR = js['pvp']['brackets']['ARENA_BRACKET_2v2_SKIRMISH']['weeklyPlayed']
            weekWSKR = js['pvp']['brackets']['ARENA_BRACKET_2v2_SKIRMISH']['weeklyWon']
            seasonPSKR = js['pvp']['brackets']['ARENA_BRACKET_2v2_SKIRMISH']['seasonPlayed']
            seasonWSKR = js['pvp']['brackets']['ARENA_BRACKET_2v2_SKIRMISH']['seasonWon']
            try:
                weekRSKR = round(100 * weekWSKR / weekPSKR, 2)
            except ZeroDivisionError:
                weekRSKR = 0
            try:
                seasonRSKR = round(100 * seasonWSKR / seasonPSKR, 2)
            except ZeroDivisionError:
                seasonRSKR = 0
            
            tmpstr = "< 2v2 레이팅 : "+str(rating22) +" >\n"
            tmpstr += "\n\t이번 주   총 "+str(weekP22) +" 판\t"+str(weekW22)+" 승\t승률 : "+str(weekR22)+"%\n"
            tmpstr += "\n\t이번 시즌 총 "+str(seasonP22) +" 판\t"+str(seasonW22)+" 승\t승률 : "+str(seasonR22)+"%\n\n"
            tmpstr += "< 3v3 레이팅 : "+str(rating33) +" >\n"
            tmpstr += "\n\t이번 주   총 "+str(weekP33) +" 판\t"+str(weekW33)+" 승\t승률 : "+str(weekR33)+"%\n"
            tmpstr += "\n\t이번 시즌 총 "+str(seasonP33) +" 판\t"+str(seasonW33)+" 승\t승률 : "+str(seasonR33)+"%\n\n"
            tmpstr += "< 평전 레이팅 : "+str(ratingRBG) +" >\n"
            tmpstr += "\n\t이번 주   총 "+str(weekPRBG) +" 판\t"+str(weekWRBG)+" 승\t승률 : "+str(weekRRBG)+"%\n"
            tmpstr += "\n\t이번 시즌 총 "+str(seasonPRBG) +" 판\t"+str(seasonWRBG)+" 승\t승률 : "+str(seasonRRBG)+"%\n\n"
            tmpstr += "< 연투 레이팅 : "+str(ratingSKR) +" >\n"
            tmpstr += "\n\t이번 주   총 "+str(weekPSKR) +" 판\t"+str(weekWSKR)+" 승\t승률 : "+str(weekRSKR)+"%\n"
            tmpstr += "\n\t이번 시즌 총 "+str(seasonPSKR) +" 판\t"+str(seasonWSKR)+" 승\t승률 : "+str(seasonRSKR)+"%"
            self.prtext.setText(tmpstr)
            self.prtext.adjustSize()
            
            imgurl = js['thumbnail']
            url = "https://render-kr.worldofwarcraft.com/character/"+imgurl
            img = urllib.request.urlopen(url).read()
            pixface = QPixmap()
            pixface.loadFromData(img)
            self.thumbnail.setPixmap(pixface)
        pixmap = QPixmap(classimg)
        self.prbg.setPixmap(pixmap)
        self.profile.show()
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
            self.PageChoose(0)
            return 0
        else:
            return -2
    def ShowPage(self,no):
        try:
            self.ladder
        except AttributeError:
            return
        self.thumbnail.clear()
        i = no - 1
        i *= 10
        self.indexNo= i
        count = 0
        while count<10:
            if i>=self.totalNo:
                tmp = ""
                self.fr[count].hide()
            else:
                tmp = "랭킹 "
                tmp += str(self.ladder['rows'][i]['ranking'])
                tmp += " 위      레이팅 : "
                tmp += str(self.ladder['rows'][i]['rating'])
                tmp += "\n서버 : "
                tmp += self.ladder['rows'][i]['realmName']
                tmp += "\t\t"
                tmp += self.SpecName(self.ladder['rows'][i]['specId'])
                tmp += "  "
                tmp += self.ClassName(self.ladder['rows'][i]['classId'])
                tmp += "    "
                tmp += self.ladder['rows'][i]['name']
                self.fr[count].show()
            self.tx[count].setText(tmp)
            self.tx[count].adjustSize()
            count += 1
            i += 1
    def Search(self):
        name = self.searchName.text()
        i = self.indexNo
        t = self.totalNo
        while i<t and MD.ladder['rows'][i]['name']!=name:
            i+=1
        if i>=t:
            return -1
        self.indexNo = i
        pageno = int(i/10)+1
        self.pg[5].setText(str(pageno))
        self.PageChoose(5)
        return i
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
    def ClassRoute(self,no):
        if no == 1:
            return "img/warrior.png"
        elif no == 2:
            return "img/paladin.png"
        elif no == 3:
            return "img/hunter.png"
        elif no == 4:
            return "img/rogue.png"
        elif no == 5:
            return "img/priest.png"
        elif no == 6:
            return "img/death knight.png"
        elif no == 7:
            return "img/shaman.png"
        elif no == 8:
            return "img/mage.png"
        elif no == 9:
            return "img/warlock.png"
        elif no == 10:
            return "img/monk.png"
        elif no == 11:
            return "img/druid.png"
        elif no == 12:
            return "img/demonhunter.png"
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
    def SpecName(self, no):
        if no == 250:
            return "혈기"
        elif no == 251:
            return "냉기"
        elif no == 252:
            return "부정"
        elif no == 577:
            return "파멸"
        elif no == 581:
            return "복수"
        elif no == 102:
            return "조화"
        elif no == 103:
            return "야성"
        elif no == 104:
            return "수호"
        elif no == 105:
            return "회복"
        elif no == 253:
            return "야수"
        elif no == 254:
            return "사격"
        elif no == 255:
            return "생존"
        elif no == 62:
            return "비전"
        elif no == 63:
            return "화염"
        elif no == 64:
            return "냉기"
        elif no == 268:
            return "양조"
        elif no == 269:
            return "풍운"
        elif no == 270:
            return "운무"
        elif no == 65:
            return "신성"
        elif no == 66:
            return "보호"
        elif no == 70:
            return "징벌"
        elif no == 256:
            return "수양"
        elif no == 257:
            return "신성"
        elif no == 258:
            return "암흑"
        elif no == 259:
            return "잠행"
        elif no == 260:
            return "무법"
        elif no == 261:
            return "암살"
        elif no == 262:
            return "정기"
        elif no == 263:
            return "고양"
        elif no == 264:
            return "복원"
        elif no == 265:
            return "고통"
        elif no == 266:
            return "악마"
        elif no == 267:
            return "파괴"
        elif no == 71:
            return "무기"
        elif no == 72:
            return "분노"
        elif no == 73:
            return "보호"
        else:
            return "??"
    def TimeStr(self, tst):
        if type(tst) != time.struct_time:
            return "알 수 없음"
        y = tst.tm_year
        m = tst.tm_mon
        d = tst.tm_mday
        hour = tst.tm_hour
        minute = tst.tm_min
        sec = tst.tm_sec
        wd = tst.tm_wday
        ans = str(y)+"년 "+str(m)+"월 "+str(d)+"일 "
        if wd==0:
            ans += "월요일 "
        elif wd==1:
            ans += "화요일 "
        elif wd==2:
            ans += "수요일 "
        elif wd==3:
            ans += "목요일 "
        elif wd==4:
            ans += "금요일 "
        elif wd==5:
            ans += "토요일 "
        elif wd==6:
            ans += "일요일 "
        ans += str(hour)+":"+str(minute)+":"+str(sec)
        return ans

app = QApplication(sys.argv)
MD = wowLadder()
sys.exit(app.exec_())
