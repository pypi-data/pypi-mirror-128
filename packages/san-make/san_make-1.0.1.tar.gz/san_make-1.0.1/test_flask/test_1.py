from flask import Flask,jsonify,request,render_template,make_response
from homework.con_db import Con_DB
a=Flask(__name__)
@a.route('/st1',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return jsonify({'code':'1003','jieguo':'filed'})
    else:
        name=request.form.get('name')
        passwd=request.values.get('passwd')
        if name == 'admin' and passwd == '123456':
            res=make_response(jsonify({'code':'10001','jieguo':'success'}))
            res.set_cookie('username',name,max_age=60)
            return res
        else:
            return jsonify({'code':'1001','jieguo':'filed'})
@a.route('/st',methods=['GET'])
def index1():
    return render_template('login.html')
if __name__ == '__main__':
    a.run(host='0.0.0.0',port=4321,debug=True)