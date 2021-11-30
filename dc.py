"""
Author: Ju0x (https://github.com/Ju0x)
This is just a very minimalistic Code-example for a Discord-Bot, that works with this method.
If you want to use it on multiple servers, please add a path for every server in the JSON
"""

import nextcord
from nextcord.ext import commands
import secrets
import json
import asyncio

bot = commands.Bot(
    command_prefix="!",
    intents=nextcord.Intents.all()  # TODO: Change for verified bots
)
image_server = "http://127.0.0.1:5000"


@bot.event
async def on_ready():
    print(f"{bot.user} - Started successfully")


"""
This method makes only sense, if the verification is in a private chat
"""


async def start_captcha(member: nextcord.Member):
    id_code = secrets.token_urlsafe(8)  # Generates the Identifier

    with open("./ids.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if not data.get("active"):
        data["active"] = {}

    data["active"][str(member.id)] = {
        "request_count": 0,
        "id": id_code
    }

    with open("./ids.json", "w+", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    message = await member.send(
        embed=nextcord.Embed(
            title="Verification - Please verify you!",
            description="Click on the checkmark under this message to get verified.",
            color=0x00FF43
        ).set_thumbnail(
            url=f"{image_server}/captcha?id={id_code}"  # Sets the pixel in the embed
        )
    )
    await message.add_reaction("☑")

    def check(reaction, user) -> bool:
        if user == member:
            if str(reaction.emoji) == "☑":
                return True
        return False

    try:
        await bot.wait_for("reaction_add", timeout=180.0, check=check)

        with open("./ids.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Checks if the user is still in the JSON
        if data.get("active"):
            if data["active"].get(str(member.id)):
                if data["active"][str(member.id)].get("request_count"):
                    if data["active"][str(member.id)]["request_count"] >= 2:
                        await member.send(
                            embed=nextcord.Embed(
                                description="**Verification complete!**",
                                color=0x00FF43
                            )
                        )

                        # TODO: Some actions
                        return
    except asyncio.TimeoutError:
        pass

    await member.send(
        embed=nextcord.Embed(
            description="**The verification failed. Please contact the staff.**",
            color=nextcord.Color.red()
        )
    )


@bot.event
async def on_member_join(member):
    if member.bot:
        return

    """
    Here are no permission changes for the user on discord, so if you use it, please add code for the permissions
    """

    await start_captcha(member)


bot.run()  # Runs the bot with the specific Discord-Token
