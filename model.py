import random

game_field = ['1','2','3','4','5','6','7','8','9']
player_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
enemy_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
mark = 'X'
win = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),
            (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
name = ''
game = False

async def get_game():
    global game
    return game

async def set_game():
    global game
    global name
    if game == False:
        game = True
    else:
        name = ''
        game = False

async def getMark() -> str:
    global mark
    return mark

async def changeMark():
    global mark
    if mark == 'O':
        mark = 'X'
    else:
        mark = 'O'

async def getName():
    global name
    return name

async def setName(new_name: str):
    global name
    name = new_name

async def getField():
    global game_field
    return game_field

async def setField():
    global game_field
    return game_field

async def setPlayerMove(move:int):
    global player_field
    player_field[move-1] = 1

async def setEnemyMove(move:int):
    global enemy_field
    enemy_field[move] = 1

async def getPlayerField():
    global player_field
    return player_field

async def getEnemyField():
    global enemy_field
    return enemy_field

async def win_condition(field: list):
    global win
    for move in win:
        if field[move[0]] == field[move[1]] == field[move[2]] == 1:
            return True