import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# Lấy Token từ biến môi trường
TOKEN = os.getenv("DISCORD_TOKEN")

# Lấy ID động từ biến môi trường và ép kiểu sang số nguyên (int)
try:
    TRAP_CHANNEL_ID = int(os.getenv("TRAP_CHANNEL_ID"))
    OWNER_ID = int(os.getenv("OWNER_ID"))
except (TypeError, ValueError):
    print("❌ LỖI KHỞI ĐỘNG: Thiếu TRAP_CHANNEL_ID hoặc OWNER_ID trong file .env hoặc Render!")
    exit()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    # Bỏ qua tin nhắn của chính bot
    if message.author == bot.user:
        return

    # Logic xử lý kênh bẫy
    if message.channel.id == TRAP_CHANNEL_ID:
        # Bỏ qua nếu là Admin
        if message.author.guild_permissions.administrator:
            await message.delete()
            print(f"Cảnh báo: Admin {message.author} vừa nhắn vào kênh bẫy. Đã xóa tin nhắn.")
            return

        try:
            # Ban kẻ spam và xóa tin nhắn
            await message.author.ban(reason="Tự động ban: Nhắn tin vào kênh Honeypot")
            await message.delete()
            print(f"Đã ban thành công: {message.author}")
            
            # Gửi tin nhắn trực tiếp cho bạn
            try:
                owner = await bot.fetch_user(OWNER_ID)
                await owner.send(
                    f"🚨 **Báo cáo chống Spam:**\n"
                    f"Vừa ban thành công kẻ gian: `{message.author}`\n"
                    f"ID: `{message.author.id}`\n"
                    f"Lý do: Đạp bẫy tại kênh Honeypot."
                )
            except discord.Forbidden:
                print("Lỗi: Không thể DM cho chủ bot. (Hãy kiểm tra lại cài đặt quyền riêng tư của bạn)")
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn cho chủ bot: {e}")

        except discord.Forbidden:
            print(f"Thất bại: Bot không đủ quyền ban {message.author}.")
        except discord.HTTPException as e:
            print(f"Lỗi hệ thống Discord: {e}")

    await bot.process_commands(message)

# Khởi chạy web server ảo trước khi chạy bot
keep_alive()
bot.run(TOKEN)