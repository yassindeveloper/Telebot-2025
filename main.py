import telebot
import speedtest
import matplotlib.pyplot as plt
import psutil
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv("7292861219:AAHGXONU73SJM7hnz0v0u8Z8QG8yhXH6E28")
CHAT_ID = os.getenv("7699570274")

bot = telebot.TeleBot(BOT_TOKEN)

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping
    return round(download_speed, 2), round(upload_speed, 2), round(ping, 2)

def analyze_network():
    download, upload, ping = test_speed()
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    # رسم بياني
    labels = ["Download", "Upload", "Ping", "CPU %", "RAM %"]
    values = [download, upload, ping, cpu, ram]
    colors = ["blue", "green", "red", "orange", "purple"]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color=colors)
    plt.title(f"Network Analysis - {datetime.now().strftime('%H:%M:%S')}")
    plt.ylim(0, max(values) + 10)
    plt.tight_layout()
    chart_file = "chart.png"
    plt.savefig(chart_file)
    plt.close()

    summary = f"""<b>Network Report</b>
⬇️ Download: {download} Mbps
⬆️ Upload: {upload} Mbps
🏓 Ping: {ping} ms
🧠 CPU: {cpu}%
💾 RAM: {ram}%
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    with open(chart_file, "rb") as photo:
        bot.send_photo(CHAT_ID, photo, caption=summary, parse_mode="HTML")

if __name__ == "__main__":
    while True:
        try:
            analyze_network()
        except Exception as e:
            bot.send_message(CHAT_ID, f"❌ Error: {str(e)}")
        time.sleep(120)  # كل دقيقتين
