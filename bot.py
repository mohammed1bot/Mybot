import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message

# توكن البوت الخاص بك
TOKEN = "8790699159:AAEiqdvSc8VnC9q-ut0XNwTYAr-caZ0vEHY"

# الآيدي الخاص بك لتصلك الإشعارات عليه
ADMIN_ID = 6177263456

# قائمة الكلمات والعبارات المستهدفة للفلترة
BANNED_WORDS = [
    "تعرفون حد",
    "حد يعرف استاذ",
    "تعرفون حد يحل",
    "محتاج مدرس",
    "حد عنده استاذ",
    "محتاج مساعدة",
    "حد عنده توتر",
    "Assignment help",
    "يحل بروجكت",
    "يحل اسايمنت",
    "مدرس خصوصي",
    "محتاجه مدرس خصوصي",
    "يحل",
    "تعرفون حد يسوي",
    "حد يسوي"
]

dp = Dispatcher()

@dp.message(F.text)
async def monitor_messages(message: Message, bot: Bot):
    if not message.text:
        return
    
    # مراقبة المجموعات فقط وعدم الرد في الرسائل الخاصة
    if message.chat.type not in ["group", "supergroup"]:
        return

    text_lower = message.text.lower()
    for word in BANNED_WORDS:
        if word.lower() in text_lower:
            try:
                chat_title = message.chat.title or "مجموعة بدون اسم"
                user_name = message.from_user.full_name
                user_id = message.from_user.id
                user_username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد معرف"
                
                alert_text = (
                    f"🚨 **تم رصد طالب بحاجة لمساعدة!**\n\n"
                    f"📌 **المجموعة:** {chat_title}\n"
                    f"👤 **الطالب:** {user_name} ({user_username})\n"
                    f"🆔 **معرف الطالب (ID):** `{user_id}`\n"
                    f"💬 **الرسالة:** {message.text}"
                )
                
                # إرسال التنبيه لك على الخاص مباشرة
                await bot.send_message(ADMIN_ID, alert_text, parse_mode="Markdown")
                
            except Exception as e:
                logging.error(f"Failed to send alert: {e}")
            break

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
