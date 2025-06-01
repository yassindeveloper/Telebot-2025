import time
import speedtest
import telebot
import psutil
from datetime import datetime

# ضع توكن البوت هنا
TOKEN = "7292861219:AAHGXONU73SJM7hnz0v0u8Z8QG8yhXH6E28"
CHAT_ID = "7699570274"

bot = telebot.TeleBot(TOKEN)

def analyze_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping

    # تحليل ذكي
    download_score = "✅ ممتاز" if download > 20 else "⚠️ ضعيف"
    upload_score = "✅ جيد" if upload > 5 else "⚠️ ضعيف"
    ping_score = "✅ ممتاز" if ping < 50 else "⚠️ عالي"

    # تحليل استهلاك النظام
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    # نقاط الضعف
    weaknesses = []
    if download < 10: weaknesses.append("❗ تنزيل ضعيف")
    if upload < 2: weaknesses.append("❗ رفع ضعيف")
    if ping > 100: weaknesses.append("❗ بنج مرتفع")
    if cpu > 85: weaknesses.append("🔻 استهلاك CPU مرتفع")
    if ram > 90: weaknesses.append("🔻 استهلاك RAM مرتفع")

    report = f"""📡 تقرير فحص الشبكة ({datetime.now().strftime('%H:%M:%S')}):

⬇️ التحميل: {download:.2f} Mbps — {download_score}
⬆️ الرفع: {upload:.2f} Mbps — {upload_score}
📶 البنغ: {ping:.2f} ms — {ping_score}

🖥️ CPU: {cpu:.1f}%
💾 RAM: {ram:.1f}%

🔍 تحليل:
{chr(10).join(weaknesses) if weaknesses else '✅ لا توجد مشاكل واضحة'}
    """
    return report


# ⏱️ التكرار كل دقيقتين
while True:
    try:
        result = analyze_speed()
        bot.send_message(CHAT_ID, result)
        time.sleep(120)  # كل دقيقتين
    except Exception as e:
        bot.send_message(CHAT_ID, f"حدث خطأ أثناء الفحص:\n{str(e)}")
        time.sleep(60)
