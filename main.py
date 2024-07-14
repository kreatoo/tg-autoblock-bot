from telethon import TelegramClient, events, sync
from telethon import functions, types

# Remember to change these!
api_id = 45678
api_hash = 'jgjotr0eq2iewjfjgghkhohoh'
message = 'You are not in my contacts, blocking!'

# Session name
session_name='tg-autoblock-bot'
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    if not event.contact:
        sender = await event.get_sender()
        
        try:
            # Send a message to the sender
            await client.send_message(sender.id, message)

            # Block the sender
            await client(functions.contacts.BlockRequest(id=sender.id))

            # Delete the chat history
            await client(functions.messages.DeleteHistoryRequest(
                peer=sender.id,
                max_id=0,
                just_clear=True,
                revoke=False
            ))

        except PeerIdInvalidError:
            print(f"Invalid peer ID for sender: {sender.id}. Skipping this sender.")
        except Exception as e:
            print(f"An error occurred: {e}")

client.start()
client.run_until_disconnected()
