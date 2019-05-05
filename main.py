# -*- coding: utf-8 -*-
"""
Created on Wed May  1 00:33:34 2019

@author: yassi
"""

import numpy as np
import time
from lib.game import Status
from lib.game import update

def test_base():

    s = Status()

    request = {"player":"どっちのプレイヤーか","x":"選択したx座標", "y":"選択肢したy座標", "power":"成るかどうか","own":"持ち駒ならどれを打つか"}

    actions = [
        {"player":0,"x1":2,"y1":6,"x2":3,"y2":6}, #角道空ける
        {"player":1,"x1":6,"y1":2,"x2":5,"y2":2}, #角道空ける
        {"player":0,"x1":2,"y1":5,"x2":3,"y2":5}, #角道閉じる
        {"player":1,"x1":5,"y1":2,"x2":4,"y2":2}, #石田流
        {"player":0,"x1":0,"y1":4,"x2":1,"y2":5}, #玉上がり
        {"player":1,"x1":7,"y1":7,"x2":7,"y2":2}, #飛車回り
        {"player":0,"x1":1,"y1":5,"x2":1,"y2":6}, #玉寄り
        {"player":1,"x1":8,"y1":4,"x2":7,"y2":5}, #玉上がり
        {"player":0,"x1":0,"y1":3,"x2":1,"y2":4}, #金上がり（はや囲い）
        {"player":1,"x1":8,"y1":6,"x2":7,"y2":6}, #銀上がり
        {"player":0,"x1":1,"y1":7,"x2":2,"y2":6}, #角上がり（持久戦）
        {"player":1,"x1":7,"y1":5,"x2":8,"y2":6}, #玉引き（片美濃）
    ]

    start = time.time()
    for action in actions:

        request = {"player":action["player"], "x":action["x1"], "y":action["y1"], "power":False, "own":None}
        update(s, request)
        request = {"player":action["player"], "x":action["x2"], "y":action["y2"], "power":False, "own":None}
        update(s, request)
        #s.show()  
    end = time.time()

    print("{0} [s]".format(end-start))

def test_kill():

    s = Status()

    request = {"player":"どっちのプレイヤーか","x":"選択したx座標", "y":"選択肢したy座標", "power":"成るかどうか","own":"持ち駒ならどれを打つか"}

    actions = [

        {"player":0,"x":2,"y":4,"power":False,"own":None},
        {"player":0,"x":3,"y":4,"power":False,"own":None},

        {"player":1,"x":8,"y":3,"power":False,"own":None},
        {"player":1,"x":7,"y":2,"power":False,"own":None},

        {"player":0,"x":3,"y":4,"power":False,"own":None},
        {"player":0,"x":4,"y":4,"power":False,"own":None},

        {"player":1,"x":8,"y":5,"power":False,"own":None},
        {"player":1,"x":7,"y":6,"power":False,"own":None},

        {"player":0,"x":4,"y":4,"power":False,"own":None},
        {"player":0,"x":5,"y":4,"power":False,"own":None},

        {"player":1,"x":6,"y":0,"power":False,"own":None},
        {"player":1,"x":5,"y":0,"power":False,"own":None},

        {"player":0,"x":1,"y":1,"power":False,"own":None},
        {"player":0,"x":1,"y":4,"power":False,"own":None},

        {"player":1,"x":5,"y":0,"power":False,"own":None},
        {"player":1,"x":4,"y":0,"power":False,"own":None},

        {"player":0,"x":5,"y":4,"power":False,"own":None},
        {"player":0,"x":6,"y":4,"power":False,"own":None},
        {"player":0,"x":None,"y":None,"power":True,"own":None},

        {"player":1,"x":4,"y":0,"power":False,"own":None},
        {"player":1,"x":3,"y":0,"power":False,"own":None},

        {"player":0,"x":6,"y":4,"power":False,"own":None},
        {"player":0,"x":7,"y":4,"power":False,"own":None},

    ]

    start = time.time()
    for action in actions:
        update(s, action)
    end = time.time()

    print("{0} [s]".format(end-start))    
    s.show()
    print(s.get())

if __name__ == "__main__":
    
    test_kill()














