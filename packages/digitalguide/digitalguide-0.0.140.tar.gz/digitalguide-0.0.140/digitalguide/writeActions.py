import boto3
from datetime import datetime
import os
from telegram import CallbackQuery
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

session = boto3.session.Session()
client = session.client('s3',
                        region_name=config["space"]["region_name"],
                        endpoint_url=config["space"]["endpoint_url"],
                        aws_access_key_id=os.getenv('SPACES_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET'))


def telegram_write_photo(update, context, bucket, folder):
    user_id = update.effective_user.id
    name = update.effective_user.name

    client.put_object(Bucket=bucket,
                      Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.jpg',
                      Body=update.message.photo[-1].get_file().download_as_bytearray(),
                      ACL='private',
                      #Metadata={
                      #    'x-amz-meta-my-key': 'your-value'
                      #}
                      )

def telegram_write_message(update, context, bucket, folder):
    user_id = update.effective_user.id
    name = update.effective_user.name
    message = update.effective_message.text

    client.put_object(Bucket=bucket,
                      Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.txt',
                      Body=message,
                      ACL='private',
                      #Metadata={
                      #    'x-amz-meta-my-key': 'your-value'
                      #}
                      )

def telegram_write_voice(update, context, bucket, folder):
    user_id = update.effective_user.id
    name = update.effective_user.name

    client.put_object(Bucket=bucket,
                    Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.mp3',
                    Body=update.message.voice.get_file().download_as_bytearray(),
                    ACL='private',
                    #Metadata={
                    #    'x-amz-meta-my-key': 'your-value'
                    #}
                    )

def telegram_write(update, context, bucket, folder):
    if type(update)==CallbackQuery:
        pass
    elif update.message.voice:
        telegram_write_voice(update, context, bucket, folder)
    elif update.message.text:
        telegram_write_message(update, context, bucket, folder)
    elif update.message.photo:
        telegram_write_photo(update, context, bucket, folder)
    else:
        raise NotImplementedError("This type of update can not be saved")

telegram_action_functions = {"write_photo": telegram_write_photo,
                    "write_message": telegram_write_message,
                    "write_voice": telegram_write_voice,
                    "write": telegram_write
                    }