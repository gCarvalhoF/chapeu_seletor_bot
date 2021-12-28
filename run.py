import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from random import choice
from classes import House

load_dotenv()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=";", intents=intents)


grifinoria = House(
    'Grifinória', 'https://i.imgur.com/hmeEow4.png', discord.Color.dark_red(), 'https://media.giphy.com/media/VfgrRPB3gzEXE1dkJH/giphy.gif')
corvinal = House('Corvinal', 'https://i.imgur.com/clvXrtz.png',
                 discord.Color.dark_blue(), 'https://media.giphy.com/media/8eHkKBkxqzdgOs5Tj5/giphy.gif')
lufalufa = House(
    'Lufa Lufa', 'https://i.imgur.com/MC9EKuB.png', discord.Color.from_rgb(255, 255, 0), 'https://media.giphy.com/media/lH0opzhvIvZTBcvFWo/giphy.gif')
sonserina = House(
    'Sonserina', 'https://i.imgur.com/kMg4nix.png', discord.Color.dark_green(), 'https://media.giphy.com/media/oXDvyC3wFfIpgocN4A/giphy.gif')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    activity = discord.Game(name="🎩 Chapéu Seletor | Dev: gCarvalhof", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)


async def house_announcement(member, role):
    categories = member.guild.categories
    for category in categories:
        if role.name.upper() in category.name:
            for txt_channel in category.text_channels:
                if "boas-vindas" in txt_channel.name:
                    if 'Sonserina' in role.name:
                        color = sonserina.color
                        thumbnail_url = sonserina.symbol_url
                        image_url = sonserina.gif_url

                    elif 'Grifinória' in role.name:
                        color = grifinoria.color
                        thumbnail_url = grifinoria.symbol_url
                        image_url = grifinoria.gif_url

                    elif 'Corvinal' in role.name:
                        color = corvinal.color
                        thumbnail_url = corvinal.symbol_url
                        image_url = corvinal.gif_url

                    elif 'Lufa Lufa' in role.name:
                        color = lufalufa.color
                        thumbnail_url = lufalufa.symbol_url
                        image_url = lufalufa.gif_url

                    embed = discord.Embed(title=f"Você agora é da {role.name.capitalize()}",
                                          description=f"Seja bem-vindo(a) à {role}, esperamos que tenha uma boa jornada nessa casa e que possa fazer vários amigos por aqui!", color=color)
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_image(
                        url=image_url)

                    await txt_channel.send(embed=embed, content=f'|| {member.mention} ||')


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
