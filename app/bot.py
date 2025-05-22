import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from recommender import get_recommendations

logging.basicConfig(
    filename='error.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
print("🔍 BOT_TOKEN:", BOT_TOKEN)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RecommenderForm(StatesGroup):
    mood = State()
    energy = State()
    tempo = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Привет! 🎵 Я музыкальный бот.\nНапиши /recommend, чтобы выбрать настроение и получить треки.")

@dp.message_handler(commands='recommend')
async def cmd_recommend(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Весёлое", callback_data='mood_0.9'),
        types.InlineKeyboardButton("Грустное", callback_data='mood_0.2'),
        types.InlineKeyboardButton("Расслабленное", callback_data='mood_0.4'),
        types.InlineKeyboardButton("Энергичное", callback_data='mood_0.8'),
    )
    await message.answer("Выбери настроение:", reply_markup=keyboard)
    await RecommenderForm.mood.set()

@dp.callback_query_handler(lambda c: c.data.startswith('mood_'), state=RecommenderForm.mood)
async def process_mood(callback_query: types.CallbackQuery, state: FSMContext):
    valence = float(callback_query.data.split('_')[1])
    await state.update_data(valence=valence)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Низкая", callback_data='energy_0.3'),
        types.InlineKeyboardButton("Средняя", callback_data='energy_0.6'),
        types.InlineKeyboardButton("Высокая", callback_data='energy_0.9'),
    )
    await bot.send_message(callback_query.from_user.id, "Теперь выбери энергию:", reply_markup=keyboard)
    await RecommenderForm.energy.set()

@dp.callback_query_handler(lambda c: c.data.startswith('energy_'), state=RecommenderForm.energy)
async def process_energy(callback_query: types.CallbackQuery, state: FSMContext):
    energy = float(callback_query.data.split('_')[1])
    await state.update_data(energy=energy)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Для отдыха", callback_data='tempo_90'),
        types.InlineKeyboardButton("Для прогулки", callback_data='tempo_110'),
        types.InlineKeyboardButton("Для тренировки", callback_data='tempo_130'),
    )
    await bot.send_message(callback_query.from_user.id, "И наконец — выбери активность:", reply_markup=keyboard)
    await RecommenderForm.tempo.set()

@dp.callback_query_handler(lambda c: c.data.startswith('tempo_'), state=RecommenderForm.tempo)
async def process_tempo(callback_query: types.CallbackQuery, state: FSMContext):
    tempo = float(callback_query.data.split('_')[1])
    await state.update_data(tempo=tempo)

    user_data = await state.get_data()
    valence = user_data['valence']
    energy = user_data['energy']

    try:
        tracks = get_recommendations(valence, energy, tempo)
        if not tracks:
            await bot.send_message(callback_query.from_user.id, "⚠️ Треки не найдены. Попробуй другие параметры.")
        else:
            response = "🎧 Вот твои рекомендации:\n\n"
            for t in tracks:
                response += f"🎵 {t['name']} — {t['artists']} ({int(t['tempo'])} BPM)\n"
            await bot.send_message(callback_query.from_user.id, response)

    except Exception as e:
        logging.error(f"Ошибка при получении рекомендаций: {e}")
        await bot.send_message(callback_query.from_user.id, "⚠️ Ошибка при получении рекомендаций.")
    finally:
        await state.finish()

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")