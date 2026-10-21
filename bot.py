import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Fetch the token from Railway Variables
TOKEN = os.environ.get("TOKEN")

# Check if token exists before starting
if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("==================================================")
    print("ERROR: TOKEN is missing!")
    print("Please go to Railway -> Variables and add:")
    print("Name: TOKEN")
    print("Value: (your BotFather token)")
    print("==================================================")
    sys.exit(1) # This stops the app

STYLES = {
    "stiletto": "👠 Stilettos\n\nClassic thin high heel, 3–4 inches.\nBest for: formal events, evenings, parties.\nComfort: low.",
    "kitten": "👠 Kitten Heels\n\nLow heel, 1.5–2 inches.\nBest for: office, beginners, long wear.\nComfort: high.",
    "block": "👠 Block Heels\n\nThick heel, stable, 2–3.5 inches.\nBest for: daily commute, casual outings.\nComfort: medium-high.",
    "wedge": "👠 Wedges\n\nContinuous sole, stable.\nBest for: outdoor, summer.\nComfort: medium-high.",
    "pump": "👠 Pumps\n\nClosed-toe classic, 2–3.5 inches.\nBest for: work, formal occasions.\nComfort: medium.",
    "mule": "👠 Mules\n\nBackless, easy to slip on.\nBest for: social occasions.\nComfort: medium.",
}

HEIGHT_GUIDE = {
    "2": "📏 2 inches and below: beginner-friendly, suitable for daily wear.",
    "3": "📏 3 inches: most common height, suitable for office and events.",
    "4": "📏 4 inches: requires experience, not for long walking.",
    "5": "📏 5 inches and above: professional level, short wear only.",
}

OCCASION = {
    "work": "🎯 Workplace: recommend kitten heels or block heels (2–3 inches).",
    "date": "🎯 Date: recommend pumps or mules (2–3 inches).",
    "wedding": "🎯 Wedding: recommend stilettos or pumps (3–4 inches).",
    "party": "🎯 Party: recommend stilettos or block heels (3–4 inches).",
}

COMFORT_TIPS = "🦶 Comfort Tips\n\n• Continuous heel height over 1.5 inches is not recommended for long periods.\n• Alternate with flat shoes.\n• Choose block heels for stability."
WELCOME_TEXT = "Welcome! 👋\nI provide info about women's high heels.\n\nChoose an option below:"

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👠 Heel styles", callback_data="menu_styles")],
        [InlineKeyboardButton("📏 Heel height", callback_data="menu_height")],
        [InlineKeyboardButton("🎯 Occasion", callback_data="menu_occasion")],
        [InlineKeyboardButton("🦶 Comfort tips", callback_data="menu_tips")],
    ])

def styles_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Stilettos", callback_data="style_stiletto")],
        [InlineKeyboardButton("Kitten Heels", callback_data="style_kitten")],
        [InlineKeyboardButton("Block Heels", callback_data="style_block")],
        [InlineKeyboardButton("Wedges", callback_data="style_wedge")],
        [InlineKeyboardButton("Pumps", callback_data="style_pump")],
        [InlineKeyboardButton("Mules", callback_data="style_mule")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def height_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("2 inches", callback_data="height_2")],
        [InlineKeyboardButton("3 inches", callback_data="height_3")],
        [InlineKeyboardButton("4 inches", callback_data="height_4")],
        [InlineKeyboardButton("5 inches+", callback_data="height_5")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def occasion_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Work", callback_data="occ_work")],
        [InlineKeyboardButton("Date", callback_data="occ_date")],
        [InlineKeyboardButton("Wedding", callback_data="occ_wedding")],
        [InlineKeyboardButton("Party", callback_data="occ_party")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to menu", callback_data="back_main")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_styles":
        await query.edit_message_text("Choose a heel style:", reply_markup=styles_menu())
    elif data == "menu_height":
        await query.edit_message_text("Choose a heel height:", reply_markup=height_menu())
    elif data == "menu_occasion":
        await query.edit_message_text("Choose an occasion:", reply_markup=occasion_menu())
    elif data == "menu_tips":
        await query.edit_message_text(COMFORT_TIPS, reply_markup=back_menu())
    elif data.startswith("style_"):
        await query.edit_message_text(STYLES[data.replace("style_", "")], reply_markup=back_menu())
    elif data.startswith("height_"):
        await query.edit_message_text(HEIGHT_GUIDE[data.replace("height_", "")], reply_markup=back_menu())
    elif data.startswith("occ_"):
        await query.edit_message_text(OCCASION[data.replace("occ_", "")], reply_markup=back_menu())
    elif data == "back_main":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu())

def main():
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running and polling Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
