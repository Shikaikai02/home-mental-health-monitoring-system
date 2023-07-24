import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
import time

mood_dict = {"happy":5, "pleased":4, "neutral":3, "sad":2, "angry":1}

while True:
    conn = pymysql.connect(
    host='localhost',
    user='root',
    password='7474574',
    database='homeSystem'
)
    cursor = conn.cursor()
    sql = "select id,name from person"
    cursor.execute(sql)
    res = cursor.fetchall()
    #print(res)
    for i in res:
        id = i[0]
        name = i[1]
        #print(id)
        sql = 'select mood,timestamp from mood where id = %s order by timestamp asc'
        cursor.execute(sql,id)
        res1 = cursor.fetchall()
        mood_list = []
        mood_idx = []
        for m in res1:
            mood = m[0]
            idx = m[1].strftime("%Y-%m-%d %H:%M:%S")
            mood_list.append(mood_dict[mood])
            mood_idx.append("")

        #print(mood_idx)
        #print(mood_list)
        my_dict = {'Mood' : mood_list}
        df = pd.DataFrame(my_dict,index=mood_idx)
        #print(df)
        df.plot()
        # 设置x轴和y轴的刻度和标签
        # plt.xticks([1, 2, 3, 4, 5], ['Jan', 'Feb', 'Mar', 'Apr', 'May'])
        plt.yticks([1, 2, 3, 4, 5], ['angry', 'sad', 'neutral', 'pleased', 'happy'])
        plt.xlabel('Time')
        plt.ylabel('Mood')            
        plt.savefig('./static/picture/{}.png'.format(name))
        print('saved line chart : {}'.format(name))
        plt.close()
        labels = 'angry', 'sad', 'neutral', 'pleased', 'happy'
        sql = 'select count(mood) from mood where id = %s and mood = "happy"'
        cursor.execute(sql,id)
        happy = cursor.fetchall()[0][0]
        sql = 'select count(mood) from mood where id = %s and mood = "pleased"'
        cursor.execute(sql,id)
        pleased = cursor.fetchall()[0][0]
        sql = 'select count(mood) from mood where id = %s and mood = "neutral"'
        cursor.execute(sql,id)
        neutral = cursor.fetchall()[0][0]
        sql = 'select count(mood) from mood where id = %s and mood = "sad"'
        cursor.execute(sql,id)
        sad = cursor.fetchall()[0][0]
        sql = 'select count(mood) from mood where id = %s and mood = "angry"'
        cursor.execute(sql,id)
        angry = cursor.fetchall()[0][0]
        sizes = [angry, sad, neutral, pleased, happy]
        colors = ['#e55252', '#55b2f9', '#8ef7ce', '#e3fb81', '#ffc938']
        fig, ax = plt.subplots(1)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, shadow=False, explode=None)
        ax.axis('equal')
        ax.legend(labels=labels, loc='upper right')
        plt.savefig('./static/picture/{}-pie.png'.format(name))
        print('saved pie chart : {}'.format(name))
        plt.close()
    time.sleep(1)