import pytest
from pymongo import MongoClient
from flask import Flask,jsonify
from flask.testing import FlaskClient

import os
import json
import sys
sys.path.append('c:/Users/nicole/PycharmProjects/dierban/')
from runserver import bp

clientmg = MongoClient('localhost', 27017)
player = clientmg.diyiban.player
treasure = clientmg.diyiban.treasure
session = clientmg.diyiban.session
#market.create_index([("goods", ASCENDING)], unique=True)#不能以商品建立索引 因为会有商品重复
#commands = ["add", "sub", "mul", "div", "no"]
# session={}#"wotm pytest is too hard to use in pytest when flask use session"

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(bp)

# username = 'Joe'
# data_changejewelry = json.dumps({"jewelry":"bracelet"})
# data_sell = json.dumps({"item":"dagger", "task":1, "price":80})
# data_login = json.dumps({"username":"Joe","password":"123456"})
# data_changetool = json.dumps({"tool":"basketball"})
# data_market = json.dumps({"item":"bag"})

username = 'Joe'
data_changejewelry = json.dumps({"jewelry": "bracelet"})
data_sell = json.dumps({"item": "dagger", "task": 1, "price": 80})
data_login = json.dumps({"username": "Joe", "password": "123456"})
data_changetool = json.dumps({"tool": "basketball"})
data_market = json.dumps({"item": "bag"})

def test_register_get(client: FlaskClient):
    response = client.get('/register')
    print(response)
    assert response.status_code == 200

def test_home_get(client: FlaskClient):
    response = client.get("/%s/home" % (username))
    print(response)
    json = response.get_json()
    assert json["ok"]==1


def test_sell_get(client: FlaskClient):
    response = client.get("/%s/sell" % (username))
    json = response.get_json()
    print(json)
    assert response.status_code == 200


def test_market_get(client: FlaskClient):
    response = client.get("/%s/market" % (username))
    json = response.get_json()
    print(json)
    assert json["ok"] == 1

def test_changetool_get(client: FlaskClient):
    response = client.get("/%s/changetool" % (username))
    print(response)
    json = response.get_json()
    print(json)
    assert response.status_code == 200

def test_changejewelry_get(client: FlaskClient):
    response = client.get("/%s/changejewelry" % (username))
    print(response)
    json = response.get_json()
    print(json)
    assert response.status_code == 200

def test_find_get(client: FlaskClient):
    response = client.get("/%s/find" % (username))
    json = response.get_json()
    print(json)
    assert json["ok"]==1

def test_work_get(client: FlaskClient):
    response = client.get("/%s/work" % (username))
    json = response.get_json()
    print(json)
    assert json["ok"]==1

'''
@pytest.mark.parametrize(('username','message'),(
        [('Joe','0'),
        ('Kate','0')]
))
def test_work(client: FlaskClient, username, message):
        #print(session.find_one({'username':username})["session"])
        #client.set_cookie('localhost', 'session', player.find_one({'username':username})['session'])
        response = client.get('/{0}/work'.format(username))
        print(response)
        # print(response.get_json())
        # print(response.data)
        # print(response.get_cookies())
        json = response.get_json()
        print(json)
        assert json["ok"] == message
        
    @pytest.mark.parametrize(('username', 'message'), (
            [('mk', 1),
             ('mk2', 0)]
    ))
    def test_travel(username, message):
        aclient = client
        print(session.find_one({'username': username})["session"])
        aclient.set_cookie('localhost', 'session', player.find_one({'username': username})['session'])
        response = aclient.get('/{0}/work'.format(username))
        json = response.get_json()
        assert json["ok"] == message
'''


def test_sell_post(client: FlaskClient):
    global data_sell
    response = client.post("/%s/sell" % (username), data=data_sell, content_type='application/json')
    print(response)
    json = response.get_json()
    print(json)
    assert json["ok"] == 1


def test_login_post(client: FlaskClient):
    global data_login
    response = client.post("/", data=data_login, content_type='application/json')
    assert response.status_code == 302


def test_changetool_post(client: FlaskClient):
    global data_changetool
    response = client.post('/%s/changetool' % (username), data=data_changetool, content_type='application/json')
    print(response)
    json = response.get_json()
    print(json)
    assert json["ok"] == 1



def test_changejewelry_post(client: FlaskClient):
    global data_changejewelry
    response = client.post('/%s/changejewelry'%(username), data=data_changejewelry, content_type='application/json')
    print(response)
    json = response.get_json()
    print(json)
    assert json["ok"] == 1


def test_market_post(client: FlaskClient):
    global data_market
    response = client.post('/%s/market' % (username), data=data_market, content_type='application/json')
    print(response)
    json = response.get_json()
    print(json)
    assert json["ok"] == 1

