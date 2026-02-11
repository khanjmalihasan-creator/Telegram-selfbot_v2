#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest

print("===== BOT STARTED =====", flush=True)

# ========== تنظیمات اجباری ==========
API_ID = 31266351
API_HASH = '0c86dc56c8937015b96c0f306e91fa05'
PHONE_NUMBER = '+989396612827'
# ====================================

# ========== لیست فحش‌های رکیک واقعی ==========
BAD_WORDS = [
    "کص ننت", "کیرم دهنت", "جنده", "کونی", "لاشی",
    "کص کش", "حرومزاده", "گاییدمت", "ننه جنده",
    "کصخل", "خارکصه", "تخم سگ", "پدر سوخته",
    "مادر جنده", "کیر تو کص ننت", "کص لیس",
    "بی ناموس", "مادر قهوه", "پدر سگ", "خواهر جنده",
    "کیر خر", "گاو", "الاغ", "حیوان", "کثافت",
    "گاییده شده", "کونی کصکش", "پدرسگ", "ننتو گاییدم",
    "کیرم تو اون صورتت", "کص ننت و جد و آبادت",
    "برو گمشو کصخل", "عقده ای", "پیف پاف",
    "کیر تو زندگی کصشعرت", "جاکش", "خائن",
    "کیر تو اون ننه کونیه ات", "کص ننش", "مادر سگ",
    "کیر تو اون پدر کونی ات", "برو بمیر", "برو گاییده شو",
    "کص ننت و اونایی که مثل تو هستن", "کونی زاده",
    "ننتو گاییدم کصکش", "کیر تو اون پدر و مادر عنی ات"
]

# ========== کلاس اصلی سلف بات ==========
class PersianSelfBot:
    def __init__(self):
        self.enemy_id = None
        self.enemy_name = None
        self.enemy_mode = False
        self.client = None
        
    async def start(self):
        """شروع سلف بات"""
        print("=" * 60)
        print("🔥 سلف بات فارسی - حالت دشمن فعال")
        print(f"📱 شماره: {PHONE_NUMBER}")
        print("=" * 60)
        
        try:
            from telethon.sessions import StringSession

session_string = os.getenv("SESSION")  # Session String از Variables Railway

self.client = TelegramClient(
    StringSession(session_string),  # استفاده از StringSession
    API_ID,
    API_HASH,
    device_model="PC",
    system_version="Linux",
    app_version="SelfBot v1.0"
)
            
            print("📡 در حال اتصال به تلگرام...")
            await self.client.start(phone=PHONE_NUMBER)
            
            me = await self.client.get_me()
            print(f"✅ متصل شدیم به: {me.first_name}")
            
            # شروع آپدیت ساعت (فقط عدد - بدون ایموجی)
            asyncio.create_task(self.update_time_only())
            
            # تنظیم هندلرها
            await self.setup_handlers()
            
            print("\n" + "=" * 50)
            print("🎯 سلف بات فعال شد!")
            print("📌 دستورات:")
            print("   • تنظیم دشمن (با ریپلای)")
            print("   • خاموش دشمن")
            print("   • وضعیت")
            print("=" * 50 + "\n")
            
            await self.client.run_until_disconnected()
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("تلاش مجدد...")
            await asyncio.sleep(5)
            await self.start()
    
    async def update_time_only(self):
        """آپدیت ساعت روی پروفایل - فقط عدد، بدون ایموجی، بدون بیوگرافی"""
        print("🕒 شروع آپدیت ساعت پروفایل...")
        
        while True:
            try:
                # زمان ایران
                iran_tz = pytz.timezone('Asia/Tehran')
                now = datetime.now(iran_tz)
                
                # فقط ساعت و دقیقه - بدون هیچ ایموجی یا علامت اضافه
                time_str = now.strftime('%H:%M')
                
                # آپدیت فقط اسم پروفایل - بیوگرافی دست نمی‌خوره
                await self.client(UpdateProfileRequest(
                    first_name=time_str,
                    about=None  # بیوگرافی تغییر نمی‌کنه
                ))
                
                print(f"✅ ساعت آپدیت شد: {time_str}")
                
            except Exception as e:
                print(f"⚠️ خطا در آپدیت ساعت: {e}")
            
            # هر 5 دقیقه آپدیت کن
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
            
            # ========== تنظیم دشمن ==========
            if event.text == 'تنظیم دشمن' and event.is_reply:
                reply = await event.get_reply_message()
                target = await reply.get_sender()
                
                self.enemy_id = target.id
                self.enemy_name = target.first_name or "کاربر"
                self.enemy_mode = True
                
                await event.reply(f"✅ دشمن تنظیم شد: {self.enemy_name}")
                print(f"🎯 دشمن تنظیم شد: {self.enemy_name}")
                return
            
            # ========== خاموش دشمن ==========
            if event.text == 'خاموش دشمن':
                self.enemy_mode = False
                self.enemy_id = None
                self.enemy_name = None
                await event.reply("✅ حالت دشمن خاموش شد")
                print("🟢 حالت دشمن خاموش شد")
                return
            
            # ========== وضعیت ==========
            if event.text == 'وضعیت':
                status = "فعال" if self.enemy_mode else "غیرفعال"
                enemy = self.enemy_name if self.enemy_mode else "ندارد"
                
                await event.reply(
                    f"📊 وضعیت سلف بات:\n\n"
                    f"🔥 حالت دشمن: {status}\n"
                    f"👤 دشمن فعلی: {enemy}\n"
                    f"🕒 ساعت پروفایل: فعال\n"
                    f"🌐 هاست: Railway"
                )
                return
            
            # ========== پاسخ به دشمن (فحش رکیک) ==========
            if self.enemy_mode and self.enemy_id and event.sender_id == self.enemy_id:
                # انتخاب فحش رکیک
                bad_word = random.choice(BAD_WORDS)
                
                # 80% شانس پاسخ
                if random.random() < 0.8:
                    await event.reply(bad_word)
                    print(f"🔥 فحش به دشمن: {bad_word[:20]}...")
                return
            
            # ========== پاسخ خودکار به پیام خصوصی ==========
            if event.is_private:
                # تأخیر 2-8 ثانیه
                await asyncio.sleep(random.uniform(2, 8))
                await event.reply("🔺به دلیل مشغله کاری و قطعی مکرر اینترنت ممکنه کمی با تاخیر جواب بگیرید")
                print(f"🤖 پاسخ خودکار به {sender.first_name}")

# ========== اجرای بات ==========
bot = PersianSelfBot()

async def main():
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 سلف بات متوقف شد.")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        time.sleep(5)
        asyncio.run(main())
