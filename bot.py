"""
High Heel Information Bot
A Telegram bot that provides information about women's high heel styles,
heel heights, occasion styling, and comfort tips.

Setup:
1. Get a token from @BotFather
2. Replace YOUR_BOT_TOKEN_HERE below with your token
3. pip install -r requirements.txt
4. python bot.py
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# REPLACE THIS WITH YOUR TOKEN FROM @BotFather
# ============================================================
TOKEN = "YOUR_BOT_TOKEN_HERE"


# ============================================================
# CONTENT DATA
# ============================================================

STYLES = {
    "stiletto": (
        "👠 Stilettos\n\n"
        "Classic thin high heel, usually 3–4 inches or higher.\n\n"
        "Best for: formal events, evenings, parties.\n"
        "Comfort: low — not ideal for long walking.\n"
        "Stability: low — requires practice."
    ),
    "kitten": (
        "👠 Kitten Heels\n\n"
        "Low heel, only 1.5–2 inches.\n\n"
        "Best for: office, beginners, long wear.\n"
        "Comfort: high.\n"
        "Stability: high — easiest to walk in."
    ),
    "block": (
        "👠 Block Heels\n\n"
        "Thick heel, stable and easy to walk in, 2–3.5 inches.\n\n"
        "Best for: daily commute, casual outings, long days.\n"
        "Comfort: medium-high.\n"
        "Stability: high."
    ),
    "wedge": (
        "👠 Wedges\n\n"
        "Continuous sole, more stable than thin heels.\n\n"
        "Best for: outdoor, summer, casual events.\n"
        "Comfort: medium-high.\n"
        "Stability: high."
    ),
    "pump": (
        "👠 Pumps\n\n"
        "Closed-toe classic, 2–3.5 inches.\n\n"
        "Best for: work, formal occasions, interviews.\n"
        "Comfort: medium.\n"
        "Stability: medium."
    ),
    "mule": (
        "👠 Mules\n\n"
        "Backless, easy to slip on and off.\n\n"
        "Best for: social occasions, quick outings.\n"
        "Comfort: medium.\n"
        "Stability: medium — heel can slip off."
    ),
}

HEIGHT_GUIDE = {
    "2": (
        "📏 2 inches (5 cm) and below\n\n"
        "Level: beginner-friendly.\n"
        "Suitable for: daily wear, office, long walking.\n"
        "Tip: the safest choice if you are new to heels."
    ),
    "3": (
        "📏 3 inches (7.5 cm)\n\n"
        "Level: most common height.\n"
        "Suitable for: office, events, dinners.\n"
        "Tip: a good balance of style and comfort."
    ),
    "4": (
        "📏 4 inches (10 cm)\n\n"
        "Level: requires some high heel experience.\n"
        "Suitable for: parties, short events.\n"
        "Tip: not recommended for long walking or standing."
    ),
    "5": (
        "📏 5 inches (12.5 cm) and above\n\n"
        "Level: professional / experienced wearers.\n"
        "Suitable for: photos, short formal events.\n"
        "Tip: bring flat shoes for backup."
    ),
}

OCCASION = {
    "work": (
        "🎯 Workplace\n\n"
        "Recommended: kitten heels or block heels (2–3 inches).\n"
        "Pair with: ankle-length pants, midi skirts, tailored dresses.\n"
        "Avoid: stilettos over 4 inches for all-day wear."
    ),
    "date": (
        "🎯 Date\n\n"
        "Recommended: pumps or mules (2–3 inches).\n"
        "Pair with: dresses, slim jeans, skirts.\n"
        "Tip: choose a style you can walk in comfortably."
    ),
    "wedding": (
        "🎯 Wedding\n\n"
        "Recommended: stilettos or pumps (3–4 inches).\n"
        "Pair with: formal dresses, gowns.\n"
        "Tip: bring flat shoes for backup — weddings are long."
    ),
    "party": (
        "🎯 Party\n\n"
        "Recommended: stilettos or block heels (3–4 inches).\n"
        "Pair with: evening wear, statement outfits.\n"
        "Tip: block heels are easier if you plan to dance."
    ),
}

COMFORT_TIPS = (
    "🦶 Comfort Tips\n\n"
    "• Continuous heel height over 4 cm (~1.5 inches) is not recommended for long periods.\n"
    "• Alternate with flat shoes if you wear heels all day.\n"
    "• Choose block or wedge heels when you need stability.\n"
    "• Take short breaks and stretch your feet.\n"
    "• These are general tips, not medical advice."
)

WELCOME_TEXT = (
    "Welcome! 👋\n\n"
    "I provide information about women's high heels: styles, heel heights, "
    "occasion styling, and comfort tips.\n\n"
    "Choose an option below:"
)


# ============================================================
# KEYBOARDS
# ============================================================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("👠 Heel styles", callback_data="menu_styles")],
        [InlineKeyboardButton("📏 Heel height guide", callback_data="menu_height")],
        [InlineKeyboardButton("🎯 Occasion styling", callback_data="menu_occasion")],
        [InlineKeyboardButton("🦶 Comfort tips", callback_data="menu_tips")],
    ]
    return InlineKeyboardMarkup(keyboard)


def styles_menu():
    keyboard = [
        [InlineKeyboardButton("Stilettos", callback_data="style_stiletto")],
        [InlineKeyboardButton("Kitten Heels", callback_data="style_kitten")],
        [InlineKeyboardButton("Block Heels", callback_data="style_block")],
        [InlineKeyboardButton("Wedges", callback_data="style_wedge")],
        [InlineKeyboardButton("Pumps", callback_data="style_pump")],
        [InlineKeyboardButton("Mules", callback_data="style_mule")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def height_menu():
    keyboard = [
        [InlineKeyboardButton("2 inches or below", callback_data="height_2")],
        [InlineKeyboardButton("3 inches", callback_data="height_3")],
        [InlineKeyboardButton("4 inches", callback_data="height_4")],
        [InlineKeyboardButton("5 inches and above", callback_data="height_5")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def occasion_menu():
    keyboard = [
        [InlineKeyboardButton("Work", callback_data="occ_work")],
        [InlineKeyboardButton("Date", callback_data="occ_date")],
        [InlineKeyboardButton("Wedding", callback_data="occ_wedding")],
        [InlineKeyboardButton("Party", callback_data="occ_party")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back to menu", callback_data="back_main")]]
    )


# ============================================================
# HANDLERS
# ============================================================

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
        key = data.replace("style_", "")
        await query.edit_message_text(STYLES[key], reply_markup=back_menu())

    elif data.startswith("height_"):
        key = data.replace("height_", "")
        await query.edit_message_text(HEIGHT_GUIDE[key], reply_markup=back_menu())

    elif data.startswith("occ_"):
        key = data.replace("occ_", "")
        await query.edit_message_text(OCCASION[key], reply_markup=back_menu())

    elif data == "back_main":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu())


# ============================================================
# MAIN
# ============================================================

def main():
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("ERROR: You must replace YOUR_BOT_TOKEN_HERE with your real token from @BotFather")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
