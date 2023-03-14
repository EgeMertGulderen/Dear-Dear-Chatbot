import re
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import openpyxl
import sqlite3
from sqlite3 import Error

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

ser = Service("C:\\chromedriver.exe")
op = webdriver.ChromeOptions()

op.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ser, options=op)

driver.get(
    'https://bilsis.hacettepe.edu.tr/oibs/bologna/start.aspx?gkm=00103773538880322003550534480229238776366903333633360')

wait = WebDriverWait(driver, 5)
driver.find_element(By.XPATH, '//*[@id="form1"]/div[5]/nav/ul[1]/li/div/a').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="proMenu"]/li[2]/a').click()
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="proMenu"]/li[2]/ul/li[2]/a').click()

iframe = driver.find_element(By.ID, 'IFRAME1')
driver.switch_to.frame(iframe)

soup = BeautifulSoup(driver.page_source, 'html.parser')

classes = soup.find_all('a', {'target': '_parent'})

bölüm_lst = []
ders_dict_lst = []


def get_class_information(driver, lst,bölüm_dict):
    time.sleep(2)
    ders_dili = ""
    dersin_düzeyi = ""
    bölümü = ""
    öğrenim_türü = ""
    dersin_türü = ""
    dersin_amacı = ""
    dersin_içeriği = ""
    ön_koşul = ""
    dersin_kordinatör = ""
    dersi_veren = ""
    dersin_yardımcısı = ""
    dersin_staj = ""

    class_soup = BeautifulSoup(driver.page_source, 'html.parser')
    ders_detay = class_soup.find('table', {'class': 'table table-hover table-striped'})

    try:
        ders_dili = ders_detay.find('span', {'id': 'dlDers_DILLabel_0'}).text
    except AttributeError:
        ders_dili = ''
    try:
        dersin_düzeyi = ders_detay.find('span', {'id': 'dlDers_Label6_0'}).text
    except AttributeError:
        dersin_düzeyi = ''

    try:
        bölümü = ders_detay.find('span', {'id': 'dlDers_Label7_0'}).text
    except AttributeError:
        bölümü = ''
    try:
        öğrenim_türü = ders_detay.find('span', {'id': 'dlDers_Label5_0'}).text
    except AttributeError:
        öğrenim_türü = ''
    try:
        dersin_türü = ders_detay.find('span', {'id': 'dlDers_TURLabel_0'}).text
    except AttributeError:
        dersin_türü = ''
    try:
        dersin_amacı = ders_detay.find('span', {'id': 'dlDers_AMACLabel_0'}).text
    except AttributeError:
        dersin_amacı = ''
    try:
        dersin_içeriği = ders_detay.find('span', {'id': 'dlDers_ICERIKLabel_0'}).text
    except AttributeError:
        dersin_içeriği = ''
    try:
        ön_koşul = ders_detay.find('span', {'id': 'dlDers_DERS_ONKOSULLabel_0'}).text
    except AttributeError:
        ön_koşul = ''
    try:
        dersin_kordinatör = ders_detay.find('span', {'id': 'dlDers_DERS_KOORDINATORLabel_0'}).text
    except AttributeError:
        dersin_kordinatör = ''
    try:
        dersi_veren = ders_detay.find('span', {'id': 'dlDers_DERS_VERENLabel_0'}).text
    except AttributeError:
        dersi_veren = ''
    try:
        dersin_yardımcısı = ders_detay.find('span', {'id': 'dlDers_DERS_YARDIMCILabel_0'}).text
    except AttributeError:
        dersin_yardımcısı = ''
    try:
        dersin_staj = ders_detay.find('span', {'id': 'dlDers_STAJ_VARMILabel_0'}).text
    except AttributeError:
        dersin_staj = ''

    ders = class_soup.find('table', {'class': 'grdStyle'})
    ders_bilgi = ders.find_all('td', {'style': 'padding:3px;'})

    ders_yarıyıl = ders_bilgi[0].text
    ders_kodu = ders_bilgi[1].text
    ders_adı = ders_bilgi[2].text
    ders_tu = ders_bilgi[3].text
    ders_kredi = ders_bilgi[4].text
    ders_akts = ders_bilgi[5].text



    ders_dict = {'Dersin Adı': ders_adı,
                 'Dersin Kodu': ders_kodu,
                 'Dersin Kredisi': ders_kredi,
                 'Dersin AKTS': ders_akts,
                 'Ders Yarıyılı': ders_yarıyıl,
                 'Ders TU': ders_tu,
                 'Dersin Dili': ders_dili,
                 'Dersin Düzeyi': dersin_düzeyi,
                 'Dersin Bölümü': bölümü,
                 'Dersin Öğrenim Türü': öğrenim_türü,
                 'Dersin Türü': dersin_türü,
                 'Dersin Amacı': dersin_amacı,
                 'Dersin İçeriği': dersin_içeriği,
                 'Dersin Ön Koşulu': ön_koşul,
                 'Dersin Kordinatörü': dersin_kordinatör,
                 'Dersi Veren': dersi_veren,
                 'Derse Yardımcı Olan': dersin_yardımcısı,
                 'Dersin Staj Durumu': dersin_staj
                 }

    lst.append(ders_dict)
    bölüm_dict.update({'Dersler' : ders_dict})

xpath_lst = []
xpath_lst.extend(['//*[@id="proMenu"]/li[3]/ul/li[1]/a', '//*[@id="proMenu"]/li[3]/ul/li[2]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[3]/a', '//*[@id="proMenu"]/li[3]/ul/li[4]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[5]/a', '//*[@id="proMenu"]/li[3]/ul/li[6]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[7]/a', '//*[@id="proMenu"]/li[3]/ul/li[8]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[9]/a', '//*[@id="proMenu"]/li[3]/ul/li[10]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[11]/a', '//*[@id="proMenu"]/li[3]/ul/li[12]/a',
                  '//*[@id="proMenu"]/li[3]/ul/li[13]/a'])


for i in classes:
    if i.text == "YAPAY ZEKA MÜHENDİSLİĞİ (765)" or i.text == "BİLGİSAYAR MÜHENDİSLİĞİ (356)":
        url = 'https://bilsis.hacettepe.edu.tr/oibs/bologna/' + i['href']
        driver.get(url)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="form1"]/div[5]/nav/ul[1]/li/div/a').click()
        time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="proMenu"]/li[3]/ul/li[2]/a').click()
        time.sleep(1)

        iframe = driver.find_element(By.ID, 'IFRAME1')
        driver.switch_to.frame(iframe)
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        elements = soup1.find_all("div", {'class': 'panel panel-default'})
        bölüm = ''
        dil = ''
        azami_süre = ''
        süre = ''
        kontenjan = ''
        staj = ''
        İçerik_head = ''
        İçerik = ''
        Tarihçe_head = ''
        Tarihçe = ''
        Kazanılan_Derece_head = ''
        Kazanılan_Derece = ''
        Kabul_head = ''
        Kabul = ''
        Mezuniyet_head = ''
        Mezuniyet = ''
        İstihdam = ''
        Ölçme_head = ''
        Ölçme = ''
        Anabilim = ''
        Program = ''



        for element in elements:
            if element.find("span", {'id': 'grdAboutProg_lblHeader_0'}):
                bölüm = element.find("span", {'id': 'grdAboutProg_lblHeader_0'}).text

                x = element.find('table', {'class': 'table-hover'})
                dil = x.find('span', {'id': 'grdAboutProg_Label1_0'}).text
                azami_süre = x.find('span', {'id': 'grdAboutProg_Label16_0'}).text
                süre = x.find('span', {'id': 'grdAboutProg_Label15_0'}).text
                kontenjan = x.find('span', {'id': 'grdAboutProg_Label17_0'}).text
                staj = x.find('span', {'id': 'grdAboutProg_Label19_0'}).text

            elif element.find("span", {'id': 'grdAboutProg_lblProgContent_0'}):
                x = element.find('table', {'class': 'table-hover'})
                İçerik = x.find('span', {'id': 'grdAboutProg_Label6_0'}).text


            elif element.find("span", {'id': 'grdAboutProg_lblTarihce_0'}):
                x = element.find('table', {'class': 'table-hover'})
                Tarihçe = x.find('span', {'id': 'grdAboutProg_Label5_0'}).text


            elif element.find("span", {'id': 'grdAboutProg_lblALINACAK_DERECE_0'}):
                x = element.find('table', {'class': 'table-hover'})
                Kazanılan_Derece = x.find('span', {'id': 'grdAboutProg_Label31_0'}).text


            elif element.find("span", {'id': 'grdAboutProg_lblKABUL_KOSUL_0'}):
                x = element.find('table', {'class': 'table-hover'})
                Kabul = x.find('span', {'id': 'grdAboutProg_Label32_0'}).text


            elif element.find("span", {'id': 'grdAboutProg_lblMEZUN_KOSUL_0'}):
                x = element.find('table', {'class': 'table-hover'})
                Mezuniyet = x.find('span', {'id': 'grdAboutProg_Label34_0'}).text



            elif element.find("span", {'id': 'grdAboutProg_lblMezunIstihdam_0'}):
                x = element.find('table', {'class': 'table-hover'})
                İstihdam = x.find('span', {'id': 'grdAboutProg_Label3_0'}).text


            elif element.find("span", {'id': 'grdAboutProg_lblSINAV_KURAL_0'}):
                x = element.find('table', {'class': 'table-hover'})
                Ölçme = x.find('span', {'id': 'grdAboutProg_Label35_0'}).text


        a = soup1.find('span', {'id': 'grdAboutProg_lblProgYetkili_0'})
        b = a.find_all('table', {'class': 'table-hover'})
        teacher_lst = []
        for teacher in b:
            teacher_lst.append(teacher.text.strip())

        if len(teacher_lst) == 2:
            Anabilim = teacher_lst[0]
            Program = teacher_lst[1]

        elif len(teacher_lst) == 1:
            Anabilim = teacher_lst[0]
            Program = ''

        else:
            Anabilim = ''
            Program = ''

        bölüm_dict = {'Bölüm Adı': bölüm,
                      'Bölüm Dili': dil,
                      'Bölüm Süresi': süre,
                      'Bölüm Azami Süresi': azami_süre,
                      'Bölüm Kontenjanı': kontenjan,
                      'Bölüm Staj Durumu': staj,
                      'Bölüm İçeriği': İçerik,
                      'Bölüm Tarihçesi': Tarihçe,
                      'Bölüm Kazanılan Derece': Kazanılan_Derece,
                      'Bölüm Kabul Koşulları': Kabul,
                      'Bölüm Mezuniyet': Mezuniyet,
                      'Bölüm İstihdam Olanakları': İstihdam,
                      'Bölüm Ölçme ve Değerlendirme': Ölçme,
                      'Bölüm Anabilim Başkanı': Anabilim,
                      'Bölüm Program Başkanı': Program}

        bölüm_lst.append(bölüm_dict)

        time.sleep(1)
        driver.switch_to.default_content()
        driver.find_element(By.XPATH, '//*[@id="proMenu"]/li[3]/ul/li[13]/a').click()
        time.sleep(2)
        iframe = driver.find_element(By.ID, 'IFRAME1')
        driver.switch_to.frame(iframe)
        time.sleep(2)

        lst = []
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        Lessons = soup2.find_all("a", {
            'style': 'color:#5B636A;font-family:Open Sans;font-size:9pt;display:table-cell;vertical-align :middle; color:black;'})
        for lesson in Lessons:
            attribute = lesson['id']
            attribute = attribute.split("btnDersAyrinti_", 1)[1]
            lst.append(attribute)

        for number in lst:
            button = driver.find_element(By.CSS_SELECTOR, '#grdBolognaDersler_btnDersAyrinti_' + number)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            get_class_information(driver, ders_dict_lst,bölüm_dict)
            driver.switch_to.default_content()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="proMenu"]/li[3]/ul/li[13]/a').click()
            iframe = driver.find_element(By.ID, 'IFRAME1')
            driver.switch_to.frame(iframe)







bölüm_df = pd.DataFrame.from_dict(bölüm_lst)
ders_df= pd.DataFrame.from_dict(ders_dict_lst)
bölüm_df.to_excel('Bölüm.xlsx')
ders_df.to_excel('Ders.xlsx')
print('Fin')
