import pandas as pd
import numpy as np
import mysql.connector
import json
from datetime import datetime

import matplotlib.pyplot as plt

from data.arayüz.quiz import Ui_quiz
from data.arayüz.hata import Ui_hata
from data.arayüz.Ana import Ui_MainWindow
from data.arayüz.Giris import Ui_Giris
from data.arayüz.KayitOl import Ui_kayitOl
from data.arayüz.SifremiUnuttum import Ui_sifreUnut
from data.arayüz.KelimeEkle import Ui_kelimeUnut

import pygame

from PyQt6 import QtGui, QtWidgets, QtCore

import requests
from PIL import Image
from io import BytesIO
import configparser

import sys
import os

x=0
quizSoruSayisiDegeri= 10
kullaniciBilgi= np.nan
hataMsj=''
try:
    config = configparser.ConfigParser()
    config.read('data/sifre.ini')
    password_ = config['DEFAULT']['password'][1:-1]
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=str(password_),
        database="proje"
    )
except Exception as e:
    hataMsj='Veri tabanina baglanamadi !!!'
    raise e
def veri_uye():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM proje.uyeler")
        myresult = mycursor.fetchall()

        return pd.DataFrame(myresult, columns=["id", 'kullanici_adi', 'sifre'])
    except Exception as e:
        global hataMsj
        hataMsj=e
        
def veri_bilgi():
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT id, turkce, ing, konu, ses, okunus, ornekler, {kullaniciBilgi['id'][0]}_tarih, {kullaniciBilgi['id'][0]}_seviye FROM proje.kelimeler")
        myresult = mycursor.fetchall()
                
        return pd.DataFrame(myresult, columns=["id",'turkce', 'ing','konu','ses','okunus','ornekler', 'tarih', 'seviye'])
    except Exception as e:
        global hataMsj
        hataMsj=e
    
#region Hata
class hata(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_hata()
        self.ui.setupUi(self)
        self.ui.label_2.setText(hataMsj)
        self.ui.ButtonKapat.clicked.connect(self.kapat)

    def kapat(self):
        global hataMsj
        if hataMsj=='Veri tabanina baglanamadi !!!\nYapilan Degişikler kaydedilmeyeyecektir':
            hataMsj=''
            self.kapat()
        else:
            hataMsj=''
            self.close()

#region Qsuiz
class quiz(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_quiz()
        self.ui.setupUi(self)
        self.sayi= 0
        self.sorular = self.get_soru(quizSoruSayisiDegeri)
        self.dogruSayi= 0
        self.yanlisSayi= 0
        
        self.ui.secim1.clicked.connect(lambda: self.kontrol(self.ui.secim1.text(),'secim1'))
        self.ui.secim2.clicked.connect(lambda: self.kontrol(self.ui.secim2.text(),'secim2'))
        self.ui.secim3.clicked.connect(lambda: self.kontrol(self.ui.secim3.text(),'secim3'))
        self.ui.secim4.clicked.connect(lambda: self.kontrol(self.ui.secim4.text(),'secim4'))
        self.show_question()
        
    def show_question(self): 
        if self.sayi== quizSoruSayisiDegeri:
            self.ac()
            self.kapat()
            self.ui.soru.setText('Quiz bitti !!!')
            self.ui.secim1.setText('Doğru Sayısı: ')     ; self.ui.secim1.setStyleSheet('color: green')
            self.ui.secim2.setText(str(self.dogruSayi))  ; self.ui.secim2.setStyleSheet('color: green')
            self.ui.secim3.setText('Yanlış Sayısı: ')    ; self.ui.secim3.setStyleSheet('color: red')
            self.ui.secim4.setText(str(self.yanlisSayi)) ; self.ui.secim4.setStyleSheet('color: red')
            return    
        self.ac()
        self.ui.label_sira.setText(f'{self.sayi+1}/{quizSoruSayisiDegeri}')
        self.ui.soru.setText(self.sorular.iloc[self.sayi, 2])
        seçimler = np.random.choice(np.delete(np.arange(quizSoruSayisiDegeri), self.sayi), size=3, replace=False)

        sik = [self.sayi, seçimler[0], seçimler[1], seçimler[2]]
        np.random.shuffle(sik)

        self.ui.secim1.setText(self.sorular.iloc[sik[0], 1])
        self.ui.secim2.setText(self.sorular.iloc[sik[1], 1])
        self.ui.secim3.setText(self.sorular.iloc[sik[2], 1])
        self.ui.secim4.setText(self.sorular.iloc[sik[3], 1])
        self.sayi += 1
        
    def kapat(self):
        self.ui.secim1.setEnabled(False);self.ui.secim2.setEnabled(False);self.ui.secim3.setEnabled(False);self.ui.secim4.setEnabled(False)
    
    def ac(self):
        BACKGROUND_COLOR = 'background-color: white; color: black'
        self.ui.secim1.setEnabled(True) ; self.ui.secim1.setStyleSheet(BACKGROUND_COLOR)
        self.ui.secim2.setEnabled(True) ; self.ui.secim2.setStyleSheet(BACKGROUND_COLOR)
        self.ui.secim3.setEnabled(True) ; self.ui.secim3.setStyleSheet(BACKGROUND_COLOR)
        self.ui.secim4.setEnabled(True) ; self.ui.secim4.setStyleSheet(BACKGROUND_COLOR)
    def kontrol(self, secim, isim):
        GREEN_COLOR = 'background-color: green'
        RED_COLOR = 'background-color: red'
        if secim == self.sorular.iloc[self.sayi-1, 1]:
            if isim=='secim1':
                self.ui.secim1.setStyleSheet(GREEN_COLOR)
            elif isim=='secim2':
                self.ui.secim2.setStyleSheet(GREEN_COLOR)
            elif isim=='secim3':
                self.ui.secim3.setStyleSheet(GREEN_COLOR)
            elif isim=='secim4':
                self.ui.secim4.setStyleSheet(GREEN_COLOR)
            self.dogruSayi += 1

            self.guncelle(self.sorular.iloc[self.sayi-1, 0])
        else:
            if isim=='secim1':
                self.ui.secim1.setStyleSheet(RED_COLOR)
            elif isim=='secim2':
                self.ui.secim2.setStyleSheet(RED_COLOR)
            elif isim=='secim3':
                self.ui.secim3.setStyleSheet(RED_COLOR)
            elif isim=='secim4':
                self.ui.secim4.setStyleSheet(RED_COLOR)
            self.yanlisSayi += 1
            try:
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE`proje`.`kelimeler` SET {kullaniciBilgi['id'][0]}_tarih= '2000-01-01',{kullaniciBilgi['id'][0]}_seviye = '{0}' WHERE İngilizce = '{self.sorular.iloc[self.sayi-1, 2]}'")
                mydb.commit()
            except Exception as e:
                global hataMsj
                hataMsj=e
        self.kapat()
        
        QtCore.QTimer.singleShot(1000, self.show_question)
        
    def get_soru(self, count):
        df= veri_bilgi()
        df['tarih']= pd.to_datetime(df['tarih'],format='%Y-%m-%d')
        df= df[df['tarih']<pd.to_datetime(f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}',format='%Y-%m-%d')]
        df= df[df['seviye'] !=6]

        df= df.sort_values("seviye",ascending=False)
        soruSayi= count
        sorular= df.drop(df.index)
        for i in [5,4,3,2,1,0]:
            if soruSayi==0:
                return sorular
            elif len(df[df['seviye']==i])>soruSayi:
                sorular= pd.concat([sorular,df[df['seviye']==i].sample(soruSayi)])
                soruSayi= 0
            else:
                sorular= pd.concat([sorular,df[df['seviye']==i]])
                soruSayi-= len(df[df['seviye']==i])
        if soruSayi==0:
                return sorular
    def guncelle(self,id):
        try:
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT {kullaniciBilgi['id'][0]}_tarih, {kullaniciBilgi['id'][0]}_seviye FROM proje.kelimeler where id= '{id}'")
            myresult = pd.DataFrame(mycursor.fetchall())
            artis=myresult[1][0]
            tarih=pd.to_datetime(f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}',format='%Y-%m-%d')
            if   artis==0:            tarih=tarih+ pd.tseries.offsets.DateOffset(days=1)
            elif artis==1:            tarih=tarih+ pd.tseries.offsets.DateOffset(weeks=1)
            elif artis==2:            tarih=tarih+ pd.tseries.offsets.DateOffset(months=1)
            elif artis==3:            tarih=tarih+ pd.tseries.offsets.DateOffset(months=3)
            elif artis==4:            tarih=tarih+ pd.tseries.offsets.DateOffset(months=6)
            elif artis==5:            tarih=tarih+ pd.tseries.offsets.DateOffset(years=1)
        
            tarih=pd.to_datetime(tarih,format='%Y-%m-%d')
            mycursor.execute(f"UPDATE`proje`.`kelimeler` SET {kullaniciBilgi['id'][0]}_tarih= '{tarih}',{kullaniciBilgi['id'][0]}_seviye = '{artis+1}' WHERE id = '{id}'")
            mydb.commit()
        except Exception as e:
            global hataMsj
            hataMsj=e
        
#region Uygulama        
class uygulama(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.turkce.setText('Türkçe')
        self.ui.ing.setText('ingilizce')
        self.ui.ileri.clicked.connect(self.ileri)
        self.ui.geri.clicked.connect(self.geri)
        self.ui.ses.clicked.connect(self.ses)
        
        self.ui.actionKelime_Ekle.triggered.connect(self.KelimeEkle)
        self.ui.actionQuiz_i_Ba_lat.triggered.connect(self.quiz)
        
        self.ui.action5.triggered.connect(self.sayi5)
        self.ui.action10.triggered.connect(self.sayi10)
        self.ui.action15.triggered.connect(self.sayi15)
        self.ui.action20.triggered.connect(self.sayi20)
        self.ui.action25.triggered.connect(self.sayi25)
        self.ui.action30.triggered.connect(self.sayi30)

        self.sifirla(quizSoruSayisiDegeri)

        for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            percentage = '%{:.0f}'.format(width)

            if width != 0:
                ax.text(x+width/2, 
                        y+height/2, 
                        percentage, 
                        horizontalalignment='center', 
                        verticalalignment='center')
        ax.legend(bbox_to_anchor=(1, 1), loc='best')
        plt.show()
    def sifirla(self,sayi):
        self.ui.action5.setText('5')
        self.ui.action10.setText('10')
        self.ui.action15.setText('15')
        self.ui.action20.setText('20')
        self.ui.action25.setText('25')
        self.ui.action30.setText('30')
        if sayi==5:
            self.ui.action5.setText('5 ●')
        elif sayi==10:
            self.ui.action10.setText('10 ●')
        elif sayi==15:
            self.ui.action15.setText('15 ●')
        elif sayi==20:
            self.ui.action20.setText('20 ●')
        elif sayi==25:
            self.ui.action25.setText('25 ●')
        elif sayi==30:
            self.ui.action30.setText('30 ●') 
    def quizSoruSayisi(self,sayi):
        self.sifirla(sayi)
        global quizSoruSayisiDegeri
        quizSoruSayisiDegeri= sayi
        
    def sayi5(self) :        self.quizSoruSayisi(5)
    def sayi10(self):        self.quizSoruSayisi(10)
    def sayi15(self):        self.quizSoruSayisi(15)
    def sayi20(self):        self.quizSoruSayisi(20)
    def sayi25(self):        self.quizSoruSayisi(25)
    def sayi30(self):        self.quizSoruSayisi(30)
    
    def quiz(self):
        self.ana_sayfa = quiz()
        self.ana_sayfa.show()
    def KelimeEkle(self):
        self.ana_sayfa = KelimeEkle()
        self.ana_sayfa.show()
    
    def ses(self):
        filename = veri_bilgi()['ing'][x] + '.mp3'  

        sound_file = f"data/ses/{filename}"
        if os.path.exists(sound_file):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f"Error playing sound: {e}")
            finally:
                pygame.mixer.quit()
            return 

        if veri_bilgi()['ses'][x].startswith('http'): 
            try:
                response = requests.get(veri_bilgi()['ses'][x])
                if response.status_code == 200:
                    with open(f"data/ses/{filename}", 'wb') as f:
                        f.write(response.content)

                    if os.path.exists(sound_file):
                        try:
                            pygame.mixer.init()
                            pygame.mixer.music.load(sound_file)
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                pygame.time.Clock().tick(10)
                        except Exception as play_error:
                            print(f"{play_error}")
                        finally:
                            pygame.mixer.quit()
            except Exception as download_error:
                print(f"EIndirme Hatasi: {download_error}")
    def foto(self, resim):
        if os.path.exists(f"data/image/{resim}.png"):
            pixmap = QtGui.QPixmap(f"data/image/{resim}.png")
            self.ui.resim.setPixmap(pixmap)
        else:
            url = f"https://api.unsplash.com/search/photos?query={resim}"
            headers = {"Authorization": "Client-ID xxSyiroQ-BXkciHTmkDjYrHJ0PT-Cu4bBLvV71HKcvw"}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                first_image_url = data['results'][0]['urls']['small']
                response = requests.get(first_image_url)
                img = Image.open(BytesIO(response.content))
                img.save(f"data/image/{resim}.png")
                self.ui.resim.setPixmap(QtGui.QPixmap(f"data/image/{resim}.png"))
    def bilgi(self):
        data = json.loads(json.loads(veri_bilgi()['ornekler'][x]))
        self.ui.bilgiler.clear()
        
        if isinstance(data, list):
            for meaning in data:
                if isinstance(meaning, dict):
                    self.ui.bilgiler.append(f"Sözcük Türü: {meaning.get('partOfSpeech', 'N/A')}")
                        
                if 'synonyms' in meaning and meaning['synonyms']:
                    synonyms = ', '.join(meaning['synonyms'])
                    self.ui.bilgiler.append(f"\tEşanlamlılar: {synonyms}")
                        
                if 'antonyms' in meaning and meaning['antonyms']:
                    antonyms = ', '.join(meaning['antonyms'])
                    self.ui.bilgiler.append(f"\tZıtanlamlılar: {antonyms}")
                        
                for tanim in meaning.get('definitions', []):
                    if isinstance(tanim, dict):
                        self.ui.bilgiler.append(f"\tTanım: {tanim.get('definition', 'N/A')}")
                                
                    if 'synonyms' in tanim and tanim['synonyms']:
                        synonyms = ', '.join(tanim['synonyms'])
                        self.ui.bilgiler.append(f"\tEşanlamlılar: {synonyms}")
                                
                    if 'antonyms' in tanim and tanim['antonyms']:
                        antonyms = ', '.join(tanim['antonyms'])
                        self.ui.bilgiler.append(f"\tZıtanlamlılar: {antonyms}")
                                
                    if 'example' in tanim:
                        self.ui.bilgiler.append(f"\t\tÖrnek: {tanim['example']}")

    def ileri_geri(self, direction):
        global x
        if direction == "ileri":
            x += 1
        elif direction == "geri":
            x -= 1
        if len(veri_bilgi()) == x:
            x = 0
        if x<0:
            x=len(veri_bilgi())-1
        self.ui.turkce.setText(veri_bilgi()['turkce'][x])
        self.ui.ing.setText(veri_bilgi()['ing'][x])
        self.ui.bilgiler.setText(veri_bilgi()['konu'][x])
        resim= veri_bilgi()['ing'][x]
        try:
            self.foto(resim)
        except Exception as e:
            global hataMsj
            hataMsj=e
            self.ui.resim.setPixmap(QtGui.QPixmap("data/logo.png"))
        self.bilgi()
        
        self.ui.ses.setText(veri_bilgi()['okunus'][x][1:-1])
        
    def ileri(self):
        self.ileri_geri(direction="ileri")

    def geri(self):
        self.ileri_geri(direction="geri")
        
#region Kayıt
class kayit(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_kayitOl()
        self.ui.setupUi(self)
        
        self.ui.ButtonKayitoOl.clicked.connect(self.kayit_)
    def kayit_(self):
        global hataMsj
        mycursor = mydb.cursor()
        kullanici_adi = self.ui.linekulAdi.text()
        sifre = self.ui.linekulSifre.text()
        sifre_tekrar = self.ui.lineEditSifreTekrar.text()
        if sifre != sifre_tekrar:
            hataMsj='Şifreler Uyuşmuyor'
            
        elif kullanici_adi != '' and sifre != '':
            mycursor.execute(f"INSERT INTO proje.uyeler (kullanici_adi, sifre) VALUES ('{kullanici_adi}', '{sifre}')")
            mydb.commit()
            
            mycursor.execute(f"SELECT * FROM proje.uyeler WHERE kullanici_adi= '{kullanici_adi}' and sifre= '{sifre}'")
            myresult = mycursor.fetchall()
            
            df = pd.DataFrame(myresult, columns=["id", 'kullanici_adi', 'sifre'])
            
            mycursor.execute(f"ALTER TABLE `proje`.`kelimeler` ADD COLUMN `{df['id'][0]}_tarih` DATE NULL DEFAULT '2000-01-01' , ADD COLUMN `{df['id'][0]}_seviye` INT NULL DEFAULT '0' ")
            
            mydb.commit()
            hataMsj='Kayıt Başarılı'
            self.close()
            
        else:
            hataMsj='Kayıt Başarisiz'
        self.ana_sayfa = hata()
        self.ana_sayfa.show()
        

#region Kayit Unut
class KayitUnut(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_sifreUnut()
        self.ui.setupUi(self)
        
        self.ui.buttonKayitOl.clicked.connect(self.sifreYenile)
    def sifreYenile(self):
        global hataMsj
        mycursor = mydb.cursor()
        kullanici_adi = self.ui.linekulAdi.text()
        sifre = self.ui.lineyeniSifre.text()
        sifre_tekrar = self.ui.linesifreTekrar.text()
        if sifre != sifre_tekrar:
            hataMsj='Şifreler Uyuşmuyor'
        elif kullanici_adi != '' and sifre != '':
            try:
                mycursor.execute(f"UPDATE proje.uyeler SET sifre = '{sifre}' WHERE kullanici_adi = '{kullanici_adi}'")
                mydb.commit()
                hataMsj='Şifreler Yenilendi'
            except Exception as e:
                global hataMsj
                hataMsj=e
        else:
            hataMsj='kısa'
        
        self.ana_sayfa = hata()
        self.ana_sayfa.show()        
#region Kelime Ekle
class KelimeEkle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_kelimeUnut()
        self.ui.setupUi(self)
        
        self.ui.kaydet.clicked.connect(self.kelimeEkle)
    def kelimeEkle(self):
        global hataMsj
        mycursor = mydb.cursor()
        turkce = self.ui.turkce.text()
        ing = self.ui.ing.text()
        konu = self.ui.konu.text()
        try:
            res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{ing}").content.decode('utf-8')
            json_data = json.loads(res)
            ses = json_data[0]['phonetics'][0]['audio']
            if ses=='':
                hataMsj='Ses Bulunamadı'
                self.ana_sayfa = hata()
                self.ana_sayfa.show()
                return
            okunus = json_data[0]['phonetics'][0]['text']
            ornekler = (json_data[0]['meanings']) 

            sql = "INSERT INTO kelimeler (turkce, ing, konu, ses, okunus, ornekler) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (turkce, ing, konu, ses, okunus, json.dumps(json.dumps(ornekler)))
            mycursor.execute(sql, val)
            mydb.commit()   
        except Exception as e:
            hataMsj=f'Kelime Bulunamadı. Hata: {e}'
            self.ana_sayfa = hata()
            self.ana_sayfa.show()
            return
        
        hataMsj='Kelime Eklendi'
        self.ana_sayfa = hata()
        self.ana_sayfa.show()
        self.close()

#region Giriş
class Giris(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Giris()
        self.ui.setupUi(self)
        
        self.ui.button_giris.clicked.connect(self.giris)
        self.ui.button_kayitOl.clicked.connect(self.kayit)
        self.ui.button_sifreUnut.clicked.connect(self.sifre_unut)
        
    def giris(self):
        global hataMsj
        df = veri_uye()
        kullanici_adi = self.ui.line_kulAdi.text()
        sifre = self.ui.line_sifre.text()
        
        if kullanici_adi in df['kullanici_adi'].values and sifre in df['sifre'].values:
            global kullaniciBilgi
            kullaniciBilgi= pd.DataFrame(df[df['kullanici_adi']==kullanici_adi]).reset_index(drop=True)
            if hataMsj=='Veri tabanina baglanamadi !!!\nYapilan Degişikler kaydedilmeyeyecektir':
                self.ana_sayfa= hata()
                self.ana_sayfa.show()
                self.close()
            else:
                self.ana_sayfa = uygulama()
                self.ana_sayfa.show()
                self.close()
                
        else:
            hataMsj='Kullanici veya Sifre Hatali'
            self.ana_sayfa = hata()
            self.ana_sayfa.show()
            
    def kayit(self):
        self.ana_sayfa = kayit()
        self.ana_sayfa.show()
        
    def sifre_unut(self):
        self.ana_sayfa = KayitUnut()
        self.ana_sayfa.show()
 
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Giris()
    win.show()
    sys.exit(app.exec())

app()