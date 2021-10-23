


import requests
import json

import mysql.connector as my

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

types = {
    'TV': '6',
    'OVA': '8',
    'ONA': '9',
    'Special': '7',
    'Movie': '10',
}

    

def animes_inf():
    cur = conn.cursor()
    cur.execute('select max(id) from anime')
    max_id_anime = cur.fetchall()[0][0]

    if max_id_anime == None:
        max_id_anime = 1
    else:
        max_id_anime = int(max_id_anime)+1

    cur.execute('select name from anime')
    animes = cur.fetchall()
    d = {}
    for i in animes:
        d[i[0]] = ''
        
    cur.execute('select * from anime_class')
    data = cur.fetchall()
    clases = {}
    for i in data:
        clases[i[1]] = str(i[0])

    
    data_names = read_json_all('names.json')

    cur.execute("select * from liens ")
    data = cur.fetchall()
    liens = {}
    line = 0 
    for i in data:
        liens[i[1]] = ''

    # variables
    # type
    t_type = '''<small>النوع</small>
            <small><a href="https://animelek.me/anime-type/'''
    ln_type = len(t_type)

    # number episode
    t_nmep = '''<div class="full-list-info">
            <small>عدد الحلقات</small>
                        <small>'''
    ln_nmep = len(t_nmep)

    # class
    t_class = '<li><a href="https://animelek.me/anime-genre/'
    ln_class = len(t_class)

    # episode
    y_episode = '<h3><a style="color:#969696;" href="'
    t_episode = y_episode + 'https://animelek.me/episode/'
    ln_episode = len(y_episode)

    # image
    t_img = '''<div class="anime-thumbnail-pic">                
            <img src="'''
    ln_img = len(t_img)

    for dt in data_names:
        line+=1
        if dt['name'] in d:
            continue
        index = 0
        r = requests.get(f"https://animelek.me/anime/{dt['url']}")
        if r.status_code != 200:
            continue
        html = r.text
        
        # image

        s_img = html.find(t_img, index)+ln_img
        e_img = html.find('" class="thumbnail img-responsive"', s_img)
        image = html[s_img:e_img]

        rimg = requests.get(image)
        if r.status_code == 200:
            with open(f"anime/{dt['url']}-anime.png", 'wb') as f:
                f.write(r.content)

        # type
        s_type = html.find(t_type, index)+ln_type
        s_type = html.find('">', s_type)+2
        e_type = html.find('</a></small>', s_type)

        anime_type = types[html[s_type:e_type]]
        index = e_type

        # number episodes
        s_nmep = html.find(t_nmep, index)+ln_nmep
        e_nmep = html.find('</small>', s_nmep)

        number_episodes = html[s_nmep:e_nmep]
        index = e_nmep

        #print(number_episodes)

        # class
        anime_class = []

        while True:
            s_class = html.find(t_class, index)+ln_class
            if s_class == -1+ln_class:
                break
            
            s_class = html.find('">', s_class)+2
            e_class = html.find('</a></li>', s_class)

            anime_class.append(clases[html[s_class:e_class]])

            index = e_class

        anime_class = ','.join(anime_class)
        cur.execute(f"""insert into anime values(
                    '{dt['name']}', '{dt['story']}', '{anime_class}', '{anime_type}', '3',
                    '{dt['anime_date']}', 'photos/anime/{dt['url']}-anime.png', '{number_episodes}', '', '15', {max_id_anime})""")
        conn.commit()
        max_id_anime+=1
        print(f'{line} :', dt['name'])
        
    
        
        
        

        
        
animes_inf()
    


'''
while True:
            ss_episode = html.find(t_episode, index)+ln_episode
            if ss_episode == -1+ln_episode:
                break
            
            s_episode = html.find('">', ss_episode)+2
            
            lien_episode = html[ss_episode:s_episode-2]
            
            if lien_episode in liens:
                continue
            
            e_episode = html.find('</a></h3>', s_episode)

            episode_number = html[s_episode:e_episode]

            res = []

            for i in episode_number:
                if i.isdigit():
                    res.append(i)
            res = ''.join(res)

            cur.execute(f"insert into ")

            index = e_episode
        break'''




 
