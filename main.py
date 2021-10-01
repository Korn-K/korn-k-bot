from repository import Repository
from keep_alive import keep_alive
import discord
import os
import random

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

def get_invoicechannel_members():
  voice_channel_id = int(os.getenv('VOICE_CHANNEL_ID'))
  channel = client.get_channel(voice_channel_id)
  members = list(channel.members)
  online_members = list(
    filter(lambda x: 
      str(x.status) == 'online' and not x.bot, 
      members)
    )
  return online_members

async def sample(message):
  users = get_invoicechannel_members()
  existed_user_ids = set(Repository().findAll())

  target_users = list(filter(lambda x: str(x.id) not in existed_user_ids, users))

  if(len(target_users) == 0): 
    await message.channel.send("🙃 ครบทุกคนแล้ว เริ่มใหม่")
    Repository().reset()
    target_users = users

  selected_user = random.sample(target_users, 1)[0]

  Repository().save(selected_user.id)
  
  await message.channel.send("เชิญ <@!{}> มาตอบคำถาม".format(selected_user.id))

@client.event
async def on_message(message):
  if message.content.startswith("-sample"):
    await sample(message)

  if message.content.startswith("ใครหล่อสุดในนี้"):
    await message.channel.send("เอกไงจะใครละ")

  # if message.author.name == "Korn K.":
  #   await message.channel.send("สวัสดีพี่เอกสุดหล่อ")

  if (message.content.startswith("-p") or message.content.startswith("!p")) and not message.channel.name.startswith("ใส่เพลง"):
    await message.channel.send("กรุณาขอเพลงในชาแนล \`ใส่เพลง\`")
  
  if message.content.startswith("sg!") and not message.channel.name.startswith("soccer"):
    await message.channel.send("กรุณาเล่นบอลในชาแนล \`soccer\`")


keep_alive()
client.run(os.getenv("DISCORD_BOT_TOKEN"))