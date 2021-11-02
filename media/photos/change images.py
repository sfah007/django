

import requests
import json
import os
import mysql.connector as my
import glob

conn = my.connect(
            user = 'hamza',
            passwd = '123456',
            host = 'localhost',
            database = 'mydb'
)




def read_json(filename):
    j = open(filename, 'r', encoding='utf-8')
    j = json.load(j)


    cl = {}

    for i in range(len(j)):
        cl[j[i]['name']] = j[i]['id']

    return cl

def read_json_all(filename):
    j = open(filename, 'r', encoding='utf-8')
    j = json.load(j)


    return j


cur = conn.cursor()
cur.execute(f"select name, id from anime")
data = cur.fetchall()

t_img = '''<div class="anime-thumbnail-pic">                
            <img src="'''
ln = len(t_img)

def to(n):
    res = []

    while n != 0:
        if n%2 == 0:
            res.append('0')
        else:
            res.append('1')
        n = n//2
        
    return ''.join(res[::-1])

os.chdir('anime')
files = glob.glob('*.png')
images = {}
for file in files:
    images[file[:-4]] = ''

'''
for dt in data:
    url = dt[0].replace(' ','-')
    r = requests.get(f'https://animelek.me/anime/{url}')
    if r.status_code == 200:
        nb = to(int(dt[1]))
        if nb in images:
            continue
        
        html = r.text
        s = html.find(t_img)+ln
        e = html.find('" class="thumbnail img-responsive" ', s)

        re = requests.get(html[s:e].strip(' '))
        if re.status_code == 200:
            
            with open(f"{nb}.png", 'wb') as f:
                f.write(re.content)
                cur.execute(f"update anime set image_anime='photos/anime/{nb}' where name='{dt[0]}'")
'''

                
def insert():
    cur.execute(f"select max(id) from liens ")
    max_id = cur.fetchall()[0][0]
    if max_id == None:
        max_id = 1
    else:
        max_id = int(max_id)+1

    name = input('Name : ')
    lien = input('Lien : ')
    number = input('Number : ')
    episode = input('Episode : ')
    work = input('Work : ')

    cur.execute(f"insert into liens values('{name}', '{lien}', '{number}', '{episode}', {max_id}, '{work}')")
    conn.commit()
    max_id+=1

print(to(834))
print(to(835))
print(to(836))

        
























        
