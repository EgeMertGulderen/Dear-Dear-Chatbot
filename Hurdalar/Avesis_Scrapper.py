import re
import time

import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

ser = Service("C:\\chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=ser, options=op)

teacher_information_lst = []

for i in range(0, 1):
    url = "https://avesis.hacettepe.edu.tr/arastirmaci-arama?size=100&B%C3%B6l%C3%BCm%20Ara=bilgisayar&%C3%87al%C4%B1%C5%9F%C4%B1lan%20B%C3%B6l%C3%BCm[0]=Bilgisayar%20M%C3%BChendisli%C4%9Fi%20B%C3%B6l%C3%BCm%C3%BC"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find_all("div", {"class": "title"})


    def get_teachers():
        for teacher in element:
            tag = teacher.a
            # Get the attribute
            attribute = tag['data-networkuserid']
            url_id = 'https://avesis.hacettepe.edu.tr/nr/' + attribute
            r = requests.get(url_id)
            soup1 = BeautifulSoup(r.text, "html.parser")
            check = soup1.find('div', {"id": "wrapper"})

            if check is None:

                check = soup1.find('div', {"id": "wrap"})
                test = check.find('div', {'class': 'identity-header-info'})
                name = test.find("h2")

                print(name)
                faculty = test.select("h4")
                department = faculty[0].text
                specialty = faculty[1].text
                research_Area = faculty[2]
                strong = research_Area.find('strong')
                strong.decompose()
                test1 = soup1.find('div', {'class': 'span4 cv-header-contact'})
                information = test1.find_all('div')
                lst = []
                for section in information:
                    hr = section.find('a').text
                    lst.append(hr)

                if len(lst) == 3:
                    teacher_information = {'Ad': name.text.strip(),
                                           'Departman': department.strip(),
                                           'Uzmanlık': specialty.strip(),
                                           'Araştırma Alanları': research_Area.text.strip(),
                                           'E-Posta': 'mailto:' + lst[0].strip(),
                                           }
                elif len(lst) == 4:

                    teacher_information = {'Ad': name.text.strip(),
                                           'Departman': department.strip(),
                                           'Uzmanlık': specialty.strip(),
                                           'Araştırma Alanları': research_Area.text.strip(),
                                           'E-Posta': 'mailto:' + lst[0].strip(),
                                           'Web': lst[3]
                                           }

                teacher_information_lst.append(teacher_information)

            else:

                name = check.find("h1", {"class": "title"})

                if check.find("span", {"class": 'corporateInformation'}) is None:
                    faculty = ""
                    department = ""
                    specialty = ""
                else:
                    field = check.find("span", {"class": 'corporateInformation'}).text.strip().split(',')
                    if len(field) == 1:
                        faculty = field[0]
                    elif len(field) == 2:
                        faculty = field[0]
                        department = field[1]
                    else:
                        faculty = field[0]
                        department = field[1]
                        specialty = field[2]
                research = check.find('div', {'class': 'col-md-12', 'style': 'margin-top: 10px;'})
                if research is None:
                    res = ""
                else:
                    strong = research.find('strong')
                    strong.decompose()
                    res = research.text.strip()
                contacts = check.find('dl', {'id': 'contactList'})
                lst = []
                if contacts is None:
                    lst.append("")
                else:
                    for inf in contacts.find_all('dd'):
                        lst.append(inf.text.strip())
                web = check.find('a', {'class': 'avatar'}).get('href')

                if len(field) == 1:
                    teacher_information = {'Ad': name.text.strip(),
                                           'Departman': faculty,
                                           'Uzmanlık': specialty,
                                           'Araştırma Alanları': res,
                                           'E-Posta': 'mailto:' + lst[0].strip(),
                                           'Web': 'https://avesis.hacettepe.edu.tr' + web}
                elif len(field) == 2:
                    teacher_information = {'Ad': name.text.strip(),
                                           'Departman': faculty + "," + department,
                                           'Uzmanlık': "",
                                           'Araştırma Alanları': res,
                                           'E-Posta': 'mailto:' + lst[0].strip(),
                                           'Web': 'https://avesis.hacettepe.edu.tr' + web}

                else:
                    teacher_information = {'Ad': name.text.strip(),
                                           'Departman': faculty + "," + department,
                                           'Uzmanlık': specialty,
                                           'Araştırma Alanları': res,
                                           'E-Posta': 'mailto:' + lst[0].strip(),
                                           'Web': 'https://avesis.hacettepe.edu.tr' + web}
                    teacher_information_lst.append(teacher_information)

    get_teachers()

df = pd.DataFrame(teacher_information_lst)
df.to_excel('Teachers.xlsx')
print('Fin')
