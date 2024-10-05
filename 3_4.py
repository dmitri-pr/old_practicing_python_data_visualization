import urllib.error
import ssl
import re
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://gogov.ru/covid-19/world#sources'
document = urlopen(url, context=ctx)
html = document.read()  # .decode()

soup = BeautifulSoup(html, "html.parser")
table = soup.find(lambda tag: tag.name == 'table' and tag.find(lambda ttag: ttag.name == 'i' and re.search('\(\+.+',
                                                                                                           ttag.text)))  # ttag.text=='')) #tag.has_attr('class') and tag['class']=='info-table')
rows = table.find_all(lambda tag: tag.name == 'tr')

data = []

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip().replace(' ', '').replace('(', ' (') for ele in cols]
    data.append([ele for ele in cols if ele])
data.remove(data[0])

fhand = open('Final.txt', 'w')
fhand.write('на Дату' + '     Случаев заражения' + '     Умерло' + '     Выздоровело' + '    Заражено сейчас' + '\n\n')

print('на Дату' + '     Случаев заражения' + '     Умерло' + '     Выздоровело' + '    Заражено сейчас' + '\n')

x = []
y1 = []
y2 = []
y3 = []
y4 = []

d = dict()
d['на Дату'] = []
d['Случаев заражения'] = []
d['Умерло'] = []
d['Выздоровело'] = []
d['Заражено сейчас'] = []

for index, elements in enumerate(data):
    if elements[3] == '0': data[index][3] = '130899063'
    items_1 = elements[1].split()
    items_2 = elements[2].split()
    value = int(items_1[0]) - int(items_2[0]) - int(elements[3])
    fhand.write(
        elements[0] + '   ' + elements[1] + '   ' + elements[2] + '   ' + elements[3] + '   ' + str(value) + '\n')
    print(elements[0] + '   ' + elements[1] + '   ' + elements[2] + '   ' + elements[3] + '   ' + str(value))
    x.append(elements[0])
    d['на Дату'].append(elements[0])
    # print(x, '\n\n')
    y1.append(items_1[0])
    d['Случаев заражения'].append(int(items_1[0]))
    # print(y1)
    y2.append(items_2[0])
    d['Умерло'].append(int(items_1[0]))
    # print(y2)
    y3.append(elements[3])
    d['Выздоровело'].append(int(elements[3]))
    # print(y3)
    y4.append(str(value))
    d['Заражено сейчас'].append(value)
    # print(y4, '\n\n')

df = pd.DataFrame(d)
df.to_excel('COVID-19.xlsx', sheet_name='Statistics', index=False)

x.reverse()
# print(x, '\n\n')
y1.reverse()
y1 = [int(item) for item in y1]
y2.reverse()
y2 = [int(item) for item in y2]
y3.reverse()
y3 = [int(item) for item in y3]
y4.reverse()
y4 = [int(item) for item in y4]

# print(y1, '\n\n')
# print(y2, '\n\n')
# print(y3, '\n\n')
# print(y4, '\n\n')

y1 = tuple(y1)
y2 = tuple(y2)
y3 = tuple(y3)
y4 = tuple(y4)

y2_n = y2
y4_n = tuple(map(lambda i, j: i - j, y4, y2))
y3_n = tuple(map(lambda i, j: i - j, y3, y4))
y1_n = tuple(map(lambda i, j: i - j, y1, y3))

y1 = list(y1_n)
y2 = list(y2_n)
y3 = list(y3_n)
y4 = list(y4_n)

# print(y1_n, '\n\n')
# print(y2_n, '\n\n')
# print(y3_n, '\n\n')
# print(y4_n, '\n\n')

# start_date = '01.02.20'
# date_1 = datetime.datetime.strptime(start_date, "%d.%m.%y")

for index, item in enumerate(x):
    x[index] = datetime.datetime.strptime(item, "%d.%m.%y")

fig, ax = plt.subplots(figsize=(5, 3))
ax.stackplot(x, [y2, y4, y3, y1], labels=['Умерло', 'Заражено сейчас', 'Выздоровело', 'Случаев заражения'])
ax.set_title('Статистика по заболеваемости COVID-19')
ax.legend(loc='upper left')
ax.set_ylabel('Количество (в 100 млн)')
ax.set_xlim(xmin=x[0], xmax=x[-1])
fig.tight_layout()

plt.show()
