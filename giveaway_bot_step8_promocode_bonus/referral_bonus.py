
# Команда для просмотра заработанных реферальных бонусов
@dp.message_handler(commands=['my_bonus'])
async def my_bonus(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ? AND paid = 1", (user_id,))
    count = cursor.fetchone()[0]

    bonus = count * referral_bonus_rub
    await message.answer(f"💸 Вы заработали {bonus}₽ реферальных бонусов.")
    conn.close()
