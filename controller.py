import bot
import model
import view

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import view, model

app = ApplicationBuilder().token("5478500058:AAHkVgklz9m-8m1B5yoqv6T_ByRf6UFh_30").build()


async def printField(update, name: str):
    field = await model.getField()
    await view.printField(update, field, name)

async def start_game(update, context):
    await model.set_game()
    await view.start_game(update)
    name = update.effective_user.first_name
    await model.setName(name)
    await printField(update, name)
    first_turn = random.randint(0,1)
    if first_turn:
        await view.player_take(update, name)
    else: await enemyTurn(update, context)
    view.player_take(update, 'Бот')
    

async def playerTurn(update,context):
    game = await model.get_game()
    if game:
        move = 0

        if update.message.text == '/start':
            return
        else:
            move = int(update.message.text)
        field = await model.getField()
        mark = await model.getMark()
        name = await model.getName()
        move = await view.playerTurn(update, field, mark, name)
        await model.setPlayerMove(move)
        await printField(update, 'Бот')
        player_field = await model.getPlayerField()
        if await model.win_condition(player_field):
            await view.win(update, 'Игрок')
            return
        await model.changeMark()
        await enemyTurn(update,context)

async def enemyTurn(update,context):
    field = await model.getField()
    mark = await model.getMark()
    name = await model.getName()
    enemy_field = await model.getEnemyField()
    player_field = await model.getPlayerField()
    move = await bot.AIMove(field, player_field, enemy_field, model.win)

    field[move] = mark
    await model.setEnemyMove(move)
    await printField(update, name)
    enemy_field = await model.getEnemyField()
    if await model.win_condition(enemy_field):
        await view.win(update, 'Бот')
        return
    await model.changeMark()
    await playerTurn(update,context)

 
async def settings():
    pass

app.add_handler(CommandHandler('start', start_game))
app.add_handler(MessageHandler(filters.TEXT, playerTurn))

app.run_polling(drop_pending_updates=True)