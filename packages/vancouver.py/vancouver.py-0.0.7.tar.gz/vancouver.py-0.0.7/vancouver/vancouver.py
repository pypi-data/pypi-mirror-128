import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions

from pathlib import Path


class NotFound:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

class BadArgument:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

class UnknowError:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

class VancouverImage:
	def __init__(self, bot, channel) -> None:
		self.bot     = bot
		self.channel = channel

	async def url(self, path: str = ""):
		if Path(f"{path}").is_file() != True:
			return NotFound(
				"File not found.\nCheck if the filename is correct"
			)
		else:
			with open(path, "rb") as file:
				try:
					channel = self.bot.get_channel(self.channel)
					image   = await channel.send(
						file = discord.File(
							file, filename = "image_.png"
						)
					)
				except MissingPermissions:
					raise MissingPermissions("Can't send message")
				except commands.errors.ChannelNotFound:
					raise commands.errors.ChannelNotFound("Can't found channel")

			if image.attachments != []: 
				url = image.attachments[0].url

			return url