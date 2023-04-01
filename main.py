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

with open('config.json') as f:
    config = json.load(f)

email    = config['email']
password = config['password']
api_id   = config['api_id']
api_hash = config['api_hash']
token    = config['token']
user_id  = config['user_id']



negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet"
sampler= 'DPM++ 2M Karras'
width  = 512
height = 512
model  = 'anything-v4.0-fp16-default'

def login(email,passwd):
    headers = {
        'authority': 'p0.kamiya.dev',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.kamiya.dev',
        'referer': 'https://www.kamiya.dev/',
        'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; Mi 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    }
    
    json_data = {
        'email': email ,
        'password': passwd ,
    }
    
    response = requests.post('https://p0.kamiya.dev/api/account/login', headers=headers, json=json_data)
    return response.json()["token"]
    
def gen_img(prompt,n_prompt,key):
    headers = {
        'authority': 'p0.kamiya.dev',
        'accept': 'application/json, text/javascript',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': f'Bearer {key}',
        'content-type': 'application/json',
        'origin': 'https://www.kamiya.dev',
        'referer': 'https://www.kamiya.dev/',
        'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; Mi 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    }
    
    json_data = {
        'prompt': prompt,
        'negativePrompt': n_prompt,
        'steps': 28,
        'scale': 12,
        'seed': random.randrange(100000000, 999999999),
        'sampler': sampler,
        'width': width,
        'height': height,
        'traceId': str(uuid.uuid4()),
        'model': model,
    }
    
    response = requests.post('https://p0.kamiya.dev/api/image/generate', headers=headers, json=json_data)
    return response.json()["image"]

def kamiya_api(prompt,n_prompt):
    key = login(email,password)
    url = gen_img(prompt,n_prompt,key)
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
        message.reply_text(f"Here is the current info:\nWidth:`{str(width)}`\nHeight:`{str(height)}`\nNegative Prompt:`{negative_prompt}`\nModel:`{model}`\nSampler:`{sampler}`")

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
