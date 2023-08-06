import random
class Play:
    def __init__(self,name,turn,time):
        self.name=name
        self.turn=turn
        self.time=time
    # def score(self,out,bout,score):
    #     if out==bout:
    #         score=score
    #     if (out=='石头' and bout=='剪刀') and (out=='剪刀' and bout=='布') and (out=='布' and bout=='石头'):
    #         score+=1
    #     if (out=='石头' and bout=='布') and (out=='剪刀' and bout=='石头') and (out=='布' and bout=='剪刀'):
    #         score-=1
    #     return score
    def scores(self,out,bout):
        # for i in range(turn):
        #     for n in range(time):
        n=0
        if out == bout:
            n=0
            return n
        if (out=='石头' and bout=='剪刀') or (out=='剪刀' and bout=='布') or (out=='布' and bout=='石头'):
            n=1
            return n
        if (out=='石头' and bout=='布') or (out=='剪刀' and bout=='石头') or (out=='布' and bout=='剪刀'):
            n=-1
            return n
class Robet:
    def __init__(self,name):
        self.name=name

    def output(self):
        str=['石头','剪刀','布']
        i=random.choice(str)
        return i


if __name__=='__main__':

    ro1=Robet('ro1')
    zz=Play('zz',3,5)
    score=0
    for i in range(3):
        for n in range(5):
            you=input('请输入')
            ro = ro1.output()
            score=score+zz.scores(you,ro)
            print(score,ro)




