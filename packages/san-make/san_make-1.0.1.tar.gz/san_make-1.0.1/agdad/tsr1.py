#cording=utf-8

'''例2：
    声明一个资金类，保存3个类属性，分别保存销售总额、食品类销售额、服饰类销售额；声明类方法用于更新销售额，根据销售的商品类别进行更新
声明一个销售类，包含实例属性（商品名称、类别、单价、销售数量），销售完成后需要更新销售总额、不同品类销售额
'''
import random
import time,threading


class Money:
    toal=0
    foodmoney=0
    clothmoney=0
    @classmethod
    def update(cls,type,price,number):
        cls.toal+=price*number
        if type=='衣服':
            cls.clothmoney+=price*number
        if type=='食品':
            cls.foodmoney+=price*number

class Sale:
    def __init__(self,name,type,price,number):
        self.name=name
        self.type=type
        self.price=price
        self.number=number
        Money.update(self.type,self.price,self.number)

'''
例2：球员投篮训练，统计在2分钟内的训练成绩
    球员类：包含属性姓名、历史投篮命中率，投篮次数，命中数；以及投篮方法
每次投篮后随机调整1-3秒
命中率模拟： 比如命中率为90%，可以声明一个列表，列表中包含10个元素，9个为'命中'，1个为'未命中'，每次投篮随机从列表中选择一个元素即可
'''
#hgj
class Player:
    def __init__(self,name,hisrate,frequece,rate,meth):
        self.name=name
        self.hisrate=hisrate
        self.frequece=frequece
        self.rate=rate
        self.meth=meth
    def rate(self):
        a=self.rate*100
        b=100-a
        ratelist=[]
        for i in range(int(a)):
            ratelist.append('命中')
        for i in range(int(b)):
            ratelist.append('未命中')
        return  ratelist
    def scores(self, score):
        time1=time.time()
        c = Player.rate(self)
        while True:
            time2=time.time()
            s = random.randint(1,3)
            time.sleep(s)
            i=random.choice(c)
            if i=='命中':
                score+=1
            elif i=='未命中':
                score=score
            print(f'{self.name}的分数是{score:4}')
            if time2-time1>120:
                return score
                break
# def func(play,playerinfo):
#     play






if __name__=='__main__':
    s1=Sale('大大','食品',12,12)
    print(Money.foodmoney,Money.clothmoney,Money.toal)
    # p1=Player('哈登',0.99,20,0.91,123)
    # print(p1.scores(0))
