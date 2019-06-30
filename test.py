import discord
from discord.ext import commands
from datetime import datetime
import io
import aiohttp
import random
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
    await ctx.send("{} has been set as the default pin channel, silly! ow< ~☆".format(ctx.message.channel.mention))
# L M A O FUCK OFF WITH THAT LOWERCASE BITCH O H  M Y  G O D BWETTER TWANK U UWU

#Pin mover owo
@bot.command() #<3
async def migrate(ctx):
    migration = ctx.message.channel 
    pins = await migration.pins()
    if len(pins) != 0:
        #async with bot.get_channel(defaultChannel).typing(): (issue: wonky... so i didnt implement :'D)
        for x in reversed(pins):
            embed = discord.Embed(title = "")
            embed.set_author(name = x.author.display_name, icon_url = x.author.avatar_url)

            if x.content: #if a string is empty, it will return false in a boolean
                if len(x.content) > 256: 
                    embed.add_field(name = x.clean_content[:253] + "...", value = x.created_at.strftime("%D @ %T %p") + " - this message was hecka long, silly! ☆W☆ [jump to see the rest](" + x.jump_url + ")")
                else: 
                    embed.add_field(name = x.clean_content, value = x.created_at.strftime("%D @ %T %p") + " - [jump](" + x.jump_url + ")")

                if len(x.attachments) >= 1:
                    #I I LOVE YOU I LO3333333333ASOIDJFKS3ADJFMSADJGMSDGOWO<3
                    if len(x.attachments) == 1:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachment below")
                    else:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachments below")
            
            else:
                #for text/embeds with attachments
                if len(x.attachments) >= 1:
                    embed.add_field(name = "\u200b", value = x.created_at.strftime("%D @ %T %p") + " - [jump](" + x.jump_url + ")")
                    if len(x.attachments) == 1:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachment below") 
                    else:
                        embed.set_footer(text = "{}".format(len(x.attachments)) + " attachments below")
                    await bot.get_channel(defaultChannel).send(embed = embed) 
        
                #for text-only embeds (because these always go into this overarching else statement)
                if len(x.embeds) != 0:
                    embed.set_author(name = x.embeds[0].author.name, icon_url = x.embeds[0].author.icon_url)
                    for y in x.embeds[0].fields:
                        embed.add_field(name = y.name, value = y.value) #issue: value (date/jump) when there are multiple fields 
                    await bot.get_channel(defaultChannel).send(embed = embed)

            if len(x.attachments) >= 1:
                for y in x.attachments:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(y.url) as resp:
                            if resp.status != 200:
                                return await ctx.send('File not found, silly! >w<') #how do i make a sad owo face
                            data = io.BytesIO(await resp.read())
                            await bot.get_channel(defaultChannel).send(file=discord.File(data, y.filename))

        await ctx.send("Messages have been migrated, silly! uwu")
    else: await ctx.send("There aren't any pins here, silly! òwó")

#Random pin generator owo
@bot.command()
async def randompin(ctx):
    messages = await ctx.message.channel.history().flatten()
    message = messages[random.randint(0,len(messages))]
    await ctx.send("heres a random pin, silly! ◕w◕ :point_down:")
    if(len(message.embeds)!=0):
        await bot.get_channel(defaultChannel).send(embed = message.embeds[0]) #issue: sending two messages (embed AND attachment)
    else: 
        await ctx.send("{}".format(message.clean_content))

#literally just to make sure it works
@bot.command()
async def test(ctx):
    await ctx.send("yo i work, silly! OwO")

bot.run('TOKEN')