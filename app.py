import pandas as pd
import numpy as np
import mysql.connector
import json

from data.arayüz.hata import Ui_hata
from data.arayüz.Giris import Ui_Giris
from data.arayüz.KayitOl import Ui_kayitOl
from data.arayüz.SifremiUnuttum import Ui_sifreUnut

from PyQt6 import QtGui, QtWidgets, QtCore

import requests
import configparser

import sys
x=0
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
                pass
                
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