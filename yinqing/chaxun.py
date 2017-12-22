
import sqlite3
import jieba
import math

conn=sqlite3.connect("suoyin.db3")
c=conn.cursor()
c.execute('select count(*) from doc')
N=1+c.fetchall()[0][0]#文档总数
target=input('请输入搜索词：')
seggen=jieba.cut_for_search(target)
score={}#文档号：匹配度
for word in seggen:
    print('得到查询词：',word)
    #计算score
    tf={}#文档号：文档数
    c.execute('select list from word where term=?',(word,))
    result=c.fetchall()
    if len(result)>0:
        doclist=result[0][0]
        doclist=doclist.split(' ')
        doclist=[int(x) for x in doclist]#把字符串转换为元素为int的list
        df=len(set(doclist))#当前word对应的df数
        idf=math.log(N/df)
        print('idf：',idf)
        for num in doclist:
            if num in tf:
                tf[num]=tf[num]+1
            else:
                tf[num]=1
        #tf统计结束，现在开始计算score
        for num in tf:
            if num in score:
                #如果该num文档已经有分数了，则累加
                score[num]=score[num]+tf[num]*idf
            else:
                score[num]=tf[num]*idf
sortedlist=sorted(score.items(),key=lambda d:d[1],reverse=True)
#print('得分列表',sortedlist)

cnt=0
for num,docscore in sortedlist:
    cnt=cnt+1
    c.execute('select link from doc where id=?',(num,))
    url=c.fetchall()[0][0]
    print("当前关联度排名：",cnt)
    print('文件路径：',url,'匹配度：',docscore)

    if cnt>20:
        break
if cnt==0:
    print('无搜索结果，请更换关键词重试')