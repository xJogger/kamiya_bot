from pyrogram import Client, filters
from pyrogram.types import *
import os
import json
import requests
import io
import random
from PIL import Image, PngImagePlugin
import base64
import uuid
import time

with open('config.json') as f:
    config = json.load(f)

key          = config['key']
time_out_img = config['time_out_img']
api_id       = config['api_id']
api_hash     = config['api_hash']
token        = config['token']
user_id      = config['user_id']

'''
cmd:
start - Say Hello
info - Show info
set_an - Set Anything
set_ab - Set AbyssOrangeMix3_A2(AOM3A2)
set_l - Set 768x512 
set_p - Set 512x768 
set_s - Set 640x640
'''


negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet"
sampler= 'DPM++ 2M Karras'
width  = 640
height = 640
model  = 'Anything-v4.5-pruned-mergedVa'

def get_config(key):
    headers = {
        "Authorization": f"Bearer {key}"
    }
    response = requests.get('https://p0.kamiya.dev/api/image/config', headers=headers)
    return response.json()

def gen_img(prompt,n_prompt,key):
    headers = {
        "Authorization": f"Bearer {key}"
    }
    
    json_data = {
        "type": "text2image",
        "prompts": prompt,
        "negativePrompts": n_prompt,
        "step": 28,
        "cfg": 12,
        "seed": random.randrange(100000000, 999999999),
        "sampling": sampler,
        "width": width,
        "height": height,
        "model": model,
        "LoRAs": []
    }
    
    response = requests.post('https://p0.kamiya.dev/api/image/generate', headers=headers, json=json_data)
    return response.json()["data"]["hashid"]

def get_img(hashid,key,wait_time=600):
    headers = {
        "Authorization": f"Bearer {key}"
    }
    
    response = requests.get(f'https://p0.kamiya.dev/api/image/generate/{hashid}', headers=headers)

    time_cnt = 0
    while('jpg' not in response.json()["data"]["metadata"]):
        time.sleep(1);time_cnt = time_cnt + 1
        if time_cnt > wait_time: return time_out_img
        response = requests.get(f'https://p0.kamiya.dev/api/image/generate/{hashid}', headers=headers)
    return response.json()["data"]["metadata"]["jpg"]

def kamiya_api(prompt,n_prompt):
    hashid = gen_img(prompt,n_prompt,key)
    url    = get_img(hashid,key)
    return url

app = Client(
    "stable",
    api_id   =api_id,
    api_hash =api_hash,
    bot_token=token
)


@app.on_message(filters.command(["info"]))
def info(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        message.reply_text(f"Here is the current info : \nWidth : `{str(width)}`\nHeight : `{str(height)}`\nNegative Prompt : `{negative_prompt}`\nModel : `{model}`\nSampler : `{sampler}`")

@app.on_message(filters.command(["set_ab"]))
def set_ab(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        global model
        model = "aom3a2"
        message.reply_text(f"Current model is : `{model}`")

@app.on_message(filters.command(["set_an"]))
def set_an(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        global model
        model = 'Anything-v4.5-pruned-mergedVa'
        message.reply_text(f"Current model is : `{model}`")

@app.on_message(filters.command(["set_l"]))
def set_l(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        global width
        global height
        width = 768
        height = 512
        message.reply_text(f"Current width x height is : `768x512`")

@app.on_message(filters.command(["set_p"]))
def set_p(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        global width
        global height
        width = 512
        height = 768
        message.reply_text(f"Current width x height is : `512x768`")

@app.on_message(filters.command(["set_s"]))
def set_s(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
    else:
        global width
        global height
        width = 640
        height = 640
        message.reply_text(f"Current width x height is : `640x640`")


@app.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    await message.reply_text("Hello!")

@app.on_message(filters.text)
def draw(client, message):
    if message.from_user.id != user_id:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")
        #print(message.from_user.id,user_id)
        #print(type(message.from_user.id),type(user_id))
    else:

        msg = message.text

        K = message.reply_text("Server is working ...")

        try:
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            chars1 = "1234564890"
            gen1 = random.choice(chars)
            gen2 = random.choice(chars)
            gen3 = random.choice(chars1)
            gen4 = random.choice(chars)
            gen5 = random.choice(chars)
            gen6 = random.choice(chars)
            gen7 = random.choice(chars1)
            gen8 = random.choice(chars)
            gen9 = random.choice(chars)
            gen10 = random.choice(chars1)
            word = f"{message.from_user.id}-MOE{gen1}{gen2}{gen3}{gen4}{gen5}{gen6}{gen7}{gen8}{gen9}{gen10}"

            url = kamiya_api(msg,negative_prompt)
            res = requests.get(url)
            with open(f'{word}.png', 'wb') as f:
                f.write(res.content)

            message.reply_photo(
                photo=f"{word}.png",
                caption=
                f"Prompt: **`{msg}`**\n[Picture]({url}) by **{message.from_user.first_name}**"
            )
            os.remove(f"{word}.png")
            K.delete()
        except Exception as e:
            message.reply_text(f"An server error occurred:\n`{e}`")
            K.delete()

app.run()
