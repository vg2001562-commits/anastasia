# manicure_bot.py - ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ==================== НАСТРОЙКИ ====================
# ВСТАВЬТЕ ВАШ ТОКЕН СЮДА (получите у @BotFather)
BOT_TOKEN = "7955420179:AAHd4851TNv3aLH8mv8gKcgSm4qS7mAGmCs"  # ЗАМЕНИТЕ НА ВАШ ТОКЕН!

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ==================== СОСТОЯНИЯ ====================
class ManicureForm(StatesGroup):
    waiting_for_length = State()
    waiting_for_shape = State()
    waiting_for_color = State()
    waiting_for_occasion = State()

# ==================== ДАННЫЕ ====================
STYLES = {
    "french": {
        "name": "💅 Классический френч",
        "desc": "Белый кончик на натуральном фоне. Элегантно и универсально.",
        "techniques": "френч, линии",
        "colors": "белый, розовый, бежевый"
    },
    "ombre": {
        "name": "🌈 Омбре",
        "desc": "Плавный переход цвета. Стильно и современно.",
        "techniques": "омбре, градиент",
        "colors": "пастельные, розовый, синий"
    },
    "glitter": {
        "name": "✨ Глиттер",
        "desc": "Сверкающий дизайн с блестками. Идеально для праздников.",
        "techniques": "блестки, стразы",
        "colors": "золото, серебро, розовое золото"
    },
    "matte": {
        "name": "🎨 Матовый",
        "desc": "Бархатистая текстура без блеска. Выглядит дорого.",
        "techniques": "матовый топ",
        "colors": "все оттенки"
    },
    "minimalism": {
        "name": "✨ Минимализм",
        "desc": "Лаконичный дизайн с линиями и точками.",
        "techniques": "геометрия, линии",
        "colors": "черный, белый, нюд"
    },
    "cat_eye": {
        "name": "🐱 Кошачий глаз",
        "desc": "Магнитный лак с эффектом перелива.",
        "techniques": "магнитный лак",
        "colors": "синий, фиолетовый, бордовый"
    }
}

# Правила подбора
MATCHES = {
    "french": {"length": ["короткие", "средние"], "shape": ["квадратные", "овальные"], "color": ["нюдовые"], "occasion": ["на каждый день", "работа"]},
    "ombre": {"length": ["средние", "длинные"], "shape": ["миндалевидные", "овальные"], "color": ["пастельные", "яркие"], "occasion": ["вечеринка", "свидание"]},
    "glitter": {"length": ["средние", "длинные"], "shape": ["миндалевидные"], "color": ["блестки"], "occasion": ["вечеринка", "свадьба"]},
    "matte": {"length": ["короткие", "средние"], "shape": ["квадратные", "миндалевидные"], "color": ["темные", "нюдовые"], "occasion": ["на каждый день", "работа"]},
    "minimalism": {"length": ["короткие", "средние"], "shape": ["квадратные", "круглые"], "color": ["черный", "белый"], "occasion": ["на каждый день"]},
    "cat_eye": {"length": ["средние", "длинные"], "shape": ["миндалевидные"], "color": ["темные"], "occasion": ["вечеринка", "свидание"]}
}

# ==================== КЛАВИАТУРЫ ====================
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Подобрать стиль", callback_data="select")],
        [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="💡 Советы", callback_data="tips")]
    ])

def length_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✂️ Короткие", callback_data="len_короткие")],
        [InlineKeyboardButton(text="📏 Средние", callback_data="len_средние")],
        [InlineKeyboardButton(text="✨ Длинные", callback_data="len_длинные")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])

def shape_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬛ Квадратные", callback_data="shape_квадратные")],
        [InlineKeyboardButton(text="⚪ Овальные", callback_data="shape_овальные")],
        [InlineKeyboardButton(text="🌰 Миндалевидные", callback_data="shape_миндалевидные")],
        [InlineKeyboardButton(text="🔘 Круглые", callback_data="shape_круглые")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_length")]
    ])

def color_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌸 Пастельные", callback_data="color_пастельные")],
        [InlineKeyboardButton(text="🎨 Яркие", callback_data="color_яркие")],
        [InlineKeyboardButton(text="🌙 Темные", callback_data="color_темные")],
        [InlineKeyboardButton(text="👑 Нюдовые", callback_data="color_нюдовые")],
        [InlineKeyboardButton(text="✨ Блестки", callback_data="color_блестки")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_shape")]
    ])

def occasion_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 На каждый день", callback_data="occ_на каждый день")],
        [InlineKeyboardButton(text="💼 Для работы", callback_data="occ_работа")],
        [InlineKeyboardButton(text="🎉 Вечеринка", callback_data="occ_вечеринка")],
        [InlineKeyboardButton(text="💕 Свидание", callback_data="occ_свидание")],
        [InlineKeyboardButton(text="💍 Свадьба", callback_data="occ_свадьба")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_color")]
    ])

# ==================== КОМАНДЫ ====================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "💅 <b>Добро пожаловать!</b>\n\n"
        "Я помогу подобрать идеальный стиль маникюра.\n"
        "Учту ваши предпочтения по длине, форме, цвету и поводу.\n\n"
        "👇 <b>Нажмите на кнопку ниже</b>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "❓ <b>Помощь</b>\n\n"
        "/start - начать работу\n"
        "/help - эта справка\n\n"
        "📝 <b>Как подобрать стиль:</b>\n"
        "1. Нажмите 'Подобрать стиль'\n"
        "2. Выберите длину ногтей\n"
        "3. Выберите форму\n"
        "4. Выберите цвет\n"
        "5. Выберите повод\n\n"
        "Бот подберет подходящие варианты!",
        parse_mode="HTML"
    )

# ==================== ОБРАБОТЧИКИ ====================
@dp.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    
    # Главное меню
    if data == "select":
        await state.clear()
        await callback.message.edit_text(
            "💅 Выберите <b>длину ногтей</b>:",
            reply_markup=length_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_length)
    
    elif data == "catalog":
        text = "<b>📖 Каталог стилей</b>\n\n"
        for key, style in STYLES.items():
            text += f"{style['name']}\n"
            text += f"   {style['desc']}\n"
            text += f"   🎨 {style['techniques']}\n\n"
        await callback.message.edit_text(text, reply_markup=main_menu(), parse_mode="HTML")
    
    elif data == "tips":
        text = (
            "💅 <b>Советы по уходу</b>\n\n"
            "💧 <b>Увлажнение:</b>\n"
            "• Масло для кутикулы ежедневно\n"
            "• Крем для рук 2-3 раза в день\n\n"
            "✂️ <b>Правильная форма:</b>\n"
            "• Подпиливайте в одном направлении\n"
            "• Используйте стеклянную пилочку\n\n"
            "🎨 <b>Уход:</b>\n"
            "• Надевайте перчатки при уборке\n"
            "• Обновляйте топ раз в 3-4 дня"
        )
        await callback.message.edit_text(text, reply_markup=main_menu(), parse_mode="HTML")
    
    elif data == "back":
        await state.clear()
        await callback.message.edit_text(
            "💅 <b>Главное меню</b>",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    
    # Выбор длины
    elif data.startswith("len_"):
        length = data.replace("len_", "")
        await state.update_data(length=length)
        await callback.message.edit_text(
            f"✅ Длина: <b>{length}</b>\n\n"
            "Теперь выберите <b>форму</b>:",
            reply_markup=shape_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_shape)
    
    elif data == "back_length":
        await callback.message.edit_text(
            "Выберите <b>длину ногтей</b>:",
            reply_markup=length_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_length)
    
    # Выбор формы
    elif data.startswith("shape_"):
        shape = data.replace("shape_", "")
        await state.update_data(shape=shape)
        await callback.message.edit_text(
            f"✅ Длина: <b>{await state.get_value('length')}</b>\n"
            f"✅ Форма: <b>{shape}</b>\n\n"
            "Теперь выберите <b>цвет</b>:",
            reply_markup=color_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_color)
    
    elif data == "back_shape":
        await callback.message.edit_text(
            "Выберите <b>форму ногтей</b>:",
            reply_markup=shape_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_shape)
    
    # Выбор цвета
    elif data.startswith("color_"):
        color = data.replace("color_", "")
        await state.update_data(color=color)
        await callback.message.edit_text(
            f"✅ Длина: <b>{await state.get_value('length')}</b>\n"
            f"✅ Форма: <b>{await state.get_value('shape')}</b>\n"
            f"✅ Цвет: <b>{color}</b>\n\n"
            "Последний шаг - выберите <b>повод</b>:",
            reply_markup=occasion_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_occasion)
    
    elif data == "back_color":
        data_state = await state.get_data()
        await callback.message.edit_text(
            f"✅ Длина: <b>{data_state.get('length')}</b>\n"
            f"✅ Форма: <b>{data_state.get('shape')}</b>\n\n"
            "Выберите <b>цвет</b>:",
            reply_markup=color_menu(),
            parse_mode="HTML"
        )
        await state.set_state(ManicureForm.waiting_for_color)
    
    # Выбор повода и подбор
    elif data.startswith("occ_"):
        occasion = data.replace("occ_", "")
        await state.update_data(occasion=occasion)
        
        prefs = await state.get_data()
        
        # Подбираем стили
        recommendations = []
        for style_id, rules in MATCHES.items():
            score = 0
            if prefs.get("length") in rules.get("length", []):
                score += 1
            if prefs.get("shape") in rules.get("shape", []):
                score += 1
            if prefs.get("color") in rules.get("color", []):
                score += 1
            if occasion in rules.get("occasion", []):
                score += 1
            
            if score > 0:
                recommendations.append((style_id, score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        if not recommendations:
            text = "😔 Не удалось подобрать стили. Попробуйте изменить параметры."
            await callback.message.edit_text(text, reply_markup=main_menu())
            await state.clear()
            return
        
        text = f"✨ <b>Ваши предпочтения:</b>\n"
        text += f"📏 Длина: {prefs.get('length')}\n"
        text += f"🔷 Форма: {prefs.get('shape')}\n"
        text += f"🎨 Цвет: {prefs.get('color')}\n"
        text += f"🎉 Повод: {occasion}\n\n"
        text += "<b>🌟 Рекомендуемые стили:</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for style_id, score in recommendations[:5]:
            style = STYLES[style_id]
            text += f"\n<b>{style['name']}</b> (совпадение: {score}/4)\n"
            text += f"   📝 {style['desc']}\n"
            text += f"   🎨 {style['techniques']}\n"
        
        text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
        text += "💡 <i>Напишите название стиля, чтобы узнать подробнее</i>"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Подобрать заново", callback_data="select")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await state.clear()
    
    await callback.answer()

# ==================== ОБРАБОТКА ТЕКСТА ====================
@dp.message()
async def handle_text(message: types.Message):
    text = message.text.lower()
    
    # Ищем стиль
    found = None
    for key, style in STYLES.items():
        if text in style['name'].lower() or text in key:
            found = style
            break
    
    if found:
        await message.answer(
            f"{found['name']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📝 {found['desc']}\n\n"
            f"🎨 Техники: {found['techniques']}\n"
            f"🌈 Цвета: {found['colors']}\n\n"
            f"💡 <i>Этот стиль отлично подходит для любой длины!</i>",
            parse_mode="HTML"
        )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Подобрать стиль", callback_data="select")],
            [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")]
        ])
        await message.answer(
            "🤔 Я не нашел такого стиля.\n\n"
            "Попробуйте:\n"
            "• Написать: френч, омбре, глиттер\n"
            "• Или нажмите 'Подобрать стиль'",
            reply_markup=keyboard
        )

# ==================== ЗАПУСК ====================
async def main():
    print("=" * 50)
    print("🚀 Бот запускается...")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ОШИБКА: Токен не установлен!")
        print("📝 Получите токен у @BotFather")
        print("📝 Вставьте его в строку: BOT_TOKEN = 'ваш_токен'")
        return
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот запущен: @{me.username}")
        print("=" * 50)
        print("🎉 Бот работает! Напишите ему /start")
        print("=" * 50)
        
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\n🔧 Проверьте:")
        print("1. Токен правильный?")
        print("2. Интернет есть?")
        print("3. Включите VPN если Telegram блокируется")

if __name__ == "__main__":
    asyncio.run(main())
# manicure_bot.py - ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ ДЛЯ CODESPACES
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

# ==================== НАСТРОЙКИ ====================
# ЗАМЕНИТЕ НА ВАШ ТОКЕН ОТ @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ==================== ДАННЫЕ ====================
STYLES = {
    "french": {
        "name": "💅 Классический френч",
        "desc": "Белый кончик на натуральном фоне. Элегантно и универсально.",
        "tech": "френч, линии",
        "colors": "белый, розовый, бежевый"
    },
    "ombre": {
        "name": "🌈 Омбре",
        "desc": "Плавный переход цвета. Стильно и современно.",
        "tech": "омбре, градиент",
        "colors": "пастельные, розовый, синий"
    },
    "glitter": {
        "name": "✨ Глиттер",
        "desc": "Сверкающий дизайн с блестками. Идеально для праздников.",
        "tech": "блестки, стразы",
        "colors": "золото, серебро"
    },
    "matte": {
        "name": "🎨 Матовый",
        "desc": "Бархатистая текстура без блеска. Выглядит дорого.",
        "tech": "матовый топ",
        "colors": "все оттенки"
    },
    "minimalism": {
        "name": "✨ Минимализм",
        "desc": "Лаконичный дизайн с линиями и точками.",
        "tech": "геометрия, линии",
        "colors": "черный, белый, нюд"
    },
    "cat_eye": {
        "name": "🐱 Кошачий глаз",
        "desc": "Магнитный лак с эффектом перелива.",
        "tech": "магнитный лак",
        "colors": "синий, фиолетовый, бордовый"
    }
}

# ==================== КЛАВИАТУРЫ ====================
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Подобрать стиль", callback_data="select")],
        [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="💡 Советы", callback_data="tips")]
    ])

def length_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✂️ Короткие", callback_data="short")],
        [InlineKeyboardButton(text="📏 Средние", callback_data="medium")],
        [InlineKeyboardButton(text="✨ Длинные", callback_data="long")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])

def style_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💅 Френч", callback_data="style_french")],
        [InlineKeyboardButton(text="🌈 Омбре", callback_data="style_ombre")],
        [InlineKeyboardButton(text="✨ Глиттер", callback_data="style_glitter")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])

# ==================== КОМАНДЫ ====================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "💅 <b>Добро пожаловать!</b>\n\n"
        "Я помогу подобрать идеальный стиль маникюра.\n\n"
        "👇 <b>Нажмите на кнопку</b>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "❓ <b>Помощь</b>\n\n"
        "/start - начать работу\n"
        "/help - эта справка\n\n"
        "📝 <b>Как подобрать стиль:</b>\n"
        "1. Нажмите 'Подобрать стиль'\n"
        "2. Выберите длину ногтей\n"
        "3. Получите рекомендации\n\n"
        "💡 <b>Совет:</b> Напишите название стиля, чтобы узнать подробности",
        parse_mode="HTML"
    )

# ==================== ОБРАБОТЧИКИ ====================
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    data = callback.data
    
    if data == "select":
        await callback.message.edit_text(
            "💅 Выберите <b>длину ногтей</b>:",
            reply_markup=length_menu(),
            parse_mode="HTML"
        )
    
    elif data == "catalog":
        text = "<b>📖 Каталог стилей маникюра</b>\n\n"
        for style in STYLES.values():
            text += f"{style['name']}\n"
            text += f"   📝 {style['desc']}\n"
            text += f"   🎨 {style['tech']}\n\n"
        await callback.message.edit_text(text, reply_markup=main_menu(), parse_mode="HTML")
    
    elif data == "tips":
        text = (
            "💅 <b>Советы по уходу за ногтями</b>\n\n"
            "💧 <b>Увлажнение:</b>\n"
            "• Масло для кутикулы ежедневно\n"
            "• Крем для рук 2-3 раза в день\n\n"
            "✂️ <b>Правильная форма:</b>\n"
            "• Подпиливайте в одном направлении\n"
            "• Используйте стеклянную пилочку\n\n"
            "🎨 <b>Уход после маникюра:</b>\n"
            "• Надевайте перчатки при уборке\n"
            "• Обновляйте топ раз в 3-4 дня\n\n"
            "🥗 <b>Питание:</b>\n"
            "• Добавьте в рацион биотин\n"
            "• Пейте больше воды"
        )
        await callback.message.edit_text(text, reply_markup=main_menu(), parse_mode="HTML")
    
    elif data == "back":
        await callback.message.edit_text(
            "💅 <b>Главное меню</b>",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    
    elif data in ["short", "medium", "long"]:
        length_names = {"short": "короткие", "medium": "средние", "long": "длинные"}
        length = length_names[data]
        
        # Подбираем стили по длине
        recommendations = []
        if length == "короткие":
            recommendations = ["french", "minimalism", "matte"]
        elif length == "средние":
            recommendations = ["french", "ombre", "glitter", "matte", "minimalism", "cat_eye"]
        else:  # длинные
            recommendations = ["ombre", "glitter", "cat_eye"]
        
        text = f"✨ <b>Для {length} ногтей рекомендуем:</b>\n\n"
        for style_id in recommendations[:4]:
            style = STYLES[style_id]
            text += f"{style['name']}\n"
            text += f"   📝 {style['desc']}\n\n"
        
        text += "💡 <i>Напишите название стиля, чтобы узнать подробнее</i>"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Подобрать заново", callback_data="select")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    await callback.answer()

# ==================== ОБРАБОТКА ТЕКСТА ====================
@dp.message()
async def handle_text(message: types.Message):
    text = message.text.lower()
    
    # Ищем стиль по названию
    found = None
    for key, style in STYLES.items():
        if text in style['name'].lower() or text in key:
            found = style
            break
    
    if found:
        await message.answer(
            f"<b>{found['name']}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📝 {found['desc']}\n\n"
            f"🎨 <b>Техники:</b> {found['tech']}\n"
            f"🌈 <b>Цвета:</b> {found['colors']}\n\n"
            f"💡 <i>Этот стиль отлично подходит для любой длины!</i>",
            parse_mode="HTML"
        )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Подобрать стиль", callback_data="select")],
            [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")]
        ])
        await message.answer(
            "🤔 Я не нашел такого стиля.\n\n"
            "Попробуйте:\n"
            "• Написать: френч, омбре, глиттер\n"
            "• Или нажмите 'Подобрать стиль'",
            reply_markup=keyboard
        )

# ==================== ЗАПУСК ====================
async def main():
    print("=" * 50)
    print("🚀 Бот для подбора маникюра запускается...")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ОШИБКА: Токен не установлен!")
        print("📝 Получите токен у @BotFather и замените BOT_TOKEN")
        return
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот успешно запущен: @{me.username}")
        print(f"📊 ID бота: {me.id}")
        print("=" * 50)
        print("🎉 Бот работает! Напишите ему в Telegram /start")
        print("=" * 50)
        
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\n🔧 Проверьте:")
        print("1. Токен правильный?")
        print("2. Интернет есть?")
        print("3. В GitHub Codespaces интернет всегда есть!")

if __name__ == "__main__":
    asyncio.run(main())
