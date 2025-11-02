import panel as pn
import requests
import datetime

pn.extension(sizing_mode="stretch_width")

BOT_TOKEN = pn.widgets.PasswordInput(name="🤖 Bot Token", placeholder="Enter your Telegram Bot Token...")
CHAT_ID = pn.widgets.TextInput(name="💬 Chat ID", placeholder="Enter Chat ID to send message")
MESSAGE = pn.widgets.TextAreaInput(name="📝 Message", placeholder="Type your message here...", height=100)
status = pn.pane.Markdown("### Bot Status: ❌ Not Running")
log_box = pn.pane.Markdown("### 📜 Logs:\n")

is_running = False

def log(message):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    log_box.object += f"\n`[{time}]` {message}"

def start_bot(event):
    global is_running
    is_running = True
    status.object = "### ✅ Bot Status: Running"
    log("Bot started successfully ✅")

def stop_bot(event):
    global is_running
    is_running = False
    status.object = "### 🛑 Bot Status: Stopped"
    log("Bot stopped manually 🛑")

def restart_bot(event):
    stop_bot(event)
    start_bot(event)
    log("Bot restarted 🔁")

def bot_info(event):
    token = BOT_TOKEN.value.strip()
    if not token:
        status.object = "⚠️ Please enter your Bot Token!"
        return
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        r = requests.get(url).json()
        if r.get("ok"):
            info = r["result"]
            text = f"### 🤖 Bot Info\n**Name:** {info['first_name']}\n**Username:** @{info['username']}\n**ID:** {info['id']}"
            status.object = text
            log("Fetched bot info successfully ℹ️")
        else:
            status.object = f"❌ Invalid Token or Error: {r}"
            log("Failed to fetch bot info ❌")
    except Exception as e:
        status.object = f"⚠️ Error: {e}"
        log(f"Error while fetching info: {e}")

def send_message(event):
    token = BOT_TOKEN.value.strip()
    chat_id = CHAT_ID.value.strip()
    text = MESSAGE.value.strip()
    if not token or not chat_id or not text:
        log("⚠️ Please fill all fields before sending.")
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        r = requests.post(url, data=data).json()
        if r.get("ok"):
            log(f"📤 Message sent to {chat_id}")
        else:
            log(f"❌ Failed to send message: {r}")
    except Exception as e:
        log(f"⚠️ Error sending message: {e}")

start_btn = pn.widgets.Button(name="▶️ Start Bot", button_type="success")
stop_btn = pn.widgets.Button(name="⏹ Stop Bot", button_type="danger")
restart_btn = pn.widgets.Button(name="🔁 Restart", button_type="warning")
info_btn = pn.widgets.Button(name="ℹ️ Bot Info", button_type="primary")
send_btn = pn.widgets.Button(name="📨 Send Message", button_type="primary")

start_btn.on_click(start_bot)
stop_btn.on_click(stop_bot)
restart_btn.on_click(restart_bot)
info_btn.on_click(bot_info)
send_btn.on_click(send_message)

header = pn.pane.Markdown("# 💻 MarufVai Advanced Telegram Panel", style={"font-size": "22px"})
control_row = pn.Row(start_btn, stop_btn, restart_btn, info_btn)
send_section = pn.Column("### ✉️ Message Sender", CHAT_ID, MESSAGE, send_btn)
main_panel = pn.Column(
    header,
    BOT_TOKEN,
    control_row,
    status,
    send_section,
    log_box,
    sizing_mode="stretch_width",
)

main_panel.servable()
