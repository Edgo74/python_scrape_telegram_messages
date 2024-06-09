from telethon.sync import TelegramClient
from dotenv import dotenv_values
import datetime
import pandas as pd
import pytz


utc=pytz.UTC


# Load environment variables from .env
env_vars = dotenv_values('.env')


api_id = env_vars.get("API_ID")
api_hash = env_vars.get("API_HASH")


# Define chat groups
chats = ['your_chat_group']

# Initialize the Telegram client
client = TelegramClient('test', api_id, api_hash)

# Create an empty DataFrame to store messages
df = pd.DataFrame()


start_date = datetime.datetime(2024, 6, 7, 17, 30, 0)
end_date = datetime.datetime(2024, 6, 8, 4, 30, 0)

start_date = start_date.replace(tzinfo=utc)
end_date =end_date.replace(tzinfo=utc)



# Iterate through each chat group
with client:
    for chat in chats:
        # Fetch messages from the chat within the date range
        for message in client.iter_messages(chat, offset_date=start_date, reverse=True):
            message_date = message.date.replace(tzinfo=utc)
            if start_date <= message.date <= end_date:
                data = {
                    "group": chat,
                    "sender": message.sender_id,
                    "text": message.text,
                    "date": message.date
                }
                temp_df = pd.DataFrame([data])
                df = pd.concat([df, temp_df], ignore_index=True)

# Convert date column to timezone naive
df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)

# Save DataFrame to Excel file
df.to_excel(f"C:\\users\\adami\\test.xlsx", index=False)


