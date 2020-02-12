import requests as rq
from bs4 import BeautifulSoup
import re
def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match
def delStrList(inputStr,delStrList):
    inputStr = str(inputStr)
    for delStr in delStrList:
        inputStr = inputStr.replace(delStr,'')
    inputStr = inputStr.strip()
    return inputStr
#Extract card information from each page of card
#5001 Windstorm of Etaqua Normal Trap
#5002 Valkyrion the Magna Warrior
#5004 Vorse Raider
#there is data starting from 4007
cards = []
#w:overwrite ; a:append
def crawler(locale,write_file_type,from_id,to_id):
    if locale == 'eng':
        attriNames = ['id', 'Name', 'Attribute', 'Level', 'Rank', 'Link', 'Monster Type', 'Card Type', 'ATK', 'DEF', 'Icon',
                      'Description']
        with open('output_english.csv', write_file_type, encoding='utf-8') as file:
            for i in range(from_id, to_id):
                print(i)
                card = []
                for num in range(len(attriNames)):
                    card.append('')
                columnName = 'id'
                index = attriNames.index(columnName)
                card[index] = str(i)
                # url = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='+str(i)+'&request_locale=ja' #jp
                url = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid=' + str(i)+'&request_locale=en'
                response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
                html_doc = response.text  # text 屬性就是 html 檔案
                soup = BeautifulSoup(response.text, "lxml")  # 指定 lxml 作為解析器
                # print(soup.prettify()) # 把排版後的 html 印出來
                removeStrList = ['\t', '\r', '\n', '\\t', '\\r', '\\n', '<br/>']
                columnName = 'Name'
                index = attriNames.index(columnName)
                header_broad_title = soup.findAll('header', {'id': 'broad_title'})
                if len(header_broad_title) > 0:
                    # jp
                    # for string in header_broad_title[0].strings:
                    #     if string[0] == '\r':
                    #         cardName = delStrList(string, removeStrList)
                    cardName = delStrList(header_broad_title[0].find('h1').string, removeStrList)
                    card[index] = cardName
                    # print(cardName)
                else:
                    continue
                div_item_boxs = soup.findAll('div', {'class': 'item_box'})
                for div_item_box in div_item_boxs:
                    title = div_item_box.findAll('span', {'class': 'item_box_title'})[0].find('b').text
                    if title in attriNames:
                        index = attriNames.index(title)
                        value = div_item_box.find('span', {'class': 'item_box_value'})
                        if type(value) == type(None):
                            value = div_item_box.findAll('span', {'class': 'item_box_title'})[0]
                            insertValue = delStrList(div_item_box.contents[-1], removeStrList)
                            card[index] = insertValue
                        else:
                            insertValue = delStrList(value.string, removeStrList)
                            card[index] = insertValue
                columnName = 'Description'
                index = attriNames.index(columnName)
                if soup.findAll('div', {'class': 'item_box_text'})[0].strings:
                    flag = False
                    for string in soup.findAll('div', {'class': 'item_box_text'})[0].strings:
                        if flag:
                            insertValue += '; '+delStrList(string, removeStrList)
                        else:
                            if string[0] == '\r':
                                flag = True
                                insertValue = delStrList(string, removeStrList)
                else:
                    dd_box_card_text = soup.findAll('dd', {'class': 'box_card_text'})
                    insertValue = delStrList(soup.findAll('dd', {'class': 'box_card_text'})[0].contents[-1],
                                             removeStrList)
                card[index] = insertValue
                # cards.append(card)
                # print(card)
                # if card[5] != '':
                #     if card[2] == '' and card[3] == '' and card[4] == '':
                #         print(i)
                for indexOfCard in range(len(card)):
                    file.write(card[indexOfCard])
                    if indexOfCard != len(card) - 1:
                        file.write('\t')
                file.write('\n')
        file.close()
    elif locale == 'jp':
        attriNames = ['id', 'Name', '属性', 'レベル', 'ランク', 'リンク', '種族', 'その他項目', '攻撃力', '守備力', '効果', 'Description']
        with open('output_japanese.csv', write_file_type, encoding='utf-8') as file:
            for i in range(from_id, to_id):
                print(i)
                card = []
                for num in range(len(attriNames)):
                    card.append('')
                columnName = 'id'
                index = attriNames.index(columnName)
                card[index] = str(i)
                url = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='+str(i)+'&request_locale=ja' #jp
                response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
                html_doc = response.text  # text 屬性就是 html 檔案
                soup = BeautifulSoup(response.text, "lxml")  # 指定 lxml 作為解析器
                # print(soup.prettify()) # 把排版後的 html 印出來
                removeStrList = ['\t', '\r', '\n', '\\t', '\\r', '\\n', '<br/>']
                columnName = 'Name'
                index = attriNames.index(columnName)
                header_broad_title = soup.findAll('header', {'id': 'broad_title'})
                if len(header_broad_title) > 0:
                    # jp
                    for string in header_broad_title[0].strings:
                        if string[0] == '\r':
                            cardName = delStrList(string, removeStrList)
                    # cardName = delStrList(header_broad_title[0].find('h1').string, removeStrList)
                    card[index] = cardName
                    # print(cardName)
                else:
                    continue
                div_item_boxs = soup.findAll('div', {'class': 'item_box'})
                for div_item_box in div_item_boxs:
                    title = div_item_box.findAll('span', {'class': 'item_box_title'})[0].find('b').text
                    if title in attriNames:
                        index = attriNames.index(title)
                        value = div_item_box.find('span', {'class': 'item_box_value'})
                        if type(value) == type(None):
                            value = div_item_box.findAll('span', {'class': 'item_box_title'})[0]
                            insertValue = delStrList(div_item_box.contents[-1], removeStrList)
                            card[index] = insertValue
                        else:
                            insertValue = delStrList(value.string, removeStrList)
                            card[index] = insertValue
                columnName = 'Description'
                index = attriNames.index(columnName)
                if soup.findAll('div', {'class': 'item_box_text'})[0].strings:
                    flag = False
                    for string in soup.findAll('div', {'class': 'item_box_text'})[0].strings:
                        if flag:
                            insertValue += '; ' + delStrList(string, removeStrList)
                        else:
                            if string[0] == '\r':
                                flag = True
                                insertValue = delStrList(string, removeStrList)
                else:
                    dd_box_card_text = soup.findAll('dd', {'class': 'box_card_text'})
                    insertValue = delStrList(soup.findAll('dd', {'class': 'box_card_text'})[0].contents[-1],
                                             removeStrList)
                card[index] = insertValue
                # cards.append(card)
                # print(card)
                # if card[5] != '':
                #     if card[2] == '' and card[3] == '' and card[4] == '':
                #         print(i)
                for indexOfCard in range(len(card)):
                    file.write(card[indexOfCard])
                    if indexOfCard != len(card) - 1:
                        file.write('\t')
                file.write('\n')
        file.close()
crawler('jp','a',10000,30000)
crawler('eng','w',4007,30000)