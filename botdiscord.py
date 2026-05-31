import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# Lấy Token từ biến môi trường
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
    # Chỉ bỏ qua tin nhắn của chính bot này để tránh loop
    if message.author == bot.user:
        return

    # Logic xử lý kênh bẫy (Honeypot)
    if message.channel.id == TRAP_CHANNEL_ID:
        # Cơ chế an toàn: Bỏ qua nếu người nhắn có quyền Administrator (tránh ban nhầm)
        if message.author.guild_permissions.administrator:
            await message.delete()
            print(f"Cảnh báo: Admin {message.author} vừa nhắn vào kênh bẫy. Đã xóa tin nhắn.")
            return

        try:
            await message.author.ban(reason="Tự động ban: Nhắn tin vào kênh Honeypot")
            await message.delete()
            print(f"Đã ban thành công: {message.author}")
        except discord.Forbidden:
            print(f"Thất bại: Bot không đủ quyền ban {message.author}. Hãy kiểm tra lại Role.")
        except discord.HTTPException as e:
            print(f"Lỗi hệ thống Discord: {e}")

    # Đảm bảo các lệnh prefix (nếu có) vẫn hoạt động
    await bot.process_commands(message)

# Khởi chạy web server ảo trước khi chạy bot
keep_alive()
bot.run(TOKEN)