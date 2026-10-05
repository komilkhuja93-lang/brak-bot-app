import os
from flask import Flask, request, render_template
import telebot
from telebot.types import InputMediaPhoto
import os

# Botingiz tokeni va Test guruhingiz ID sini shu yerga yozasiz
BOT_TOKEN = '8902395002:AAG_5XzbDYMb2qygzVjbweiwvDaCPoNiBeU'
GROUP_CHAT_ID = '-1003984278331' # Test guruh ID sini yozing

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Web App'dan kelgan ma'lumotlarni qabul qilib olish
    xodim = request.form.get('xodim')
    artikul = request.form.get('artikul')
    nomi = request.form.get('nomi')
    gofra = request.form.get('gofra')
    printer = request.form.get('printer')
    stepler = request.form.get('stepler')
    izoh = request.form.get('izoh')
    photos = request.files.getlist('photos')

    # Guruhga yuboriladigan chiroyli shablon (Text)
    caption_text = f"📋 <b>Brak mahsulot hisoboti</b>\n\n"
    caption_text += f"📦 <b>Mahsulot artikuli:</b> {artikul}\n"
    caption_text += f"🏷 <b>Mahsulot nomi:</b> {nomi}\n\n"
    caption_text += f"📉 <b>Gofra Brak:</b> {gofra} dona.\n"
    caption_text += f"🖨 <b>Printer Brak:</b> {printer} dona.\n"
    caption_text += f"📎 <b>Stepler Brak:</b> {stepler} dona.\n\n"
    
    if izoh:
        caption_text += f"📝 <b>Izoh:</b> {izoh}\n\n"
        
    caption_text += f"👤 <b>Yubordi:</b> {xodim}"

    # Rasmlarni Telegramga jo'natish uchun tayyorlash
    media_group = []
    for index, photo in enumerate(photos):
        # Faylni o'qish
        photo_bytes = photo.read()
        # Faqat birinchi rasmning tagiga tekstni (shablonni) qo'shamiz
        if index == 0:
            media_group.append(InputMediaPhoto(photo_bytes, caption=caption_text, parse_mode='HTML'))
        else:
            media_group.append(InputMediaPhoto(photo_bytes))

    try:
        # Guruhga rasmlar va tekstni bitta post qilib tashlash
        bot.send_media_group(chat_id=GROUP_CHAT_ID, media=media_group)
        return "Yuborildi", 200
    except Exception as e:
        print(f"Xatolik: {e}")
        return "Xato", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)