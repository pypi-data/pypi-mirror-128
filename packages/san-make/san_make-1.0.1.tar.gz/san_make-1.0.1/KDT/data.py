#coding=utf8
def dataread():
    with open('D:\python test\KDT\data.txt',encoding='utf8') as f:
        li=f.readlines()
        lii=[]
    for i in li:
        if not i.startswith('#')==True:
            # li.remove(i)
            lii.append(i)
    return lii


if __name__ == '__main__':
    i=dataread()
    i.remove('singleclick,id=su\n')
    print(i)

