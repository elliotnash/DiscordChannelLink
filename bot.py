import os

CHANNELS_TO_SYNC = [
  863993730302607360,
  863993776275062804
]

#plz don't use in production :)
TOKEN = os.environ['TOKEN']

import discord 

client = discord.Client()

async def get_webhook(channel):
  webhooks = await channel.webhooks()
  for webhook in webhooks:
    if webhook.token != "":
      return webhook
  return await channel.create_webhook(name="SyncHook")


@client.event
async def on_ready():
  print(f'Client connected as {client.user}')

@client.event
async def on_message(msg):
  if msg.channel.id in CHANNELS_TO_SYNC and not msg.author.bot:
    for channel_id in CHANNELS_TO_SYNC:
      if channel_id == msg.channel.id:
        continue
      channel = await client.fetch_channel(channel_id)
      webhook = await get_webhook(channel)

      content = msg.content
      embeds = msg.embeds
      attachments = msg.attachments

      username = msg.author.name
      avatar_url = msg.author.avatar_url

      await webhook.send(content=msg.content, username=username, avatar_url=avatar_url, files=attachments, embeds=embeds, allowed_mentions=discord.AllowedMentions.none())

client.run(TOKEN)
