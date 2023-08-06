from telegram import (ReplyKeyboardRemove, Update)
from telegram.ext import (CallbackContext)

def telegram_append_to_context(update: Update, context: CallbackContext, key, value):
    if not key in context.user_data:
        context.user_data[key] = []
    context.user_data[key].append(value)

def telegram_check_in_context(update: Update, context: CallbackContext, key, value, doppelte_antwort):
    if key in context.user_data:
        if value in context.user_data[key]:
            update.message.reply_text(doppelte_antwort,
                                  reply_markup=ReplyKeyboardRemove())
            return "{}_FRAGE".format(key.upper())

def telegram_eval_list(update: Update, context: CallbackContext, answer_id_name_list, poi, response_text):
    if not poi in context.user_data:
        context.user_data[poi] = []

    response_text += "\n"

    for id, name in answer_id_name_list:
        if id in context.user_data[poi]:
            response_text += "✅ {}\n".format(name)
        else: 
            response_text += "◽ {}\n".format(name)

    update.message.reply_text(response_text,
                              reply_markup=ReplyKeyboardRemove())

telegram_action_functions = {"append_to_context": telegram_append_to_context,
                    "check_in_context": telegram_check_in_context,
                    "eval_list": telegram_eval_list
                    }