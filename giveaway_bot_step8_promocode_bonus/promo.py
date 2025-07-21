
# Обработка промокодов
@dp.message_handler(commands=["promo"])
async def apply_promo(message: types.Message):
    promo_code = message.get_args().strip().upper()
    user_id = message.from_user.id

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT discount FROM promo_codes WHERE code = ?", (promo_code,))
    row = cursor.fetchone()
    if not row:
        await message.answer("❌ Промокод недействителен.")
        return

    discount = row[0]
    cursor.execute("UPDATE users SET promo_used = ?, discount = ? WHERE user_id = ?", (promo_code, discount, user_id))
    conn.commit()
    await message.answer(f"✅ Промокод применён! Скидка: {discount}%")
    conn.close()
