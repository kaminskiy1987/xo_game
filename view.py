'''
async def printField(update, game_field: list, name: str):
     await update.message.reply_text(f'{game_field[0]:^5}|{game_field[1]:^5}|{game_field[2]:^5}')
     await update.message.reply_text(f'-----------------')
     await update.message.reply_text(f'{game_field[3]:^5}|{game_field[4]:^5}|{game_field[5]:^5}')
     await update.message.reply_text(f'-----------------')
     await update.message.reply_text(f'{game_field[6]:^5}|{game_field[7]:^5}|{game_field[8]:^5}\n\n')
     await update.message.reply_text(f'=============================================')
     await update.message.reply_text(f'Ход {name}')
     
    
async def playerTurn(update, game_field: list, mark, name) -> int:
     while True:
         move = int(update.message.text)
         if (0 < move < 10) and game_field[move-1].isdigit():
             game_field[move-1] = mark
             return move
         else:
             update.message.reply_text('Эта клетка занята! Сделайте другой ход')


async def win(update, name:str):
    await update.message.reply_text(f'{name} выиграл!')
    #await update.message.text == '/new game'

async def start_game(update):
    await update.message.reply_text(f'Привет {update.effective_user.first_name}\n\
       Попробуй выйграть в крестики-нолики')

async def player_take(update, name: str):
    await update.message.reply_text(f'{name} делайте ваш ход: ')
'''


