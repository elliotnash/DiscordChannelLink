import discord
import toml

config = toml.load('config.toml')
TOKEN = config['TOKEN']
CHANNELS_TO_SYNC = config['SYNCED_CHANNELS']

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
  if msg.channel.id in CHANNELS_TO_SYNC and not msg.webhook_id:
    for channel_id in CHANNELS_TO_SYNC:
      if channel_id == msg.channel.id:
        continue
      channel = await client.fetch_channel(channel_id)
      webhook = await get_webhook(channel)

      content = msg.content
      embeds = msg.embeds
      files = []
      for attachment in msg.attachments:
        if attachment.size <= 8000000:
          files.append(await attachment.to_file())

      username = msg.author.name
      avatar_url = msg.author.avatar_url

      await webhook.send(
        content=content,
        username=username,
        avatar_url=avatar_url,
        files=files,
        embeds=embeds,
        allowed_mentions=discord.AllowedMentions.none()
      )

client.run(TOKEN)
