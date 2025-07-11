#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
from dataclasses import dataclass
import pickle
import requests
from notifypy import Notify

notification = Notify("", "", "Silverstone_updater")

domain = 'https://silverstonef1.ru'
update_page = "https://silverstonef1.ru/update/?pid=1004&cat=kombo-ustrojstva#support-block"
model = 'support-info-1'  # SilverStone F1 Hybrid S-BOT
db_string = 'База камер для'
fw_string = 'Прошивка SW'
rd_string = 'Прошивка RD'
uz_string = '_UZ_'


@dataclass
class Version:
    db: str = ''
    fw: str = ''
    rd: str = ''


Ver = None


def download(link, filename):
    ret = False
    try:
        # trying to save fw file
        try:
            print('Downloading data...')
            with open(filename, 'wb') as f:
                resp = requests.get(link, verify=False)
                f.write(resp.content)

            notification.title = "Загрузка файла"
            notification.message = "Файл " + filename + " успешно сохранен"
            notification.send()
            ret = True
        except:
            print('Could not write file!')

            notification.title = "Загрузка файла"
            notification.message = "Ошибка при сохранении файла " + filename + " !"
            notification.send()
            ret = False
    except urllib.error.HTTPError:
        print('Not found :(')
        notification.title = "Загрузка файла"
        notification.message = "Не удалось скачать файл!"
        notification.send()
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

    print('Last checked version:', Ver)
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
    for p_tag in div_tag.find_all('p'):
        if p_tag is not None:
            # db
            if p_tag.text.find(db_string) != -1:
                ver_db = p_tag.contents[1][4:-4]
                if ver_db != Ver.db:
                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        if download_link.find(uz_string) != -1:
                            continue
                        print('FOUND NEW DB VERSION!', ver_db)
                        notification.title = "База радаров"
                        notification.message = "Обнаружена новая версия базы радаров"
                        notification.send()
                        print('Downloading from ', download_link)
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.db = ver_db
                            ver_save()
                else:
                    print('NO NEW DB VERSION(((', ver_db)
                    notification.title = "База радаров"
                    notification.message = "Новая версия базы радаров не найдена"
                    notification.send()
                continue
            # fw
            if p_tag.text.find(fw_string) != -1:
                ver_fw = p_tag.contents[1][4:-4]
                if ver_fw != Ver.fw:

                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        if download_link.find(uz_string) != -1:
                            continue
                        print('FOUND NEW FW VERSION!', ver_fw)
                        notification.title = "Прошивка"
                        notification.message = "Обнаружена новая версия прошивки регистратора"
                        notification.send()
                        print('Downloading from ', download_link)
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.fw = ver_fw
                            ver_save()
                else:
                    print('NO NEW FW VERSION(((', ver_fw)
                    notification.title = "Прошивка"
                    notification.message = "Новая версия прошивки регистратора не найдена"
                    notification.send()
                continue
            # rd
            if p_tag.text.find(rd_string, 0, 30) != -1:
                ver_rd = p_tag.contents[1][4:-4]
                if ver_rd != Ver.rd:
                    a_tag = p_tag.find('a')
                    if a_tag is not None:
                        download_link = domain + a_tag['href']
                        if download_link.find(uz_string) != -1:
                            continue
                        print('FOUND NEW RD VERSION!', ver_rd)
                        notification.title = "Прошивка радар-детектора"
                        notification.message = "Обнаружена новая версия прошивки радар-детектора"
                        notification.send()
                        print('Downloading from ', download_link)
                        if download(download_link, download_link.split('/')[-1]):
                            Ver.rd = ver_rd
                            ver_save()
                else:
                    print('NO NEW RD VERSION(((', ver_rd)
                    notification.title = "Прошивка радар-детектора"
                    notification.message = "ОНовая версия прошивки радар-детектора не найдена"
                    notification.send()
                continue
