# Discord bot import
import discord
from discord import app_commands
import os
import random
import ndjson
import glob
from dotenv import load_dotenv

# My program import
# None

# Bot Start
load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 煽る、励ます文書
phrase = [
    "頑張って！あなたならできるよ。",
    "一歩一歩進んでいこう。焦らずにね。",
    "少しずつでも、前に進めば必ずゴールに辿り着くよ。",
    "もう少し頑張ろうよ。諦めるのはまだ早いよ。",
    "いつまでさぼってるつもり？時間は有限だよ。",
    "真面目に取り組まないと、後で後悔することになるよ。",
    "やるべきことを放置しても、問題は解決しないよ。",
    "周りが頑張っている中で、君だけが遅れているよ。",
    "努力しないと、結果は出ないよ。自分に厳しくしよう。",
    "このままだと、信頼を失ってしまうよ。しっかりしよう。",
]

#ここに対象としたいDiscordユーザーのユーザーIDを入れてください！
#（※「000000000000000000」の部分を置き換える）
user_id = 000000000000000000

# Bot起動時の処理
@client.event
async def on_ready():
    print("Bot User login!")

    # スラッシュコマンドを同期
    await tree.sync()
    print("global command finish!")

    # guild_jsonフォルダがあるかの確認
    files = glob.glob("./*")
    judge = 0

    for i in range(0, len(files)):
        if(os.path.split(files[i])[1] == "guild_json"):
            print("guild_json already!")
            judge = 1
            break
    
    if judge != 1:
        os.mkdir("guild_json")
        print("Create guild_json file!")

# サーバーからキック、BANされた場合に特定の処理をする
@client.event
async def on_guild_remobe(guild):
    file = str(guild.id) + ".ndjson"
    files = glob.glob("./guild_json/*.ndjson")
    judge = 0

    for i in range(0, len(files)):
        if(os.path.split(files[i])[1] == str(guild.id) + ".ndjson"):
            print("guild_json already!")
            judge = 1
            break
    
    if judge == 1:
        os.remove("./guild_json/" + file)
        print("file remove. \n Reason: BAN or Kick.")
    
# メッセージを取得したときに実行される
@client.event
async def on_message(message):
    try:
        with open('./guild_json/' + str(message.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)
    except Exception as e:
        pass
    
    print(read_data)

    # Botのメッセージは除外する
    if message.author.bot:
        return
    
    print(read_data[0]["mode"])

    if read_data[0]["mode"] == "start":
        try:
            if message.author.id == user_id:
                num = random.randint(0, len(phrase))

                await message.reply("<@" + str(user_id) + ">\n" + phrase[num])
        except Exception as e:
            pass

# スラッシュコマンド
@tree.command(name="aori_and_hagemasi",description="煽り、励ましのオン・オフを行います。")
@discord.app_commands.guild_only()
@discord.app_commands.choices(mode=[discord.app_commands.Choice(name="start",value="start"),discord.app_commands.Choice(name="stop",value="stop")])
async def aori_and_hagemasi_commando(interaction: discord.Integration,mode:str):
    if mode == "start":
        # 既にファイルが存在しているかの判定
        files = glob.glob("./guild_json/*.ndjson")
        judge = 0

        for i in range(0, len(files)):
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                judge = 1
                break

        if judge == 0:
            content = {
                "mode" : "start"
            }
        
            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(content)
        else:
            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)

            if read_data[0]["mode"] == "start":
                embed = discord.Embed(title="既に煽り、励ましを開始しています！", description="<@" + str(user_id) + ">に対する煽り・励ましを止めたい場合は、/aori_and_hagemasiコマンドでstopを指定してください。", color=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=False)
                return

            read_data[0]["mode"] = "start"

            os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")

            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(read_data[0])
            
        embed = discord.Embed(title="煽り、励ましを開始します！", description="<@" + str(user_id) + ">に対する煽り・励ましを開始します。", color=0x00ff40)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        # 既にファイルが存在しているかの判定
        files = glob.glob("./guild_json/*.ndjson")
        judge = 0

        for i in range(0, len(files)):
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                judge = 1
                break

        if judge == 0:
            embed = discord.Embed(title="エラー！", description="このサーバーでは<@" + str(user_id) + ">へ対する煽り・励ましを始めた事がありません。始めたい場合は、/aori_and_hagemasiコマンドでstartを指定してください。。", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return
        else:
            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)

            if read_data[0]["mode"] == "stop":
                embed = discord.Embed(title="既に煽り、励ましを停止しています！", description="<@" + str(user_id) + ">に対する煽り・励ましを始めたい場合は、/aori_and_hagemasiコマンドでstartを指定してください。", color=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=False)
                return

            read_data[0]["mode"] = "stop"

            os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")

            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(read_data[0])
            
            embed = discord.Embed(title="煽り、励ましを終了します！", description="<@" + str(user_id) + ">に対する煽り・励ましを停止します。", color=0x00ff40)
            await interaction.response.send_message(embed=embed, ephemeral=False)

client.run(os.environ['token'])