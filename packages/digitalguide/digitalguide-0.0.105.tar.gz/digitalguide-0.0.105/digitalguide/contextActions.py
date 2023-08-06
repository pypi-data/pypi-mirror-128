from telegram import (Update)
from telegram.ext import (CallbackContext)

def default_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.from_user.first_name

def save_text_to_context(update: Update, context: CallbackContext, key):
    context.user_data[key] = update.message.text

def save_value_to_context(update: Update, context: CallbackContext, key, value):
    context.user_data[key] = value

action_functions = {"default_name": default_name,
                    "save_text_to_context": save_text_to_context,
                    "save_value_to_context": save_value_to_context
                    }