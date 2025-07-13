import datetime

from telegram import Update
from telegram.ext import ContextTypes

from ..services.config_service import ConfigService
from ..services.inactivity_service import InactivityService

def format_duration(seconds: float) -> str:
    """Converts a duration in seconds to a human-readable string."""
    delta = datetime.timedelta(seconds=seconds)
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    return ", ".join(parts)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes every message to track inactivity."""
    if not update.message or not update.message.date:
        return

    group_id = update.message.chat_id
    timestamp = update.message.date.timestamp()

    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    config_service: ConfigService = context.bot_data["config_service"]

    new_record = inactivity_service.update_inactivity(group_id, timestamp)

    if new_record is not None and config_service.is_announcement_enabled(group_id):
        await update.message.reply_text(
            f"🎉 New inactivity record! 🎉\n\n"
            f"The new record is {format_duration(new_record)}."
        )

async def record_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /record command."""
    if not update.message:
        return
    group_id = update.message.chat_id
    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    
    current_record = inactivity_service.get_current_record(group_id)
    
    await update.message.reply_text(
        f"The current inactivity record for this group is:\n"
        f"{format_duration(current_record)}"
    )

async def toggle_announcements_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /toggle_announcements command."""
    if not update.message:
        return
    group_id = update.message.chat_id
    config_service: ConfigService = context.bot_data["config_service"]

    new_state = config_service.toggle_announcements(group_id)
    status = "✅ Enabled" if new_state else "❌ Disabled"
    
    await update.message.reply_text(
        f"📢 New record announcements are now {status} for this group."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    if not update.message:
        return
    await update.message.reply_text(
        "Available commands:\n"
        "/record - Show the current inactivity record.\n"
        "/toggle_announcements - Enable or disable new record announcements.\n"
        "/seed - Set an initial record of 10 minutes to prevent initial spam.\n"
        "/help - Show this help message."
    )

async def seed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /seed command to set an initial record."""
    if not update.message:
        return
    group_id = update.message.chat_id
    inactivity_service: InactivityService = context.bot_data["inactivity_service"]

    # Seed with 10 minutes (600 seconds)
    seed_value = 600.0
    inactivity_service.seed_record(group_id, seed_value)

    await update.message.reply_text(
        f"✅ Initial record has been set to {format_duration(seed_value)}."
    )