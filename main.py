#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
import re
from tkinter import messagebox
import sys
import subprocess
import os
from dataclasses import dataclass
import pickle
from win10toast import ToastNotifier
toaster = ToastNotifier()

domain = 'http://www.silverstonef1.ru/'
update_page = "http://www.silverstonef1.ru/obnovleniya"
model='SSHybridSbot' # SilverStone F1 Hybrid S-BOT
db_string = 'База камер'
fw_string = 'Прошивка для комбо-устройства'
rd_string = 'Прошивка RD'

@dataclass
class Version:
    db: str = ''
    fw: str = ''
    rd: str = ''

Ver = None

def download(link, filename):
    ret = False
    try:
        fw = urllib.request.urlopen(link)
        # trying to save fw file
        try:
            print('Downloading data...')
            data = fw.read()
            print('Saving to file...')
            config = open(filename, 'wb')
            config.write(data)
            config.close()
            print('saved to ', filename)
            toaster.show_toast('Загрузка файла',"Файл" + filename +" успешно сохранен")
            #messagebox.showinfo(message="Файл успешно сохранен", icon='info',
            #                    title='Загрузка файла')
            ret = True

            # if messagebox.askyesno(message='Открыть папку с файлом?', icon='question',
            #                     title='Загрузка файла') is True:
            #     fw_path = os.getcwd() + '/' + filename
            #     print(fw_path)
            #     subprocess.Popen(r'explorer /select, ' + fw_path)
        except:
            print('Could not write file!')
            toaster.show_toast('Загрузка файла',"Ошибка при сохранении файла "+ filename + " !")
            # messagebox.showinfo(message="Ошибка при сохранении файла!", icon='error',
            #                     title='Загрузка файла')
            ret = False
    except urllib.error.HTTPError:
        print('Not found :(')
        toaster.show_toast('Загрузка файла',"Не удалось скачать файл!")
        # messagebox.showinfo(message="Не удалось скачать файл!", icon='error',
        #                     title='Ошибка!')
        ret = False
        pass
    return ret

def ver_save():
    with open('version.dat', 'wb') as f:
        pickle.dump(Ver, f)

# read version from file
try:
    with open('version.dat', 'rb') as f:
        Ver = pickle.loads(f.read())

    print('Last checked version:', Ver.fw)
except:
    print('Could not open version file!')
    Ver = Version()

# open updates page
update_page = urllib.request.urlopen(update_page)

str_var = ''
new_str = ''
version_latest = ''

# parsing with BeautifulSoup4
soup = BeautifulSoup(update_page.read().decode(), "html.parser")
div_tag = soup.find('div', id=model)
if div_tag is not None:
    for p_tag in div_tag.find_all('p', class_='b-tabs-content-text'):
        if p_tag is not None:
            #print(p_tag.text)
            # db
            if p_tag.text.find(db_string) != -1:
                ver_db = p_tag.contents[1][4:-4]
                if ver_db != Ver.db:
                    print('FOUND NEW DB VERSION!', ver_db)
                    toaster.show_toast('База радаров',"Обнаружена новая версия базы радаров")
                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        print('Downloading from ', download_link)
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.db = ver_db
                            ver_save()
                else:
                    print('NO NEW DB VERSION(((', ver_db)
                continue
            # fw
            if p_tag.text.find(fw_string) != -1:
                ver_fw = p_tag.contents[1][4:-4]
                if ver_fw != Ver.fw:
                    print('FOUND NEW FW VERSION!', ver_fw)
                    toaster.show_toast('Прошивка',"Обнаружена новая версия прошивки регистратора")
                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        print('Downloading from ', download_link)
                        #download(download_link, download_link.split('/')[-1])
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.fw = ver_fw
                            ver_save()
                else:
                    print('NO NEW FW VERSION(((', ver_fw)
                continue
            
            # rd
            if p_tag.text.find(rd_string, 0, 30) != -1:
                ver_rd = p_tag.contents[1][4:-4]
                if ver_rd != Ver.rd:
                    print('FOUND NEW FW VERSION!', ver_rd)
                    toaster.show_toast('Прошивка радар-детектора',"Обнаружена новая версия прошивки радар-детектора")
                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        print('Downloading from ', download_link)
                        #download(download_link, download_link.split('/')[-1])
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.rd = ver_rd
                            ver_save()
                else:
                    print('No NEW FW VERSION(((', ver_rd)
                continue

