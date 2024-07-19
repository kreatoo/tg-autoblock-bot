from telethon import TelegramClient, events, functions
from telethon.errors import PeerIdInvalidError

# Remember to change these!
api_id = 45678
api_hash = 'jgjotr0eq2iewjfjgghkhohoh'
message = 'You are not in my contacts, blocking!'

# Session name
session_name = 'tg-autoblock-bot'
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    sender = await event.get_sender()
    
    if event.message and event.message.sender and not event.message.sender.bot:
  # Check if sender is a message and the sender is not a bot
        try:
            # Get contacts
            contacts = await client(functions.contacts.GetContactsRequest(hash=0))
            sender_in_contacts = any(contact.id == sender.id for contact in contacts.users)

            if not sender_in_contacts and sender.id != (await client.get_me()).id:
                
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

        except Exception as e:
            print(f"An error occurred: {e}")

client.start()
client.run_until_disconnected()
