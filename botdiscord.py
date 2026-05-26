import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# Lấy Token từ biến môi trường (Sẽ cài đặt trên Render sau)
TOKEN = os.getenv("DISCORD_TOKEN")
TRAP_CHANNEL_ID = 1508654735110963250  # Thay bằng ID kênh thật của bạn

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == TRAP_CHANNEL_ID:
        try:
            await message.author.ban(reason="Tự động ban: Nhắn tin vào kênh Honeypot")
            await message.delete()
        except discord.Forbidden:
            print("Thất bại: Bot không đủ quyền.")
        except discord.HTTPException as e:
            print(f"Lỗi: {e}")

    await bot.process_commands(message)

# Khởi chạy web server ảo trước khi chạy bot
keep_alive()
bot.run(TOKEN)