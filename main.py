#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# سلف بات فارسی - نسخه Railway
# GitHub: telegram-selfbot-v2

import os
import sys
import time
import random
import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest

print("=" * 60)
print("🤖 سلف بات فارسی در حال راه‌اندازی...")
print("=" * 60)

# تنظیمات از Variables
API_ID = int(os.getenv('API_ID', 31266351))
API_HASH = os.getenv('API_HASH', '0c86dc56c8937015b96c0f306e91fa05')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+989396612827')

# نمایش تنظیمات
print(f"📱 شماره: {PHONE_NUMBER}")
print(f"🆔 API ID: {API_ID}")
print(f"🔑 API Hash: {API_HASH[:10]}...")

# دیتای سلف بات
class SelfBot:
    def __init__(self):
        self.enemy_id = None
        self.enemy_name = None
        self.enemy_mode = False
        self.client = None
        
        # فحش‌های رکیک
        self.bad_words = [
            "کص ننت", "کیرم دهنت", "جنده", "کونی", "لاشی",
            "کص کش", "حروم زاده", "گاییدمت", "ننه جنده",
            "کص خل", "خارکصه", "تخم سگ", "بی ناموس"
        ]
    
    async def start(self):
        """شروع سلف بات"""
        try:
            # ساخت کلاینت
            self.client = TelegramClient(
    'session',
                API_ID,
                API_HASH,
                device_model="iPhone 15 Pro",
                system_version="iOS 17.0",
                app_version="Telegram iOS 10.0"
            )
            
            # اتصال
            print("📡 در حال اتصال به تلگرام...")
            await self.client.start(phone=PHONE_NUMBER)
            
            # اطلاعات کاربر
            me = await self.client.get_me()
            print(f"✅ متصل شدیم به: {me.first_name}")
            print(f"👤 یوزرنیم: @{me.username}")
            
            # شروع وظایف
            asyncio.create_task(self.update_profile_time())
            
            # هندلرها
            await self.setup_handlers()
            
            print("\n" + "=" * 50)
            print("🎯 سلف بات فعال شد!")
            print("📌 دستورات:")
            print("   تنظیم دشمن (با ریپلای)")
            print("   خاموش دشمن")
            print("   وضعیت")
            print("=" * 50 + "\n")
            
            # اجرای دائمی
            await self.client.run_until_disconnected()
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("تلاش مجدد در 10 ثانیه...")
            time.sleep(10)
            await self.start()
    
    async def update_profile_time(self):
        """آپدیت تایم ایران روی پروفایل"""
        print("🕒 شروع آپدیت زمان پروفایل...")
        
        while True:
            try:
                # زمان ایران
                iran_tz = pytz.timezone('Asia/Tehran')
                now = datetime.now(iran_tz)
                
                # فرمت زمان
                time_str = f"🕒 {now.strftime('%H:%M')} تهران"
                
                # آپدیت پروفایل
                await self.client(UpdateProfileRequest(
                    first_name=time_str,
                    about="🔺به دلیل مشغله کاری و قطعی مکرر اینترنت ممکنه کمی با تاخیر جواب بگیرید"
                ))
                
                print(f"✅ پروفایل آپدیت شد: {time_str}")
                
            except Exception as e:
                print(f"⚠️ خطا در آپدیت پروفایل: {e}")
            
            # هر 5 دقیقه
            await asyncio.sleep(300)
    
    async def setup_handlers(self):
        """تنظیم هندلرهای رویداد"""
        
        @self.client.on(events.NewMessage(incoming=True))
        async def handler(event):
            # خودم نباشم
            if event.sender_id == (await self.client.get_me()).id:
                return
            
            sender = await event.get_sender()
            print(f"📨 پیام از {sender.first_name}: {event.text[:30]}...")
            
            # تنظیم دشمن
            if event.text == 'تنظیم دشمن' and event.is_reply:
                reply = await event.get_reply_message()
                target = await reply.get_sender()
                
                self.enemy_id = target.id
                self.enemy_name = target.first_name or "کاربر"
                self.enemy_mode = True
                
                await event.reply(f"✅ دشمن تنظیم شد!\n👤: {self.enemy_name}")
                print(f"🎯 دشمن تنظیم شد: {self.enemy_name}")
                return
            
            # خاموش دشمن
            if event.text == 'خاموش دشمن':
                self.enemy_mode = False
                await event.reply("✅ حالت دشمن خاموش شد")
                print("🟢 حالت دشمن خاموش شد")
                return
            
            # وضعیت
            if event.text == 'وضعیت':
                status = "فعال ✅" if self.enemy_mode else "غیرفعال ⭕"
                enemy = self.enemy_name if self.enemy_mode else "ندارد"
                
                await event.reply(
                    f"📊 وضعیت:\n\n"
                    f"🔥 حالت دشمن: {status}\n"
                    f"👤 دشمن: {enemy}\n"
                    f"🕒 تایم ایران: فعال\n"
                    f"📡 هاست: Railway"
                )
                return
            
            # پاسخ به دشمن
            if self.enemy_mode and event.sender_id == self.enemy_id:
                bad_word = random.choice(self.bad_words)
                emoji = random.choice(["🔥", "⚡", "💢"])
                await event.reply(f"{emoji} {bad_word} {emoji}")
                print(f"🔥 به دشمن جواب دادم: {bad_word}")
                return
            
            # پاسخ خودکار به پیام خصوصی
            if event.is_private:
                await asyncio.sleep(random.uniform(2, 6))
                await event.reply("🔺به دلیل مشغله کاری و قطعی مکرر اینترنت ممکنه کمی با تاخیر جواب بگیرید")
                print(f"🤖 پاسخ خودکار به {sender.first_name}")

# ساخت و اجرای بات
bot = SelfBot()

async def main():
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 سلف بات متوقف شد.")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        time.sleep(10)
        asyncio.run(main())
