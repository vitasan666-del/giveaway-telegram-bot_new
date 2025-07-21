
# Обработка оплаты с учётом промокода
@dp.message_handler(commands=['pay'])
async def cmd_pay(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT discount FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    discount = row[0] if row else 0

    price = price_rub
    if discount:
        price = int(price_rub * (100 - discount) / 100)

    prices = [LabeledPrice(label="Участие", amount=price * 100)]
    await bot.send_invoice(
        chat_id=user_id,
        title="Оплата со скидкой",
        description=f"Скидка {discount}%",
        payload=str(user_id),
        provider_token=pay_provider_token,
        currency="RUB",
        prices=prices,
        start_parameter="giveaway",
    )
    conn.close()
