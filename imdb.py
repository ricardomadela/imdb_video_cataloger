#!/usr/bin/python3
from bs4 import BeautifulSoup
import http.cookiejar
import requests, time, datetime, os, sys
import urllib
import io
import urllib.request
from urllib.parse import quote
import glob

extensao = 'mp4'

def busca2(url,codimdb):
    opener=urllib.request.build_opener()
    cookie = http.cookiejar.CookieJar() # get cookie
    cookie_process = urllib.request.HTTPCookieProcessor(cookie) #
    opener = urllib.request.build_opener(cookie_process) # build opener        
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
        ('Accept-Encoding', 'none'),
        ('Accept-Language', 'en-US,en;q=0.8'),
        ('Connection', 'keep-alive'),]
    urllib.request.install_opener(opener)
    videos=urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(videos, 'html.parser')
    img_elements = soup.find_all('img')  # Encontrar todos os elementos 'img'
    ano = " "
    try:
        ano = (str(img_elements[1]).split('(')[1].split(')')[0])#
    except Exception as e:
        print(e)
    imagens = str(img_elements[1]).split('https')
    linkimagem = 'https' + str(imagens[-1]).split('.jpg')[0] + '.jpg'
    response = requests.get(linkimagem)  # Fazer o download da imagem
    if response.status_code == 200:
        novonome = filename.replace('.' + str(extensao),' (' + str(codimdb) + ').' + str(extensao))
        if str(novonome).startswith(str(ano)) == False:
            novonome = str(ano) + ' - ' + str(novonome)
        os.rename(filename,novonome)
        nome = novonome.replace('.' + str(extensao),'')
        with open(f"{nome}.jpg", "wb") as f:
            f.write(response.content)

        print(novonome)

def busca(url):
    try:
        opener=urllib.request.build_opener()
        cookie = http.cookiejar.CookieJar() # get cookie
        cookie_process = urllib.request.HTTPCookieProcessor(cookie) #
        opener = urllib.request.build_opener(cookie_process) # build opener        
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
            ('Accept-Encoding', 'none'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Connection', 'keep-alive'),]
        urllib.request.install_opener(opener)
        videos=urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(videos, 'html.parser')
        links = soup.find_all('a', href=lambda href: href and 'imdb.com/title' in href)
        links2 = soup.find_all('h3')
        textos_h3 = [h3.get_text(strip=True) for h3 in links2]
        contador = 0
        for texto in textos_h3:
            if 'IMDb' in texto:
                if len(texto) > 3 and 'Series' not in texto:
                    break
            contador += 1
        try:
            href = links[contador - 1]['href']
            codimdb = str(href).split('www.imdb.com/title/')[1].split('/')[0]
            url = 'https://www.imdb.com/title/' + str(codimdb) + '/'
            busca2(url,codimdb)
            return(True)
        except Exception as e:
            return(False)
    except Exception as e:
        print("ERRO: " + str(filename))
        return(False)
for filename in glob.glob("*." + str(extensao)):
    if '(tt' not in filename:
        filme = filename.replace("." + str(extensao),"").replace("(n)","").replace("(l)","").replace("(d)","").replace(" ","+")
        parte2 = ""
        if '(' in filme:
            parte2 = filename.replace("." + str(extensao),"").replace("(n)","").replace("(l)","").replace("(d)","").split('(')[1].split(')')[0].replace(" ","+")
        url = 'https://www.google.com/search?q=movie+' + str(filme) + '+imdb+tt00' + filename[2]
        if busca(url) == False:
            filme2 = filename.replace("." + str(extensao),"").replace("(n)","").replace("(l)","").replace("(d)","").replace('(' + parte2 + ')','').replace(" ","+")
            url = 'https://www.google.com/search?q=movie+' + str(filme) + '+imdb+tt00' + filename[2]
            if busca(url) == False:
                filme3 = filename.split("-")[0] + " " + parte2.replace(" ","+")
                url = 'https://www.google.com/search?q=movie+' + str(filme) + '+imdb+tt00' + filename[2]
                busca(url)
    else:
        print(str(filename) + " já indexado" + (str(' ') * (145 - (len(str(filename) + " já indexado")))), end='\r')
