import discord
from discord.ext import commands
from datetime import datetime
import io
import aiohttp
#owo
description = "a disc bot to handle pins a lil better"
bot = commands.Bot(command_prefix='!', description=description, case_insensitive=True)

defaultChannel = 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#Channel set function
@bot.command()
async def setchannel(ctx):
    global defaultChannel
    defaultChannel = ctx.message.channel.id
    await ctx.send("#{} has been set as the default pin channel, silly! ow< ~☆".format(ctx.message.channel))
# L M A O FUCK OFF WITH THAT LOWERCASE BITCH O H  M Y  G O D BWETTER TWANK U UWU

#Pin mover owo
@bot.command() #<3
async def migrate(ctx):
    migration = ctx.message.channel 
    pins = await migration.pins()
    if len(pins) != 0:
        for x in reversed(pins):
            embed = discord.Embed(title = "")
            embed.set_author(name = x.author.display_name, icon_url = x.author.avatar_url)

            if x.content: #if a string is empty, it will return false in a boolean
                if len(x.content) > 256: 
                    embed.add_field(name = x.clean_content[:253] + "...", value = x.created_at.strftime("%D @ %T %p") + " - this message was hecka long, silly! ☆W☆ [jump to see the rest](" + x.jump_url + ")")
                else: 
                    embed.add_field(name = x.clean_content, value = x.created_at.strftime("%D @ %T %p") + " - [jump](" + x.jump_url + ")")
                
                if len(x.attachments) != 0:
                    #I I LOVE YOU I LO3333333333ASOIDJFKS3ADJFMSADJGMSDGOWO<3
                    if len(x.attachments) == 1:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachment below")
                    else:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachments below")
            else:
                embed.add_field(name = "\u200b", value = x.created_at.strftime("%D @ %T %p") + " - [jump](" + x.jump_url + ")")
                if len(x.attachments) == 1:
                    embed.set_footer(text = "{}".format(len(x.attachments)) + " attachment below") # FIX THIS ONE TOO HEH
                else:
                    embed.set_footer(text = "{}".format(len(x.attachments)) + " attachments below")
            await bot.get_channel(defaultChannel).send(embed = embed)

            if len(x.attachments) != 0:
                for y in x.attachments:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(y.url) as resp:
                            if resp.status != 200:
                                return await ctx.send('File not found, silly! >w<') #how do i make a sad owo face
                            data = io.BytesIO(await resp.read())
                            await bot.get_channel(defaultChannel).send(file=discord.File(data, y.filename))

        await ctx.send("Messages have been migrated, silly! uwu")
    else: await ctx.send("There aren't any pins here, silly! òwó")



#literally just to make sure it works
@bot.command()
async def test(ctx):
    await ctx.send("yo i work, silly! OwO")

bot.run('TOKEN')
