
import requests
import mysql.connector as my
import json
import re
import os
import glob

conn = my.connect(
                user = 'hamza',
                passwd = '123456',
                host = 'localhost',
                database = 'mydb'    
)

cur = conn.cursor()
cur.execute(f"select * from anime")
data = cur.fetchall()
animes = {}

for dt in data:
    res = []
    for i in dt[0]:
        if re.search('[0-9a-zA-Z]', i):
            res.append(i)
            
    res = ''.join(res)
    res = res.lower()

  
    animes[res] = dt[0]



def read_json(filename):
    j = open(filename, 'r', encoding='utf-8')
    j = json.load(j)


    cl = {}

    for i in range(len(j)):
        cl[j[i]['name']] = j[i]['id']

    return cl


def witanime(html):
    
    i = 0
    an = '''<div class="anime-card-poster">
<div class="hover ehover6">
<img class="img-responsive" src="https://witanime.com/wp-content/uploads/'''
    
    t = '" alt="'

    
    
    u = '''" />'''
    
    ln = len(t)
    
    
    while True:
        i = html.find(an, i)
        if i == -1:
            break

        i = html.find(t, i)
        i = i+ln
        e = html.find(u, i)

        res = []
        for x in html[i:e]:
            if re.search('[0-9a-zA-Z]', x):
                res.append(x)
                
        res = ''.join(res)
        res = res.lower()

        if not res in animes:
            w.write(html[i:e] + '\n' )



def run():
    w = open('names.txt', 'w', encoding='utf-8')
    for zx in range(1,27):
        url = f'https://witanime.com/قائمة-الانمي/page/{zx}/'
        #url = f'https://ww.anime4up.com/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A-fg1/page/{zx}'
        r = requests.get(url)
        html = r.text
        witanime(html)
        
        #print(url)
    w.close()

# class
cur = conn.cursor()
cur.execute(f"select * from anime_class")
data = cur.fetchall()
cl = {}

for dt in data:
    cl[dt[1]] = f'{dt[0]}'

cur.execute(f"select max(id) from anime_class")
data = cur.fetchall()[0][0]

if data == None:
    data = 1
else:
    data = int(data)+1
    
cl['max_id'] = data

# type
types = {
    'TV': '6',
    'Special': '7',
    'OVA': '8'
}
# state
states = {
    'مكتمل': '3'
}
# date
cur = conn.cursor()
cur.execute(f"select * from anime_date")
data = cur.fetchall()
dates = {}

for dt in data:
    dates[dt[1]] = f'{dt[0]}'
    
def episodes():
    cur.execute("select * from liens")
    data = cur.fetchall()
    liens = {}
    for dt in data:
        liens[f"{dt[0]}:{dt[2]}"] = ''

    cur.execute("select * from images")
    data = cur.fetchall()
    images = {}
    for dt in data:
        images[dt[0]] = ''

    cur.execute("select max(id) from anime")
    id_anime = cur.fetchall()[0][0]
    if id_anime == None:
        id_anime = 1
    else:
        id_anime = int(id_anime)+1
        
    
    
    cur.execute("select max(id) from liens")
    max_id_lien = cur.fetchall()[0][0]
    if max_id_lien == None:
        max_id_lien = 1
    else:
        max_id_lien = int(max_id_lien)+1

        
    w = open('names.txt', 'r', encoding='utf-8')
    t_img = '''<div class="second-section">
<div class="container">
<div class="anime-info-container">
<div class="anime-info-right">
<div class="anime-thumbnail">
<img src="'''
    ln_img = len(t_img)
    
    t_class = '<li><a href="https://witanime.com/anime-genre/'
    et_class = '</a></li>'
    ln_class = len(t_class)
    ind = 0
    t_story = '<p class="anime-story">'
    ln_story = len(t_story)
    t_type = '<div class="anime-info"><span>النوع:</span> <a href="https://witanime.com/anime-type/'
    ln_type = len(t_type)

    t_state = '<div class="anime-info"><span>حالة الأنمي:</span> <a href="https://witanime.com/anime-status/'
    ln_state = len(t_state)

    t_time = '<div class="anime-info"><span>مدة الحلقة:</span> '
    ln_time = len(t_time)

    t_number = '''<div class="anime-info">
<span>عدد الحلقات:</span>
'''
    ln_number = len(t_number)

    t_date = '<div class="anime-info"><span>الموسم:</span> <a href="https://witanime.com/anime-season/'
    ln_date = len(t_date)

    t_eps = '''<div class="episodes-card">
<div class="hover ehover6">
<div class="episodes-card-title">
<h3><a href="'''
    ln_eps = len(t_eps)

    for line in w:
        line = line.strip('\n')
        line = line.strip('.')
        line = line.strip('!')
        line = line.lower()
        
        if line[-1] == ' ':
            line = line[:-1]

        url = line.replace(' ', '-')
        r = requests.get(f'https://witanime.com/anime/{url}/')
        html = r.text

        # episodes
        while True:
            s_eps = html.find(t_eps, ind)+ln_eps

            if s_eps == -1+ln_eps:
                break
            e_eps = html.find('">', s_eps)
            ee_eps = html.find("</a></h3>", e_eps)
            ind = e_eps

            res = []
            lien = html[s_eps:e_eps]

            for i in html[e_eps+2:ee_eps]:
                if i.isdigit():
                    res.append(i)
            res = ''.join(res)
            ind = ee_eps
            if not f"{line}:{res}" in liens:
                '''
                cur.execute(f"delete from liens where episode='{lien}' ")
                conn.commit()
                '''
                liens[f"{line}:{res}"] = ''
                cur.execute(f"insert into liens values('{line}', '{lien}', '{res}', '', {max_id_lien}, '1')")
                #conn.commit()
                max_id_lien+=1
        
        
        # img
        s_img = html.find(t_img, 0)+ln_img
        e_img = html.find('" class="thumbnail img-responsive"', s_img)
        ind = e_img

        anime_image = html[s_img:e_img]
        # class anime
        anime_class = []
        while True:
            s_class = html.find(t_class, ind)
            if s_class == -1:
                break
            
            ind = s_class+ln_class
            s_class = html.find('">', ind)+2
            
            e_class = html.find(et_class, ind)
            ind = e_class

            if not html[s_class:e_class] in cl:
                cur.execute(f"insert into anime_class values({cl['max_id']}, '{html[s_class:e_class]}')")
                #conn.commit()
                cl[html[s_class:e_class]] = str(cl['max_id'])
                cl['max_id'] +=1

            anime_class.append(cl[html[s_class:e_class]])

        anime_class = ','.join(anime_class)

        # story
        s_story = html.find(t_story, e_img)+ln_story
        e_story = html.find('</p>')
        ind = e_story

        anime_story = html[s_story:e_story]
        # type
        s_type = html.find(t_type, ind)+ln_type
        s_type = html.find('">', s_type)+2
        ind = s_type

        e_type = html.find('</a></div>', ind)
        ind = e_type

        anime_type = types[html[s_type:e_type]]
        # state
        s_state = html.find(t_state, ind)+ln_state
        s_state = html.find('">', s_state)+2
        ind = s_state

        e_state = html.find('</a></div>', ind)
        ind = e_state

        anime_state = states[html[s_state:e_state]]
        # number
        s_number = html.find(t_number, ind)+ln_number
        ind = s_number

        e_number = html.find(' </div>', ind)
        ind = e_number

        anime_number = html[s_number:e_number]
        # time
        s_time = html.find(t_time, ind)+ln_time
        ind = s_time

        e_time = html.find('</div>', ind)
        ind = e_time

        anime_time = html[s_time:e_time]

        # date
        s_date = html.find(t_date, ind)+ln_date
        s_date = html.find('">', s_date)+2
        ind = s_date

        e_date = html.find('</a></div>', ind)
        ind = e_date

        anime_date = dates[html[s_date:e_date]]

        name_img = line.replace(' ', '-') + ' anime.png'
        if not line in images:
            ri = requests.get(anime_image)
            if r.status_code == 200:
                with open(f"anime/{name_img}", 'wb') as f:
                    f.write(ri.content)
                    cur.execute(f"insert into images values('{line}')")
                    
                #conn.commit()

        
        cur.execute(f"insert into anime values('{line}', '{anime_story}', '{anime_class}', '{anime_type}', '{anime_state}', '{anime_date}', 'photos/anime/{name_img}', '{anime_number}', '', '15', {id_anime})")
        
        id_anime +=1
        print(line)
        
        '''
        print(anime_date)
        print(anime_time)
        print(anime_story)
        print(anime_class)
        print(anime_number)
        print(anime_state)
        print(anime_type)
        '''
        

    w.close()
    conn.commit()

def liens_add():
    cur.execute(f"select * from liens where work='1' ")
    data =cur.fetchall()
    t_episode = '<iframe id="WitAnime1-episode-iframe" src="'
    ln_episode = len(t_episode)

    for dt in data:
        r = requests.get(dt[1])
        html = r.text

        s = html.find(t_episode)+ln_episode
        e = html.find('" frameborder="0" allowfullscreen></iframe>', s)

        try:
            re = requests.get(html[s:e])
            if re.status_code == 200:
                cur.execute(f"update liens set work='yes', episode='{html[s:e]}' where lien='{dt[1]}' ")
                conn.commit()
        except:
            print("Failed")
        
def delete_names():
    w = open('names.txt', 'r', encoding='utf-8')
    for line in w:
        line = line.strip('\n')
        line = line.strip('.')
        line = line.strip('!')
        line = line.lower()

        cur.execute(f"delete from images where name='{line}' ")
    w.close()
    conn.commit()

delete_names()
#episodes()













            
