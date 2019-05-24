import numpy as np

NONE = -1
OU = 0
KIN = 1
GIN = 2
HISHA = 3
KAKU = 4
KEI = 5
KYO = 6
HU = 7
GROUP = 8
POWER = 16

def Group(piece):
    """
    返り値は0,1(player0,1) or -1(空ます)
    """
    
    return -1 if piece==NONE else piece%POWER//GROUP

def Kind(piece):
    """
    返り値は0~7(駒の種類) or -1(空ます)
    """
    
    return -1 if piece==NONE else piece%8

def Power(piece):
    """
    返り値は0,1（不成,成）
    """
    
    return -1 if piece==NONE else piece//POWER

def Turn(phase):
    """
    返り値は0,1(player0,1)
    """

    return int(phase//3)

# 盤上の駒を動かす場合
def Move(piece, x1, y1, x2, y2):
    """
    X1,y1は移動前の座標
    x2,y2は移動先の座標
    """

    if x1==x2 and y1==y2:
        return False
    
    kind = Kind(piece)
    group = Group(piece)
    sign = np.sign(0.5-group) # player0なら正(+1), player1なら負(-1)

    if Power(piece):

        # 竜
        if kind==HISHA:
            return max( abs(x2-x1), abs(y2-y1) ) == 1 or x1==x2 or y1==y2
        # 馬
        elif kind==KAKU:
            return max( abs(x2-x1), abs(y2-y1) ) == 1 or x1-y1==x2-y2 or x1+y1==x2+y2
        # 成金
        else:
            return abs(y1-y2)+abs(x1-x2)==1 or abs(y2-y1)*(x2-x1)*sign == 1
    
    else:
        
        # 周囲1マス
        if kind==OU:
            return max( abs(x2-x1), abs(y2-y1) ) == 1
        
        # 縦横1歩 or 前斜め
        elif kind==KIN:
            return abs(y1-y2)+abs(x1-x2)==1 or abs(y2-y1)*(x2-x1)*sign == 1 
        
        # 4角 or 前1歩
        elif kind==GIN:
            return abs( (y2-y1)*(x2-x1) ) == 1 or (y1==y2 and (x2-x1)*sign == 1)
        
        # 同じ縦横線上
        elif kind==HISHA:
            return x1==x2 or y1==y2
        
        # 同じ斜め線上
        elif kind==KAKU:
            return x1-y1==x2-y2 or x1+y1==x2+y2
        
        elif kind==KEI:
            return abs(y1-y2)==1 and (x2-x1)*sign == 2

        # 同じy列 かつ 前進
        elif kind==KYO:
            return y1==y2 and (x2-x1)*sign > 0 
        
        # 同じy列 かつ 前進1マス
        elif kind==HU:
            return y1==y2 and (x2-x1)*sign == 1

def Through(field, x1, y1, x2, y2):

    # 横
    if x1 == x2:
        ymin,ymax = sorted([y1,y2])
        return sum([ Group(field[x1][y]) for y in range(ymin+1,ymax) ]) == -(ymax-ymin-1)
    # 横
    elif y1 == y2:
        xmin,xmax = sorted([x1,x2])
        return sum([ Group(field[x][y1]) for x in range(xmin+1,xmax) ]) == -(xmax-xmin-1)
    # 右斜め降り
    elif x1-y1==x2-y2:
        pmin, pmax = sorted([(x1,y1),(x2,y2)])
        return sum([ Group(field[ pmin[0]+i ][ pmin[1]+i ]) for i in range(1,pmax[0]-pmin[0]) ]) == -(pmax[0]-pmin[0]-1)
    elif x1+y1==x2+y2:
        pmin, pmax = sorted([(x1,y1),(x2,y2)])
        return sum([ Group(field[ pmin[0]+i ][ pmin[1]-i ]) for i in range(1,pmax[0]-pmin[0]) ]) == -(pmax[0]-pmin[0]-1)
    return True

def Harden(piece, x, y):

    kind = Kind(piece)
    group = Group(piece)

    if not Power(piece):

        if kind == KYO and x==(8-group*8):
            return True
        elif kind == HU and x==(8-group*8):
            return True
        elif kind == KEI and x in (8-group*8,7-group*6):
            return True

    return False

def Double(piece, field, x, y):

    if Kind(piece)==HU and not Power(piece):
        return bool(np.sum(field.T[y] == piece))
    return False

def Aim(field, ox, oy):
    """
    ox,oyに敵の駒の利きがあるか
    返り値は9×9のbool値ndarray
    """
    
    def minimumAim(enemy_position):

        ex = enemy_position//10
        ey = enemy_position%10

        # 空マス or 自陣の駒ならFalse
        if Group(field[ex][ey]) in ( -1, Group(field[ox][oy]) ):
            return False

        return Move(field[ex][ey], ex, ey, ox, oy) and Through(field, ex, ey, ox, oy)

    # フィールド上の敵の駒をチェック
    enemies = np.array([ 10*x + y for x in range(9) for y in range(9)])

    # ユニバーサル関数化
    f = np.frompyfunc(minimumAim, 1, 1)

    # 王手判定
    result = f(enemies)

    return result