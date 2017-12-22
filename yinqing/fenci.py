import jieba
import chardet
import sqlite3
import importlib,sys
importlib.reload(sys)

conn = sqlite3.connect('suoyin.db3')
conn.text_factory = str

c = conn.cursor()
# 当已存在数据库的时候，需要将表删除，若不存在或第一次运行，则需要注释掉
c.execute('drop table doc')
c.execute('create table doc (id int primary key,link text)')
c.execute('drop table word')
c.execute('create table word (term varchar(25) primary key,list text)')
conn.commit()
conn.close()

def Fenci():
    num = 0
    for line in open("lujing.txt"):
        lujing=line
        print(1111111)
        print(lujing)
        num += 1
        print(line)
        line=line[17:-5]
        print(line)
        #line1 = line[0:3]
        #print(line1)
        #line2 = line[4:-1]
        #print(line2)
        line = 'TXT' + '\\' + line+'Txt'#line为文件位置
        print(line)#文件名称
        path = line
        fb = open(path, "rb")
        data = fb.read()
        bianma = chardet.detect(data)['encoding']#获取文件编码        print(bianma)
        #page = open(line, 'r', encoding=bianma, errors='ignore').read()

        #page1=page.decode('UTF-8')
        if bianma=='UTF-16':
            data = data.decode('UTF-16')
            data = data.encode('utf-8')
        word=jieba.cut_for_search(data)
        seglist = list(word)
        print(seglist)

        conn = sqlite3.connect('suoyin.db3')  # 创建数据库
        c = conn.cursor()  # 创建游标
        c.execute('insert into doc values(?,?)', (num,lujing))
       # 对每个分出的词语建立词表
        for word in seglist:
            #print(word)
        # 检验看看这个词语是否已存在于数据库
            c.execute('select list from word where term=?', (word,))
            result = c.fetchall()
        # 如果不存在
            if len(result) == 0:
                docliststr = str(num)
                c.execute('insert into word values(?,?)', (word, docliststr))
        # 如果已存在
            else:
                docliststr = result[0][0]  # 得到字符串
                docliststr += ' ' + str(num)
                c.execute('update word set list=? where term=?', (docliststr, word))
        conn.commit()
        conn.close()

Fenci()