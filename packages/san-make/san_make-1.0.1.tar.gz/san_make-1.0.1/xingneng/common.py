def get_data(li):
    li.sort()
    n=0
    for i in li:
        n+=i
    return n/len(li),li[-1],li[0]


def get_res(res):
    head = str(res.headers)
    response = res.text
    x=len(head + response)

    return x