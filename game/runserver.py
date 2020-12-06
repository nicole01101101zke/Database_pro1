# -*- coding: utf-8 -*
import threading

from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
#from flask_apscheduler import APScheduler
import connect
import accessory
import time
import json
import os
import sys
sys.path.append('../templates/')

app = Flask(__name__)
#scheduler = APScheduler()
#app.secret_key = 'zke'
#app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7+\xe6px@\xc3#\\'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


bp = Blueprint("mul", __name__, url_prefix="/")
mongo = connect.Mongo()
db = mongo.connect()
myplayer = db["player"]
mytreasure = db["treasure"]
mysession = db["session"]
#username = 'test'
list1 = ["magicbook", "computer", "shovel", "dagger", "sword", "necklace", "basketball", "earrings", "bracelet", "bag"]



work_flag=1
find_flag=1
def oneday():
    global work_flag,find_flag
    while True:
        time.sleep(300)
        work_flag = 1
        find_flag = 1

timer=threading.Timer(0,oneday)
timer.start()

@bp.route('/', methods=['POST', 'GET'])
def login():
    # upload_file = request.files.get('file')
    # print(upload_file)
    if request.method == "GET":
        return render_template("login.html")
    else:
        a = request.get_data()
        dict1 = json.loads(a)
        session["username"] = dict1["username"]
        session["password"] = dict1["password"]

        if mysession.find_one({"username":session["username"]}) != None:
            mysession.delete_one({"username":session["username"]})
        mysession.insert_one({"username":session["username"],"session":request.cookies["session"]})

        temp = myplayer.find_one({"name":session["username"]})
        if temp == None:
            return redirect('/register')
        elif temp["password"] == session["password"]:
            return redirect("/" + session["username"] + "/home")
        else:
            return redirect("/")

        #yonghu = myplayer.find_one({"name":request.form["username"]})
        #session["username"] = request.form["username"]
        #if yonghu.get("password") == request.form["password"]:
            #return redirect("/home")
        #else:
            #flash(u"incorrect password")
            #return render_template("login.html")

@bp.route('/<string:username>/home', methods=['GET', 'POST'])
def home(username):
    #a = request.get_data()
    #dict1 = json.loads(a)
    #session["username"] = dict1["username"]
    #if session["username"] == username:
        temp3 = myplayer.find_one({"name": username})
        temp3.pop("_id")
        temp3.pop("password")
        temp3.update({"ok":1})

        return jsonify(temp3)
    #else:
        #return redirect('/')

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("/register.html")
    else:
        #username = request.form["username"]
        #password = request.form["password"]
        a = request.get_data()
        dict1 = json.loads(a)
        username = dict1["username"]
        password = dict1["password"]
        dict = {"name":username, "password":password, "money":500, "tool":None, "jewelry":None, "treasure":["bag","bracelet","basketball"]}
        myplayer.insert_one(dict)

        temp = myplayer.find_one({"name":username})
        temp.update({"ok":1})
        temp.pop("_id")
        temp.pop("password")

        return jsonify(temp)



@bp.route("/<string:username>/work", methods=['GET'])
def work(username):
        global work_flag

    #if "username" in session: #session["username"]==username:
        if (work_flag == 1):
            work_flag=0
            money = myplayer.find_one({"name":username})["money"]
            toolon = myplayer.find_one({"name":username})["tool"]
            workability = mytreasure.find_one({"name":toolon})["ability"]
            money= money + workability
            myplayer.update_one({"name": username}, {"$set":{"money": money}})

            temp = myplayer.find_one({"name":username})
            temp.pop("_id")
            temp.update({"ok":1})
            return jsonify(temp)
        else:
            return jsonify({"ok":0})
    #else:
        #return jsonify({"ok":0}) #redirect('/')

@bp.route("/<string:username>/find", methods=['GET'])
def find(username):
        global find_flag
        global list1
    #if "username" in session: #session["username"]==username:
        if (find_flag==1):
            find_flag=0
            jewelry = myplayer.find_one({"name":username})["jewelry"]
            luck = mytreasure.find_one({"name":jewelry})["luck"]
            list2 = [0.01, luck/100.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0, (0.99-luck/100.0)/8.0]
            get = accessory.random_pick(list1, list2)
            print(get)
            myplayer.update_one({"name":username}, {"$push":{"treasure":get}})

            temp1 = mytreasure.find_one({"name":get})
            ability_ = temp1["ability"]
            luck_ = temp1["luck"]
            price_ = temp1["price"]
            dict = {"name":get, "ability":ability_, "luck":luck_, "available":1, "onsale":0, "player":username, "price":price_}

            mytreasure.insert_one(dict)

            res = myplayer.find_one({"name": username})
            cnt = len(res["treasure"])
            print(cnt)
            if (cnt > 10):
                temp1 = mytreasure.find_one({"player": username, "available": 1}, sort=[("price", 1)])
                print(temp1)
                myplayer.update_one({"name": username}, {"$pull": {"treasure": temp1["name"]}})
                mytreasure.update_one({"player":username,"name": temp1["name"]}, {"$set": {"player": "root"}})

            temp = myplayer.find_one({"name":username})
            temp.pop("_id")
            temp.update({"ok":1})
            return jsonify(temp)
        else:
            return jsonify({"ok":0})
    #else:
        #return redirect('/')




@bp.route('/<string:username>/market', methods=['GET', 'POST'])
def market(username):
    #if session["username"] == username:
        if request.method == "GET":
            mdict = {}
            mtemp = mytreasure.find({"onsale":1})
            for x in mtemp:
                mdict.update({x["name"]:x["price"]})
            mdict.update({"ok":1})
            return jsonify(mdict)
        else:
            #buyer = request.form["buyer"]
            #item = request.form["item"]
            a = request.get_data()
            dict2 = json.loads(a)
            buyer = username #session["username"] #dict2["buyer"]
            item = dict2["item"]
            res = mytreasure.find_one({"name":item,"onsale":1})
            if(res == None):
                return jsonify({"ok":0})
            elif(res["player"] == username):
                return jsonify({"ok": 0})
            else:
                seller = res["player"]
                temp = res["price"]
                mytreasure.update_one({"name": item}, {"$set":{"player":buyer}})
                myplayer.update_one({"name":buyer}, {"$push":{"treasure":item}})
                myplayer.update_one({"name": buyer}, {"$inc": {"money": -temp}})  # 买家金钱减少
                if seller != "root":
                    myplayer.update_one({"name": seller}, {"$pull": {"treasure": item}})
                    myplayer.update_one({"name": seller}, {"$inc": {"money": temp}})  # 卖家金钱增加

                res = myplayer.find_one({"name": buyer})
                cnt = len(res["treasure"])
                print(cnt)
                if (cnt > 10):
                    temp1 = mytreasure.find_one({"player": buyer, "available": 1}, sort=[("price", 1)])
                    print(temp1)
                    myplayer.update_one({"name": buyer}, {"$pull": {"treasure": temp1["name"]}})
                    mytreasure.update_one({"player": buyer, "name": temp1["name"]}, {"$set": {"player": "root"}})

                temp = myplayer.find_one({"name": buyer})
                temp.pop("_id")
                temp.pop("password")
                temp.update({"ok": 1})

                return jsonify(temp)
    #else:
        #return redirect('/')

@bp.route('/<string:username>/changetool', methods=['POST','GET'])
def changetool(username):
    #if session["username"] == username:
        if request.method == "GET":
            temp = myplayer.find_one({"name": username})
            temp.pop("_id")
            temp.pop("password")
            temp.update({"ok": 1})
            return jsonify(temp)
        else:
            a = request.get_data()
            dict = json.loads(a)
            player = username #session["username"] # dict["player"]
            tool = dict["tool"]

            if mytreasure.find_one({"name":tool, "player":player}) == None:
                return jsonify({"ok":0})
            elif mytreasure.find_one({"name":tool, "player":player})["ability"] == 0:
                print("this is jewelry , cannot change")
                return jsonify({"ok": 0})
            elif myplayer.find_one({"name":player, "treasure":tool}) == None:
                return jsonify({"ok": 0})
            else:
                old = myplayer.find_one({"name": player})["tool"]
                myplayer.update_one({"name": player}, {"$pull": {"treasure": tool}})
                myplayer.update_one({"name": player},{"$set":{"tool":tool}})
                if old != None:
                    myplayer.update_one({"name": player}, {"$push": {"treasure": old}})
                    mytreasure.update_one({"name": old}, {"$set":{"available":1}})
                mytreasure.update_one({"name": tool}, {"$set": {"available": 0}, "$set":{"onsale":0}})

            temp1 = myplayer.find_one({"name": player})
            temp1.pop("_id")
            temp1.pop("password")
            temp1.update({"ok": 1})

            return jsonify(temp1)
    #else:
        #return redirect('/')

@bp.route('/<string:username>/changejewelry', methods=['POST','GET'])
def changejewelry(username):
    #if session["username"] == username:
        if request.method == "GET":
            temp = myplayer.find_one({"name": username})
            temp.pop("_id")
            temp.pop("password")
            temp.update({"ok":1})
            return jsonify(temp)
        else:
            a = request.get_data()
            dict = json.loads(a)
            player = username #session["username"] #dict["player"]
            jewelry = dict["jewelry"]

            if mytreasure.find_one({"name":jewelry, "player":player})["luck"] == 0:
                print("this is tool , cannot change")
                return jsonify({"ok": 0})
            elif myplayer.find_one({"name":player, "treasure":jewelry}) == None:
                return jsonify({"ok": 0})
            else :
                old = myplayer.find_one({"name": player})["jewelry"]
                myplayer.update_one({"name": player}, {"$pull": {"treasure": jewelry}})
                myplayer.update_one({"name": player},{"$set":{"jewelry":jewelry}})
                if old != None:
                    myplayer.update_one({"name": player}, {"$push": {"treasure": old}})
                    mytreasure.update_one({"name": old}, {"$set":{"available":1}})
                mytreasure.update_one({"name": jewelry}, {"$set": {"available": 0}, "$set":{"onsale":0}})

                temp1 = myplayer.find_one({"name": player})
                temp1.pop("_id")
                temp1.pop("password")
                temp1.update({"ok": 1})

                return jsonify(temp1)
    #else:
        #return redirect('/')

@bp.route('/<string:username>/sell', methods=['POST','GET'])
def sell(username):
    #if session["username"] == username:
        if request.method == "GET":
            temp = myplayer.find_one({"name": username})
            temp.pop("_id")
            temp.pop("password")
            temp.update({"ok": 1})
            return jsonify(temp)
        else:
            a = request.get_data()
            dict = json.loads(a)
            player = username #session["username"] #dict["player"]
            item = dict["item"]
            task = dict["task"]
            price = dict["price"]

            if task == 1: #挂牌宝物
                res1 = mytreasure.find_one({"name":item, "player":player, "available":1, "onsale":0}) #正在使用的宝物不能出售
                print(res1)
                if res1 != None:
                    mytreasure.update_one({"name":item, "player":player}, {"$set":{"onsale":1}})
                    mytreasure.update_one({"name": item, "player": player}, {"$set": {"price": price}})
                else:
                    return jsonify({"ok":0})
            else: #收回宝物
                res2 = mytreasure.find_one({"name":item, "player":player, "onsale":1})
                print(res2)
                if res2 != None:
                    mytreasure.update_one({"name":item, "player":player}, {"$set":{"onsale":0}})
                else:
                    return jsonify({"ok":0})
            dict = {}
            list = []
            temp1 = myplayer.find_one({"name": player})["treasure"]
            #print(temp1)
            for temp in temp1:
                list.append(mytreasure.find_one({"name":temp,"onsale":1}))
            #print(list)
            i=0
            for x in list:
                i = i + 1
                if x != None:
                    dict[x["name"]] = x["price"]
            #dict.update({"ok":1})
            dict.update({"ok": 1})
            return jsonify(dict)
    #else:
        #return redirect("/")




#if __name__ == '__main__':
    #scheduler.init_app(app=app)
    #scheduler.start()
    #app.register_blueprint(bp)
    #app.run(port=8081)