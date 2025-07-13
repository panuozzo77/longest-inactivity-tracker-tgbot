import datetime
from functools import wraps
from typing import Callable

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

def admin_only(func: Callable) -> Callable:
    """A decorator to restrict command access to group administrators."""
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.message or not update.message.from_user:
            return
        
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id

        # Admins have all permissions in private chats
        if update.message.chat.type == 'private':
            return await func(update, context, *args, **kwargs)

        administrators = await context.bot.get_chat_administrators(chat_id)
        is_admin = any(admin.user.id == user_id for admin in administrators)

        if is_admin:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("You must be an admin to use this command.")
    return wrapped

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes every message to track inactivity."""
    if not update.message or not update.message.date or not update.message.from_user:
        return

    group_id = update.message.chat_id
    timestamp = update.message.date.timestamp()
    user = update.message.from_user
    user_info = {"id": user.id, "name": user.full_name}

    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    config_service: ConfigService = context.bot_data["config_service"]

    result = inactivity_service.update_inactivity(group_id, timestamp, user_info)

    if result and config_service.is_announcement_enabled(group_id):
        new_record, last_user_info = result
        
        # Create markdown links to tag users
        last_user_mention = f"[{last_user_info['name']}](tg://user?id={last_user_info['id']})"
        current_user_mention = f"[{user_info['name']}](tg://user?id={user_info['id']})"

        await update.message.reply_text(
            f"🎉 **New Inactivity Record!** 🎉\n\n"
            f"A new record of **{format_duration(new_record)}** has been set.\n\n"
            f"The last message was from {last_user_mention}.\n"
            f"The silence was broken by {current_user_mention}.",
            parse_mode='Markdown'
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

@admin_only
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
        "/seed <minutes> - Set an initial record to prevent initial spam.\n"
        "/leaderboard - Show the leaderboard for record setters.\n"
        "/history - Show the last 5 records.\n"
        "/clean - Reset all stats for this group.\n"
        "/help - Show this help message."
    )

@admin_only
async def seed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /seed command to set an initial record."""
    if not update.message:
        return
        
    if not context.args:
        await update.message.reply_text("Please provide the initial record time in minutes.\nUsage: /seed <minutes>")
        return

    try:
        minutes = int(context.args[0])
        if minutes <= 0:
            raise ValueError
        
        seed_value = minutes * 60.0
        group_id = update.message.chat_id
        inactivity_service: InactivityService = context.bot_data["inactivity_service"]
        inactivity_service.seed_record(group_id, seed_value)

        await update.message.reply_text(
            f"✅ Initial record has been set to {format_duration(seed_value)}."
        )
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid input. Please provide a positive number of minutes.\nUsage: /seed <minutes>")

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /leaderboard command."""
    if not update.message:
        return
    group_id = update.message.chat_id
    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    leaderboards = inactivity_service.get_leaderboards(group_id)

    response = "🏆 **Leaderboards** 🏆\n\n"

    for board_name, board_data in leaderboards.items():
        title = "🗣️ Last Word Champions" if board_name == "last_word" else "🤫 Silence Breakers"
        response += f"**{title}**\n"
        
        if not board_data:
            response += "No records yet.\n\n"
            continue

        sorted_board = sorted(board_data.items(), key=lambda item: item[1]['score'], reverse=True)
        
        for i, (user_id, data) in enumerate(sorted_board[:5]):
            response += f"{i+1}. {data['name']} - {data['score']} times\n"
        response += "\n"

    await update.message.reply_text(response, parse_mode='Markdown')

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /history command."""
    if not update.message:
        return
    group_id = update.message.chat_id
    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    history = inactivity_service.get_history(group_id)

    if not history:
        await update.message.reply_text("No record history yet.")
        return

    response = "📜 **Record History (Last 5)** 📜\n\n"
    for entry in reversed(history[-5:]):
        timestamp = datetime.datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
        duration = format_duration(entry['record_seconds'])
        breaker_name = entry['breaker_user']['name']
        last_user_name = entry['last_user']['name']
        response += f"**{duration}** on {timestamp}\n"
        response += f"- Set by: {breaker_name} (broke the silence from {last_user_name})\n\n"

    await update.message.reply_text(response, parse_mode='Markdown')

@admin_only
async def clean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /clean command to reset all group stats."""
    if not update.message:
        return
    
    group_id = update.message.chat_id
    inactivity_service: InactivityService = context.bot_data["inactivity_service"]
    inactivity_service.clean_stats(group_id)
    
    await update.message.reply_text("🧹 All stats for this group have been reset.")