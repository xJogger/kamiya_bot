# kamiya_bot

For those who understand, it's crystal clear.

1. To get started with this bot, you'll need to:

   - Obtain an API KEY [here](https://www.kamiya.dev/account.html).
   - Create a Telegram bot and obtain your bot token [here](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
   - Get your `api_id` and `api_hash` [here](https://telegra.ph/How-to-get-Telegram-APP-ID--API-HASH-05-27).

2. After obtaining the necessary credentials, follow these steps:

   - Clone this repository.
   - Copy `config.example.json` to `config.json` and fill in your Telegram bot information, API key, and other configuration details.

3. Start the bot using Docker Compose:

   ```bash
   docker-compose up -d
   ```

4. Send any text, and the bot will use that text as a prompt to generate an image. Enjoy using the bot!

About `user_id` and `time_out_img`:

- `user_id` is a restriction that allows only specific Telegram users to use this bot. You can obtain user IDs using [getidsbot](https://t.me/getidsbot).

- In case the image generation API takes longer than 10 minutes to return a picture URL, the bot will directly provide the image specified in 'time_out_img' (any valid JPG file URL).


The above content was drafted by xJogger and polished by GPT-3.5.
