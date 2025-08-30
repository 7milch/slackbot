import os
import asyncio
import logging
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]  # xapp- で始まる
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]  # xoxb- で始まる
TARGET_EMOJI = "eyes"  # 反応したいemoji名

async def handle_events(client: SocketModeClient, req: SocketModeRequest):
    try:
        logger.info(f"Received event: {req.type}")
        if req.type == "events_api":
            event = req.payload["event"]
            logger.info(f"Event type: {event.get('type')}")
            # reaction_addedイベントかつ指定emojiか
            if event.get("type") == "reaction_added" and event.get("reaction") == TARGET_EMOJI:
                logger.info(f"Target emoji reaction detected: {event.get('reaction')}")
                user = event["user"]
                item = event["item"]
                channel = item["channel"]
                ts = item["ts"]
                web_client = client.web_client
                # メッセージに返信
                await web_client.chat_postMessage(
                    channel=channel,
                    thread_ts=ts,
                    text=f":{TARGET_EMOJI}: リアクションありがとう <@{user}>！"
                )
                logger.info("Reply sent successfully")
        # イベント受信のACK
        await client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
    except Exception as e:
        logger.error(f"Error handling event: {e}")
        # エラーが発生してもACKを送信
        await client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

async def main():
    try:
        logger.info("Starting Slack Bot...")
        logger.info(f"App Token: {SLACK_APP_TOKEN[:10]}...")
        logger.info(f"Bot Token: {SLACK_BOT_TOKEN[:10]}...")
        
        client = SocketModeClient(
            app_token=SLACK_APP_TOKEN,
            web_client=AsyncWebClient(token=SLACK_BOT_TOKEN)
        )
        client.socket_mode_request_listeners.append(handle_events)
        
        logger.info("Connecting to Slack...")
        await client.connect()
        logger.info("Connected to Slack successfully!")
        
        # 無限ループで待機
        while True:
            await asyncio.sleep(10)
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}")
        exit(1)
