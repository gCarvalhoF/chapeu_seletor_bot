import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from random import choice


load_dotenv()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=";", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def house_announcement(member, role):
    categories = member.guild.categories
    for category in categories:
        if role.name.upper() in category.name:
            for txt_channel in category.text_channels:
                if "boas-vindas" in txt_channel.name:

                    if 'Sonserina' in role.name:
                        color = discord.Color.dark_green()
                    elif 'Grifinória' in role.name:
                        color = discord.Color.dark_red()
                    elif 'Corvinal' in role.name:
                        color = discord.Color.dark_blue()
                    elif 'Lufa Lufa' in role.name:
                        color = discord.Color.from_rgb(255, 255, 0)

                    embed = discord.Embed(title="Chapéu Seletor",
                                          description=f"Seja bem-vindo(a) à {role}, esperamos que tenha uma boa jornada nessa casa e que possa fazer vários amigos por aqui!", color=color)
                    embed.set_image(
                        url="https://pa1.narvii.com/6098/29a466d6b235e8ae5f27ce35644b66f4cef34065_hq.gif")

                    await txt_channel.send(embed=embed, content=member.mention)


@bot.command()
async def start(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Chapéu Seletor",
                          description="Reaja a essa mensagem para descobrir qual sua casa de Hogwarts!", color=discord.Color.green())
    embed.set_image(
        url="https://pa1.narvii.com/6098/29a466d6b235e8ae5f27ce35644b66f4cef34065_hq.gif")
    message = await ctx.send(embed=embed)
    await message.add_reaction('🎩')


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member == bot.user:
        return

    roles = [discord.utils.get(payload.member.guild.roles, name="Corvinal"), discord.utils.get(payload.member.guild.roles, name="Grifinória"), discord.utils.get(
        payload.member.guild.roles, name="Sonserina"), discord.utils.get(payload.member.guild.roles, name="Lufa Lufa")]
    role = choice(roles)

    if payload.channel_id == 924034060085510215:
        await payload.member.add_roles(role)
        await payload.member.remove_roles(discord.utils.get(payload.member.guild.roles, name="Aluno Hogwarts"))

        await house_announcement(payload.member, role)


bot.run(os.getenv('TOKEN'))
