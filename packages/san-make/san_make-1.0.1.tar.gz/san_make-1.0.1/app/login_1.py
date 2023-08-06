def sort(list):
    n=len(list)
    for i in range(n-1):
        for j in range(i+1,n):
            if list[i]>list[j]:
                list[i],list[j]=list[j],list[i]
    return list


def sum(n):
    t=0
    l=[]
    for i in range(1,n+1):
        for j in range(1,i+1):
            t=t+j
    return t



if __name__ == '__main__':
    l=[2,3,6,7,10,11,1,1]
    l.reverse()
    print(l)
    reversed(l)
    l.sort(reverse=False)
    print(l)
    l.reverse()
    print(l)
    n=sum(10)
    print(n)
    # l=sort(l)
    # print(l)


