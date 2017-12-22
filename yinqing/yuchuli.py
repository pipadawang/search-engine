import os
import sys
import re
import chardet


#扫描文件夹下面所有的文件，并保存在文件目录备份表中
lujing=input("请输入文件夹路径：")
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):         # 如果是文件则添加进 fileList
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):   # 如果是文件夹
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList
# 主函数
# 重定向输出位置
output = sys.stdout
outputfile = open('lujing.txt', 'w')
sys.stdout = outputfile
list = GetFileList(lujing, []) # 获取所有myFolder文件夹下所有文件名称（包含拓展名）
# 输出所有文件夹中的路径（相对于当前运行的.py文件的相对路径）
for route in list:
    # route 为路径
    print(route)
# 关闭输出重定向
outputfile.close()
sys.stdout = output


#将生成的路径文件lujing.txt读取，并按照路径文件对文本处理，去标签
for line in open("lujing.txt"):
    print(line)
    #line=line[0:-2]
    line1=line[0:12]
    line2=line[13:16]
    line3=line[17:-1]
    line4=line[17:-6]
    line=line1+'\\'+line2+'\\'+line3
    print(line4)
    path=line
    fb=open(path,"rb")
    data = fb.read()
    bianma = chardet.detect(data)['encoding']#获取当前文件的编码方式，并按照此编码类型处理文档
    page=open(line,'r',encoding=bianma,errors='ignore').read()
    dr = re.compile(r'<[^>]+>', re.S)#去HTML标签
    dd = dr.sub('', page)
    print(dd)
    fname='TXT'+"\\"+line4+ ".txt"
    #print(fname)
    f = open(fname, "w+", encoding=bianma)#将去标签的文件写到文件夹内，并按照原命名以txt文档方式保存
    #fo=open(fname,"w+")
    f.write(dd)