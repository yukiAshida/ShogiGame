# -*- coding: utf-8 -*-
"""
Created on Wed May  1 00:33:34 2019

@author: yassi
"""

import numpy as np
import sys
import time
from .utils import NONE,OU,KIN,GIN,HISHA,KAKU,KEI,KYO,HU
from .utils import GROUP,POWER
from .utils import Group,Kind,Power,Turn,Move,Through,Aim,Harden,Double

class Status():
    
    def __init__(self):
        
        # 盤
        self.field = np.ones((9,9))*NONE
        self.setInitialPosition()
        
        # 持ち駒
        self.own = np.zeros(16)
        
        # 状態
        self.phase = 0
        self.select_pos = {"x":None,"y":None,"own":None}  #{"x":???, "y":???}
        self.select_piece = None
        self.king = [[0,4],[8,4]] #玉の位置
        self.end = False
        
    def setInitialPosition(self):
        
        #歩の配置(2 or 6行目)
        for i in (0,1):
            self.field[2+i*4] = HU + i*GROUP
        
        #王金銀桂香の配置(0 or 8行目)
        for i in (0,1):
            self.field[8*i] = np.array([KYO,KEI,GIN,KIN,OU,KIN,GIN,KEI,KYO]) + i*GROUP
        
        #飛車角の配置(1 or 7行目)
        for i in (0,1):
            self.field[1+6*i][1+6*i] = HISHA + i*GROUP
            self.field[1+6*i][7-6*i] = KAKU + i*GROUP
        
    def show(self):
        
        labels = {NONE:" ",HU:"f",OU:"o",HISHA:"h",KAKU:"k",KIN:"g",GIN:"s",KEI:"h",KYO:"p"}
        
        output=""
        
        for col in self.field:
            output+="|"
            
            for piece in col:
                kind = NONE if piece == NONE else int(piece%17%8)
                output+=labels[kind]+"|"
            output+="\n"
        output+="\n"

        print(output)
        
        time.sleep(0.4)
    
    def get(self):

        text = "=====================\n"
        text += "phase: {0}\n".format(self.phase)
        text += "select_pos: {0}\n".format(self.select_pos)
        text += "select_piece: {0}\n".format(self.select_piece)
        text += "king: {0}\n".format(self.king)
        text += "own: {0}\n".format(self.own)
        text += "end: {0}\n".format(self.end)
        text += "=====================\n\n"

        return text
        


"""
本実装中は，array[x][y]で統一
"""

def onSelect(status, select):
    """
    phase0,3において，どの駒を動かすかの選択に対するコールバック関数
    盤上の駒を選択した場合は，select = {"x":xi, "y":yi} (0<=xi,yi<=8)
    持ち駒を選択した場合は，select = z (0 <= z <= 15)
    """

    # 持ち駒を選択 かつ 選択駒が自分のもの
    if select["own"]!=None and Group(select["own"]) == Turn(status.phase):
                
        status.select_piece = select["own"]
        status.select_pos = select
        status.phase += 1
        return

    # 盤上の駒を選択 かつ 選択駒が自分の物
    if Group(status.field[select["x"]][select["y"]]) == Turn(status.phase):
        
        status.select_piece = status.field[select["x"]][select["y"]]
        status.select_pos = select
        status.phase += 1
        return

    return

def ableMove(status, select):
    """
    動かすと選択した駒を指定箇所に動かせるかどうか
    x,yは移動先の座標
    """

    # 持ち駒だとx1,y1=Noneになる...
    x1 = status.select_pos["x"]
    y1 = status.select_pos["y"]
    x2 = select["x"]
    y2 = select["y"]

    # 盤上の駒を選択した場合
    if x1 != None:
        
        # x,yは移動可能か？（駒の能力的に）
        b1 = Move(status.select_piece, x1, y1, x2, y2 )
        
        # x,yに自分の駒が存在しないか
        b2 = Group(status.field[x2][y2]) != Group(status.select_piece)

        # x,yとstatus.select_pos間に駒が存在しないか
        b3 = Through(status.field, x1, y1, x2, y2)

        # 仮想的に動かしてみる
        field_copy = status.field.copy()
        field_copy[x1][y1] = NONE
        field_copy[x2][y2] = status.select_piece

        # 移動の結果，自玉に王手がかからないか
        if Kind(status.select_piece)==OU:
            ox, oy = (x2,y2) 
        else:
            ox, oy = status.king[Turn(status.phase)]

        b4 = not bool(Aim(field_copy, ox, oy).sum())

        return b1*b2*b3*b4
    
    # 持ち駒を選択した場合
    else:
        
        # その場所に駒が無いか
        b1 = Group(status.field[x2][y2]) == NONE

        # 動かせない場所に打ってないか
        b2 = not Harden(status.select_piece, x2, y2)

        # 2歩じゃないか
        b3 = not Double(status.select_piece, status.field, x2, y2)

        return b1*b2*b3

def onMove(status, select):
    """
    select={"x":x, "y":y} は移動先のマス
    """

    # 持ち駒だとx1,y1=Noneになる...
    piece = status.select_piece
    x1 = status.select_pos["x"]
    y1 = status.select_pos["y"]
    x2 = select["x"]
    y2 = select["y"]
    
    if ableMove(status, select):
        
        # 玉を動かしたら位置を変更
        if Kind(piece) == OU:
            status.king[Turn(status.phase)] = [x2,y2]
        
        # 持ち駒の場合は持ち駒を減らす
        if x1 == None:
            status.own[piece]-=1
        else:
            status.field[x1][y1] = NONE

        # 駒を取った場合は持ち駒に移動
        if status.field[x2][y2] != NONE:
            status.own[int(Turn(status.phase)*8 + Kind(status.field[x2][y2]))] += 1

        
        # 成り判定(動かせない場合は強制成)
        if Harden(piece, x2, y2):
            status.phase = (status.phase+2)%6
            status.select_pos = {"x":None,"y":None,"own":None}
            status.field[x2][y2] = piece+POWER        
        elif ablePower(status, select):
            status.phase += 1
            status.select_pos = {"x":x2,"y":y2,"own":None}
            status.field[x2][y2] = piece
        else:
            
            status.phase = (status.phase+2)%6
            status.select_pos = {"x":None,"y":None,"own":None}
            status.field[x2][y2] = piece
        
        status.select_piece = None

    else:
        status.select_pos = {"x":None,"y":None,"own":None}
        status.select_piece = None
        status.phase -= 1

def ablePower(status, select):
    """
    x1：動かす前のマス
    x2：移動先のマス
    """
    piece = status.select_piece
    x1 = status.select_pos["x"]
    x2 = select["x"]
    
    # 持ち駒の場合は成不可
    if x1 == None:
        return False

    # 既に成っている場合は成不可
    if Power(piece):
        return False

    # どちらのターンか
    which = Turn(status.phase)

    # 先手なら大きい方のxを取る，後手なら小さい方のxを取る
    x = sorted([x1,x2])[1-which]
    
    # 先手ならxが6以上なら，後手ならxが2以下なら
    return (1-which*2)*(x-6+4*which)>=0

def onPower(status, select):
    """
    pはなるかどうか（bool値）
    """
    
    if select["power"]:
        
        x = status.select_pos["x"]
        y = status.select_pos["y"]
        status.field[x][y] += POWER

    status.select_pos = {"x":None,"y":None,"own":None}
    status.phase = (status.phase +1)%6

def update(status, request):

    if Turn(status.phase)==request["player"]:

        if status.phase%3 == 0:
            onSelect(status, { "x":request["x"], "y":request["y"], "own":request["own"] } )
        
        elif status.phase%3 == 1:
            onMove(status, { "x":request["x"], "y":request["y"], "own":None } )
        
        elif status.phase%3 == 2:
            onPower(status, { "power": request["power"]} )

        #終了判定
        if status.phase%3 == 0 and end(status):
            status.end = True

def end(status):

    debug = {}

    # これから動かそうとする方
    which = Turn(status.phase)
    ox,oy = status.king[which]
    
    debug["king"] = "{0}の王は({1},{2})にいる".format(which,ox,oy)

    # 王手を判定
    aim = Aim(status.field, ox, oy)
    s = np.sum(aim)
    
    # 攻撃箇所
    attack_pos = [ (a//9, a%9) for a in np.where(aim)[0] ]

    debug["aim"] = "{0}から狙われています".format("と".join([ "("+str(x)+","+str(y)+")" for x,y in attack_pos ]))

    print(debug)

    # 王手がかかっていない
    if s==0:
        print("王手はかかっていません") 
        return False

    ## 玉を動かす
    for dx in range(-1,2):
        for dy in range(-1,2):
            
            # 盤外には移動できない（移動しないのもだめ）
            if (dx==0 and dy==0) or (ox+dx<0 or 8<ox+dx) or (oy+dy<0 or 8<oy+dy):
                continue

            # 移動先に自陣の駒がいる場合は動かせない
            if Group(status.field[ox+dx][oy+dy]) == which:
                continue

            # 仮想的に動かしてみる
            field_copy = status.field.copy()
            field_copy[ox][oy] = NONE
            field_copy[ox+dx][oy+dy] = OU + which*GROUP

            # 移動の結果，自玉に王手がかからないか
            if not bool(Aim(field_copy, ox+dx, oy+dy).sum()):
                print("({0},{1})に逃げられます".format(ox+dx,oy+dy))
                return False
        
    # 王手が1箇所から発生している場合は合い駒か王手の駒を取るのもあり（2箇所以上の場合は玉を動かすしかない）
    if s==1:

        # 攻撃箇所
        ax,ay = attack_pos[0]
    
        # 王手駒を取る(ただし，同玉は上で調査済みであるため除外)
        kill = Aim(status.field, ax, ay)
        kill[9*ox+oy] = False

        
        kill_pos = [ (a//9, a%9) for a in np.where(kill)[0] ]

        for kx,ky in kill_pos:
            
            field_copy = status.field.copy()
            field_copy[kx][ky] = NONE
            field_copy[ax][ay] = field_copy[kx][ky]

            if not bool(Aim(field_copy, ox, oy).sum()):

                print("取れます")
                return False

        # 合い駒     
        if max(abs(ax-ox),abs(ay-oy))>=2 and defense(status, ax,ay, ox, oy):
            print("間駒できます")
            return False

    print("詰み")
    return True

# 攻撃駒(ax,ay)=>王(ox,oy)の合い駒可能性を検証（ただし，両者が隣接していないことを前提）
def defense(status,ax,ay,ox,oy):

    which = Turn(status.phase)

    # 可能性のある駒は, 飛車(竜)・角(馬)・香・桂
    attacker = status.field[ax][ay]
    
    # 桂馬は合い駒不可
    if Kind(attacker) == KEI:
        return False

    elif Kind(attacker) == HISHA:
        
        # 同x列
        if ax == ox:
            
            sy = min(ay,oy)

            for i in range(1,abs(ay-oy)):
                
                # 盤上の駒による合い駒
                if bool(Aim(status.field, ax, sy+i).sum()):
                    return True

                # 持ち駒による合い駒
                for oi in range(8*which, 9+8*which):
                    if status.own[oi]>0 and not Harden(oi, ax, sy+i):
                        return True
        
        # 同y列
        else:
            sx = min(ax,ox)

            for i in range(1,abs(ax-ox)):

                # 盤上の駒による合い駒
                if bool(Aim(status.field, sx+i, ay).sum()):
                    return True
                
                # 持ち駒による合い駒
                for oi in range(8*which, 9+8*which):
                    if status.own[oi]>0 and not Harden(oi, sx+i, ay):
                        return True
        

    elif Kind(attacker) == KAKU:
        
        sx,sy = (ax,ay) if ax<ox else (ox,oy)

        # 右斜め降り
        if ax-ay == ox-oy:
            
            for i in range(1,abs(ax-ox)):

                # 盤上の駒による合い駒                       
                if bool(Aim(status.field, sx+i, sy+i).sum()):
                    return True
                
                # 持ち駒による合い駒
                for oi in range(8*which, 9+8*which):
                    if status.own[oi]>0 and not Harden(oi, sx+i, sy+i):
                        return True

        # 左斜め降り
        else:

            for i in range(1,abs(ax-ox)):

                # 盤上の駒による合い駒                       
                if bool(Aim(status.field, sx+i, sy-i).sum()):
                    return True
                
                # 持ち駒による合い駒
                for oi in range(8*which, 9+8*which):
                    if status.own[oi]>0 and not Harden(oi, sx+i, sy-i):
                        return True
        
    elif Kind(attacker) == KYO:

        sx = (ox if which==0 else ax)

        for i in range(1,abs(ox-ax)):
            
            # 盤上の駒による合い駒
            if bool(Aim(status.field, sx+i, ay).sum()):
                return True
            
            # 持ち駒による合い駒
            for oi in range(8*which, 9+8*which):
                if status.own[oi]>0 and not Harden(oi, sx+i, ay):
                    return True

    return False


def possible(status):

    if status.phase%3 == 0:
        
        # どちらのターンか

        # 動かせる駒は？

        # 打てる持ち駒は？

        return np.zeros(89)

    elif status.phase%3 == 1:
        
        # どちらのターンか

        # どこに動かせるか（置けるか）

        return np.zeros(81)
        
    elif status.phase%3 == 2:
        
        # 成るか成らないか

        return np.zeros(2)
        














