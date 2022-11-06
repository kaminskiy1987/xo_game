'''
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
'''

import os
import random
import sys
import view
import bot

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CommandHandler, \
    CallbackQueryHandler
import model 

app = ApplicationBuilder().token("5478500058:AAHkVgklz9m-8m1B5yoqv6T_ByRf6UFh_30").build()


async def game(callBackData):
    message = model.ANSW_YOUR_TURN  
    alert = None

    buttonNumber = int(callBackData[0])  
    if not buttonNumber == 9: 
        charList = list(callBackData)  
        charList.pop(0) 
        if charList[buttonNumber] == model.SYMBOL_UNDEF: 
            charList[buttonNumber] = model.SYMBOL_X  
            if await model.isWin(charList, model.SYMBOL_X):  
                message = model.ANSW_YOU_WIN
            else:  
                if await model.getCountUndefinedCells(charList) != 0:  
                    isCycleContinue = True
                    while (isCycleContinue):
                       if charList[bot.AIMove(charList)] == model.SYMBOL_UNDEF:  
                            charList[bot.AIMove(charList)] = model.SYMBOL_O
                            isCycleContinue = False  
                            if await model.isWin(charList, model.SYMBOL_O):  
                                message = model.ANSW_BOT_WIN

        else:
            alert = model.ALERT_CANNOT_MOVE_TO_THIS_CELL

        if await model.getCountUndefinedCells(charList) == 0 and await message == model.ANSW_YOUR_TURN:
            message = model.ANSW_DRAW

        callBackData = ''
        for c in charList:
            callBackData += c

    if message == model.ANSW_YOU_WIN or message == model.ANSW_BOT_WIN or message == model.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += callBackData[j + i * 3] + ' | '
        callBackData = None  

    return message, callBackData, alert


def getKeyboard(callBackData):
    keyboard = [[], [], []]  

    if callBackData != None:  
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(
                    InlineKeyboardButton(callBackData[j + i * 3], callback_data=str(j + i * 3) + callBackData))

    return keyboard

async def newGame(update, _):
    data = ''
    for i in range(0, 9):
         data += model.SYMBOL_UNDEF

    await update.message.reply_text(model.ANSW_YOUR_TURN, reply_markup = InlineKeyboardMarkup(getKeyboard(data)))

async def button(update, _):
    query = update.callback_query
    callbackData = query.data  

    message, callbackData, alert = await game(callbackData) 
    if alert is None:  
        await query.answer()  
        await query.edit_message_text(text=message, reply_markup= InlineKeyboardMarkup(getKeyboard(callbackData)))
    else:  
        query.answer(text=alert, show_alert=True)

async def help_command(update, _):
    await update.message.reply_text(model.ANSW_HELP)


app.add_handler(CommandHandler('start', newGame))
app.add_handler(CommandHandler('new_game', newGame))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(MessageHandler(filters.TEXT, help_command))
app.add_handler(CallbackQueryHandler(button))

app.run_polling(drop_pending_updates=True)
