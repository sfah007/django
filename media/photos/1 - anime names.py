

import requests
import mysql.connector as my
import json

conn = my.connect(
                user = 'hamza',
                passwd = '123456',
                host = 'localhost',
                database = 'mydb'    
)


w = open('names.txt', 'w', encoding='utf-8')

def read_json(filename):
    j = open(filename, 'r', encoding='utf-8')
    j = json.load(j)


    cl = {}

    for i in range(len(j)):
        cl[j[i]['name']] = j[i]['id']

    return cl

cur = conn.cursor()
cur.execute(f"select * from anime_date")
data = cur.fetchall()
dates = {}

for dt in data:
    dates[dt[1]] = str(dt[0])

out = []
def animelek(html):
    
    i = 0
    an = '<span ><a href="https://animelek.me/anime/'
    u = '/" class="overlay"></a></span>'
    ln = len(an)
    t_story = '''data-toggle="popover" data-trigger="hover"
            data-placement="top"
            data-content="'''
    ln_story = len(t_story)

    t_date = '''<h4><a a style="color:#969696;" href="https://animelek.me/anime/'''
    ln_date = len(t_date)

    t_name = '<div class="anime-card-title" title="'
    ln_name = len(t_name)
    while True:
        i = html.find(an, i)
        if i == -1:
            break
        res = {}
        i = i+ln
        e = html.find(u, i)

        url = html[i:e]

        # story
        s_story = html.find(t_story, e)+ln_story
        e_story = html.find('">', s_story)
        story = html[s_story:e_story]
        i = e_story

        '''
        # name
        s_name = html.find(t_name, i)+ln_name
        s_name = html.find('">', s_name)+2
        e_name = html.find("</a></h3>", s_name)
        name = html[s_name:e_name]
        i = e_name
        name = name.strip('.')
        name = name.strip('!')
        name = name.lower()'''
        
        
        # date
        s_date = html.find(t_date, i)+ln_date
        s_date = html.find('">', s_date)+2
        e_date = html.find("</a></h4>", s_date)

        anime_date = dates[html[s_date:e_date]]
        i = e_date

        res['url'] = url
        res['name'] = url.replace('-', ' ')
        res['story'] = story
        res['anime_date'] = anime_date
           
        
        out.append(res)
    

def anime4up(html):
    
    i = 0
    an = '''" />
<a href="https://ww.anime4up.com/anime/'''
    
    u = '/" class="overlay"></a>'
    ln = len(an)
    cur = conn.cursor()
    cur.execute(f"select * from anime")
    data = cur.fetchall()
    animes = {}

    for dt in data:
        animes[dt[0].strip(' ')] = ''
    
    while True:
        i = html.find(an, i)
        if i == -1:
            break
        i = i+ln
        e = html.find(u, i)
        
        
        if not html[i:e].strip('-') in animes:
            print(html[i:e])

def getdata():
    url = f'https://animelek.me/قائمة-الأنمي'
    r = requests.get(url)
    html = r.text
    t = '''<li role="presentation">
                                    <a href="https://animelek.me/anime-genre/'''
    ln = len(t)

    cl = read_json('class.json')
    
    s = 0
    out = []
    i = 56
    while s != -1:
        
        s = html.find(t, s)
        if s == -1:
            break
        s = s+ln
    
        s = html.find('/">', s)
        s=s+3
        e = html.find('</a>', s)
        

        if not html[s:e].strip('-') in cl:
            res = {}
            res['id'] = i
            res['name'] = html[s:e]
            i+=1
            out.append(res)
    file = open('class2.json', 'w', encoding='utf-8')
    file.write(str(json.dumps(out, ensure_ascii = False)))
    file.close()

    

#getdata()

for zx in range(1,36):
    url = f'https://animelek.me/قائمة-الأنمي/?page={zx}'
    #url = f'https://ww.anime4up.com/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A-fg1/page/{zx}'
    r = requests.get(url)
    html = r.text
    animelek(html)
    print(zx)
w.close()  

file = open('names.json', 'w', encoding='utf-8')
file.write(str(json.dumps(out, ensure_ascii = False)))
file.close()








