import os, asyncio, threading
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

class OrderState(StatesGroup):
    waiting_friend = State()
    waiting_custom_nofee = State()
    waiting_custom_fee = State()

user_orders = {}

def main_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="stars"),
         types.InlineKeyboardButton(text="💎 Telegram Premium", callback_data="premium")],
        [types.InlineKeyboardButton(text="👤 Менеджер", url="https://t.me/lywlw"),
         types.InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="balance")],
        [types.InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/rsbsupport_bot"),
         types.InlineKeyboardButton(text="⭐ Отзывы", url="https://t.me/rsbluvv")]
    ])

def stars_choice_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⭐ Без комиссии", callback_data="stars_nofee")],
        [types.InlineKeyboardButton(text="⭐ С комиссией", callback_data="stars_fee")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="to_main")]
    ])

def who_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="👤 Себе", callback_data="who_self")],
        [types.InlineKeyboardButton(text="👥 Другу", callback_data="who_friend")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="stars")]
    ])

def nofee_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="50☆ — 400 ₸", callback_data="nofee_50"),
         types.InlineKeyboardButton(text="100☆ — 800 ₸", callback_data="nofee_100")],
        [types.InlineKeyboardButton(text="150☆ — 1 200 ₸", callback_data="nofee_150"),
         types.InlineKeyboardButton(text="200☆ — 1 600 ₸", callback_data="nofee_200")],
        [types.InlineKeyboardButton(text="250☆ — 2 000 ₸", callback_data="nofee_250"),
         types.InlineKeyboardButton(text="300☆ — 2 400 ₸", callback_data="nofee_300")],
        [types.InlineKeyboardButton(text="✨ Любое количество", callback_data="custom_nofee")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="stars_nofee")]
    ])

def fee_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="15☆ — 113 ₸", callback_data="fee_15"),
         types.InlineKeyboardButton(text="25☆ — 188 ₸", callback_data="fee_25")],
        [types.InlineKeyboardButton(text="50☆ — 375 ₸", callback_data="fee_50"),
         types.InlineKeyboardButton(text="100☆ — 750 ₸", callback_data="fee_100")],
        [types.InlineKeyboardButton(text="150☆ — 1 125 ₸", callback_data="fee_150"),
         types.InlineKeyboardButton(text="200☆ — 1 500 ₸", callback_data="fee_200")],
        [types.InlineKeyboardButton(text="✨ Любое количество", callback_data="custom_fee")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="stars")]
    ])

@dp.message(CommandStart())
async def start(message: types.Message):
    text = "𝗿‌𝘀𝗯 𝘀𝗵ׂᦢׅ𝗼𝗽 𝘄ׂ𝗲𝗹𝗰ᩚᦢׅ𝗼𝗺𝗲𝘀 𝘆ᦢׅ𝘂!\n\n♡ Telegram Stars • Premium • MM2 • накрутка соцсетей\n\nВыбирай нужную услугу и оформляй заказ!\n\n— Спасибо за выбор RSB Shop ♡"
    await message.answer(text, reply_markup=main_kb())

@dp.callback_query(F.data == "to_main")
async def to_main(c: types.CallbackQuery):
    text = "𝗿‌𝘀𝗯 𝘀𝗵ׂᦢׅ𝗼𝗽 𝘄ׂ𝗲𝗹𝗰ᩚᦢׅ𝗼𝗺𝗲𝘀 𝘆ᦢׅ𝘂!\n\n♡ Telegram Stars • Premium • MM2 • накрутка соцсетей\n\nВыбирай нужную услугу и оформляй заказ!\n\n— Спасибо за выбор RSB Shop ♡"
    await c.message.edit_text(text, reply_markup=main_kb())
    await c.answer()

@dp.callback_query(F.data == "stars")
async def stars_menu(c: types.CallbackQuery):
    await c.message.edit_text("⭐ Telegram Stars\n\nВыбери тип:", reply_markup=stars_choice_kb())
    await c.answer()

@dp.callback_query(F.data == "stars_nofee")
async def stars_nofee(c: types.CallbackQuery):
    user_orders[c.from_user.id] = {"type": "nofee"}
    await c.message.edit_text("Купить звезды\n\nКому отправляем?", reply_markup=who_kb())
    await c.answer()

@dp.callback_query(F.data == "who_self")
async def who_self(c: types.CallbackQuery):
    user_orders[c.from_user.id]["target"] = "self"
    await c.message.edit_text("👤 Себе\n\nВыбери количество:", reply_markup=nofee_kb())
    await c.answer()

@dp.callback_query(F.data == "who_friend")
async def who_friend(c: types.CallbackQuery, state: FSMContext):
    await c.message.answer("Введите @username друга, которому хотите отправить Stars.")
    await state.set_state(OrderState.waiting_friend)
    await c.answer()

@dp.message(OrderState.waiting_friend)
async def get_friend(m: types.Message, state: FSMContext):
    username = m.text.strip()
    if not username.startswith("@"): username = "@" + username
    user_orders[m.from_user.id] = user_orders.get(m.from_user.id, {})
    user_orders[m.from_user.id]["target"] = username
    await state.clear()
    await m.answer(f"Пользователь {username} принят ✅\n\nТеперь выбери количество:", reply_markup=nofee_kb())

@dp.callback_query(F.data == "stars_fee")
async def stars_fee(c: types.CallbackQuery):
    user_orders[c.from_user.id] = {"type": "fee", "target": "self"}
    await c.message.edit_text("⭐ С комиссией\n\n• 15☆ — 113 ₸\n• 25☆ — 188 ₸\n• 50☆ — 375 ₸\n• 100☆ — 750 ₸\n• 150☆ — 1 125 ₸\n• 200☆ — 1 500 ₸", reply_markup=fee_kb())
    await c.answer()

@dp.callback_query(F.data.startswith("nofee_") | F.data.startswith("fee_"))
async def buy(c: types.CallbackQuery):
    amount = c.data.split("_")[1]
    order = user_orders.get(c.from_user.id, {})
    target = order.get("target", "self")
    target_text = "тебе" if target == "self" else f"другу {target}"
    price_map_nofee = {"50":"400", "100":"800", "150":"1200", "200":"1600", "250":"2000", "300":"2400"}
    price_map_fee = {"15":"113", "25":"188", "50":"375", "100":"750", "150":"1125", "200":"1500"}
    price = price_map_nofee.get(amount) if c.data.startswith("nofee") else price_map_fee.get(amount)
    await c.message.answer(f"✅ Заказ создан: {amount}☆ — {price} ₸\nПолучатель: {target_text}\n\n💳 Реквизиты:\n4400 4300 3468 5880\nПолучатель — Шехризада Р.\n\nПосле оплаты отправь чек: @lywlw\nПравила: https://t.me/rsbluvvvv/21")
    await c.answer()

@dp.callback_query(F.data == "custom_nofee")
async def custom_nofee(c: types.CallbackQuery, state: FSMContext):
    await c.message.answer("Напиши любое количество Stars (например 75):")
    await state.set_state(OrderState.waiting_custom_nofee)
    await c.answer()

@dp.message(OrderState.waiting_custom_nofee)
async def custom_nofee_get(m: types.Message, state: FSMContext):
    try:
        amount = int(m.text)
        price = amount * 8
        order = user_orders.get(m.from_user.id, {})
        target = order.get("target", "self")
        target_text = "тебе" if target == "self" else f"другу {target}"
        await m.answer(f"✅ Заказ: {amount}☆ — {price} ₸ для {target_text}\n\nОплата: 4400 4300 3468 5880\nЧек: @lywlw")
        await state.clear()
    except:
        await m.answer("Напиши цифрами, например: 75")

@dp.callback_query(F.data == "premium")
async def premium(c: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="3 месяца — 6 300 ₸", callback_data="prem_3")],
        [types.InlineKeyboardButton(text="6 месяцев — 8 300 ₸", callback_data="prem_6")],
        [types.InlineKeyboardButton(text="12 месяцев — 16 000 ₸", callback_data="prem_12")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="to_main")]
    ])
    await c.message.edit_text("🎁 Telegram Premium\n\n• 3 месяца — 6 300 ₸\n• 6 месяцев — 8 300 ₸\n• 12 месяцев — 16 000 ₸", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data.startswith("prem_"))
async def buy_prem(c: types.CallbackQuery):
    mapping = {"prem_3":"3 месяца — 6 300 ₸", "prem_6":"6 месяцев — 8 300 ₸", "prem_12":"12 месяцев — 16 000 ₸"}
    await c.message.answer(f"✅ Заказ: Premium {mapping[c.data]}\n\nОплата: 4400 4300 3468 5880\nЧек: @lywlw\nНапиши @username для активации!")
    await c.answer()

@dp.callback_query(F.data == "balance")
async def balance(c: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="⬅️ Назад", callback_data="to_main")]])
    await c.message.edit_text("🛒 Реквизиты для оплаты\n4400 4300 3468 5880\n• Получатель — Шехризада Р.\n\nВажно перед оплатой\n• Обязательно ознакомьтесь с правилами перед оплатой.\n• За претензии, возникшие из-за непрочтения правил, ответственность не несу.\n\nПравила:\nhttps://t.me/rsbluvvvv/21", reply_markup=kb)
    await c.answer()

# Flask для Render
app = Flask(__name__)
@app.route('/')
def home(): return "Rsb-Shop OK"

def run_web(): app.run(host='0.0.0.0', port=10000)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
