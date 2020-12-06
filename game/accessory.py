from flask import Blueprint, jsonify, request, redirect, session
from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)

#bp = Blueprint("mul", __name__, url_prefix="/")

player = client.diyiban.player
treasure = client.diyiban.treasure

#def getindex1(username,index):
    #temp = player.find_one({"name": username})
    #try:
        #return jsonify({"result":temp[index]})
    #except KeyError:
        #return jsonify({"result":None})

'''
def getindex2(name,index):
    temp = treasure.find_one({"name": name})
    try:
        return jsonify({"result":temp[index]})
    except KeyError:
        return jsonify({"result":None})
'''

'''
def get_norm(username,lower, upper, sigma=0.7):
    import scipy.stats as stats
    x=lower-1
    while not((x>lower) & (x<upper)):#由于正态分布其实是朝着无穷延伸的 所以难免有越界的地方 去了就是
        #上面不加括号你试试
        temp = getindex1(username, "tool")
        mu = getindex2(temp, "luck")
        X = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        N = stats.norm(loc=mu, scale=sigma)
        x=N.rvs(1)[0]
    return(round(x))
'''

def random_pick(some_list,probabilities):
    x = random.uniform(0,1)
    cumulative_probability=0.0
    for item,item_probability in zip(some_list, probabilities):
        cumulative_probability+=item_probability
        if x < cumulative_probability:
            break
    return item
