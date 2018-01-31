# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:26:50 2018

@author: los40
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time



os.chdir("C:/Users/los40/Desktop/scrapmotogp/")
#directorio del driver de chrome 
driver = webdriver.Chrome("C:/Users/los40/Desktop/scrapmotogp/chromedriver.exe")
wait = WebDriverWait(driver, 10)
#vamos a la dirección donde queremos hacer el scraping
driver.get("http://www.motogp.com/en/Results+Statistics/")
links = []
anyo = 2018
anyos = []
slider = driver.find_element_by_xpath('//*[@id="handle_season"]')

#handle_season..ui-slider-handle ui-state-default
#for year in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#season a aria-valuetext"))):
 #year.click()                                                          
 #descargamos todos los eventos de la respectiva sesion   
 #clicamos todos los ementos seleccionados con By.CSS_SELECTOR dentro del label event (option)  
for year in range(5):  
  anyo = anyo -1
  for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#event option"))):
     item.click()
     elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "padleft5")))
     print(elem.get_attribute("href"))
     links.append(elem.get_attribute("href"))
     anyos.append(anyo)                                                   
     wait.until(EC.staleness_of(elem))
  slider.send_keys(Keys.ARROW_LEFT)
  time.sleep(1)

driver.quit()

#############
##DESCARGA###

#descargamos todos los pdfs de los links que hemos almacenado
ind = 0
import requests
for i in links:
 r = requests.get(i, allow_redirects=True)
 open(str(ind) + i[-10:] + ".pdf" , 'wb').write(r.content) 
 ind = ind + 1
 #ponemos como nombre los ultimos 10 caracteres de cada link
 

#leemos los archivos .pdf que hemos descargado
#Extraemos datos de los pdf
 
 
 ######################
 ######################
 ######################
     ###SIN USO###

     
import PyPDF2
pdf_file = open(links[1][-10:] + ".pdf", 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()

pgs = page_content.split()


pgss = pgs[pgs.index("km")+1:pgs.index("Classified")-1]
spg = str(pgss)


import pandas as pd

pd.DataFrame(pgss)

#######################
#######################



###### CONVERTIR CONTENIDO DE PDF A HTLM

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
import io 




def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = path
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
    
import pandas as pd
from bs4 import BeautifulSoup as bs

    
def extraccio_dades(pdf_file,country,year):
        team = ['HONDA','YAMAHA','DUCATI','SUZUKI','KTM','APRILIA']
    
        motoh = convert_pdf_to_html(pdf_file)

        numero = 0
        motobs = bs(motoh)
        motobsg = bs.get_text(motobs)
        mbs = str(motobsg)
        mbss = mbs.split()  
    
        mbsd = mbss[mbss.index("Gap")+16:mbss.index("Pole")]
        regex=re.compile("^[a-zA-Z].*")
        okme=[m.group(0) for l in mbsd for m in [regex.search(l)] if m]

        numero=12
        pilotos = mbsd[mbsd.index(okme[0]):mbsd.index(okme[0])+numero*2]
        for i in range(50):
          if RepresentsInt(mbsd[i]) == False:
                    break
      
        ind = 1
        pilo = []
        for i in range(int(len(pilotos)/2)):
          pilo.append(pilotos[ind-1] + pilotos[ind])
          ind = ind + 2
        gap = ['0'] + mbsd[mbsd.index('laps')-numero:mbsd.index('laps')-1 ]
        regex=re.compile("\d\d\d.\d{1,2}")
        kms=[m.group(0) for l in mbsd for m in [regex.search(l)] if m]
        kmh = mbsd[mbsd.index(kms[0]):mbsd.index(kms[0])+numero]
        regex=re.compile("\d{1,2}[^:]\d\d.\d\d\d")
        time=[m.group(0) for l in mbss for m in [regex.search(l)] if m]
        tii = mbss.index(time[0])
        time1 = mbss[tii:tii+numero]
        indice = 0
        mbss[mbss.index(time[-1])+1:mbss.index(time[-1])+1+numero]
        for i in range(2000):
            if mbss[i] in list(set(team)) and mbss[i+1] in list(set(team)):
                indice = i
                break
        team1 = mbss[indice:indice+numero]        
        air = []
        humidity = []
        ground = []   
        circuito = country
        years = []
        for i in range(numero):
            air.append(mbsd[len(mbsd)-5])
            humidity.append(mbsd[len(mbsd)-3])
            ground.append(mbsd[len(mbsd)-1])
            years.append(year)
    
        return pd.DataFrame( {'1Class': range(1,numero+1),
                          '2Pilotos': pilo,
                          'Km/h:': kmh,
                          'Time:': time1,
                          'Team:': team1,
                          '3Gap': gap,
                          '3Air': air,
                          '4Ground': ground,
                          '5Humidity': humidity,
                          'Circuito': circuito,
                          'Year': years
                                             })
    
    
def errades(pdf_file, country,year):
        opdf_file = open(pdf_file, 'rb')
    
        try:
          extraccio_dades(opdf_file, country,year)
        except ValueError:
            return pdf_file
        
nolinks = []    
for i in range(len(links)):
    nolinks.append(errades(str(i)+links[i][-10:] + ".pdf",links[i][-45:-42],anyos[i]))
    

    
ok = pd.DataFrame()
for i in range(len(links)):
    if str(i)+links[i][-10:] + ".pdf" not in nolinks:
        ok = ok.append(extraccio_dades(open(str(i)+links[i][-10:] + ".pdf", 'rb'),links[i][-45:-42],anyos[i]) )
        
        
        
ok.to_csv('moto_scrap.csv',sep=',', encoding='utf-8')


