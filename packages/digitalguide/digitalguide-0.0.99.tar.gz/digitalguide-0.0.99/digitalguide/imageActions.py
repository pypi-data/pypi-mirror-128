from PIL import Image
from io import BytesIO

from telegram import (Update)
from telegram.ext import (CallbackContext)

def generate_gif(im1, im2):
    im1 = im1.resize((round(im1.size[0]*1), round(im1.size[1]*1)))
    im2 = im2.resize((round(im1.size[0]), round(im1.size[1])))

    images = []
    frames = 10

    for i in range(frames+1):
        im = Image.blend(im1, im2, i/frames)
        images.append(im)
        
    for i in range(frames+1):
        im = Image.blend(im1, im2, 1-i/frames)
        images.append(im)


    bio = BytesIO()
    bio.name = 'image.gif'

    images[0].save(bio, 'GIF', save_all=True, append_images=images[1:], duration=150, loop=0, optimize=True)
    bio.seek(0)
    return bio

def overlay_images(background, foreground):
    foreground = foreground.resize((round(background.size[0]), round(background.size[1])))
    background.paste(foreground, (0, 0), foreground)
    bio = BytesIO()
    bio.name = 'image.png'
    background.save(bio, 'PNG')
    bio.seek(0)
    return bio

def eval_gif_generation(update: Update, context: CallbackContext, picture):
    im_bytes = update.message.photo[-1].get_file().download_as_bytearray()

    im_file = BytesIO(im_bytes)  # convert image to file-like object
    im1 = Image.open(im_file)   # img is now PIL Image object
    print(picture)
    im2 = Image.open('assets/' + picture)

    gif = generate_gif(im1, im2)

    update.message.reply_document(gif)

action_functions = {"eval_gif_generation": eval_gif_generation,
                    }