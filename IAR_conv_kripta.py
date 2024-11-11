from tkinter import *
from tkinter import messagebox as mb
import requests
from tkinter import ttk
from datetime import datetime
# Импортирую необходимые библиотеки


def exchange(crypto_code, code):
    # Функция для получения курса обмена между криптовалютой и валютой
    url = "https://api.coingecko.com/api/v3/simple/price"  # URL API с сайта CoinGecko
    params = {
        "ids": crypto_code,
        "vs_currencies": code,
        "include_last_updated_at": "true"
    }
    if code and crypto_code:  # Проверка на наличие выбранных валют
        try:
            response = requests.get(url, params=params)  # Выполнение GET-запроса
            response.raise_for_status()
            data = response.json()
            if crypto_code in data and code in data[crypto_code]:
                exchange_rates = data[crypto_code][code]  # Получение курса обмена
                last_updated = data[crypto_code]["last_updated_at"]  # Получение времени последнего обновления
                last_updated = datetime.fromtimestamp(last_updated).strftime("%d.%m.%Y %H:%M:%S")

                return (f"На {last_updated} текущий курс:\n{cryptocurrency[crypto_code]} к {currency[code]}:"
                        f"\n{exchange_rates:.2f} {code.upper()} за 1 {crypto_code.upper()}")

            else:
                return f"Код валюты не найден!"  # Обработка случая, когда код не найден
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка запроса!",
                         f"Ошибка при запросе: {e}!")  # Обработка ошибки запроса
    else:
        mb.showwarning("Внимание!",
                       "Пожалуйста, выберите криптовалюту и валюту!")  # Предупреждение о незаполненных полях


def update_cryptocurrency_label(event):
    # Обновляет метку криптовалюты
    code = cryptocurrency_combobox.get()
    if code in cryptocurrency:
        cryptocurrency_label.config(text=cryptocurrency[code])
    else:
        cryptocurrency_label.config(text="")


def update_currency_label(event):
    # Обновляет метку валюты
    code = currency_combobox.get()
    if code in currency:
        currency_label.config(text=currency[code])
    else:
        currency_label.config(text="")


def show_exchange():
    # Отображает курс обмена при нажатии кнопки
    crypto_code = cryptocurrency_combobox.get()
    code = currency_combobox.get()
    result = exchange(crypto_code, code)
    if result:
        label.config(text=result)


def clear():
    # Очищает все поля ввода и метки
    cryptocurrency_combobox.set("")
    currency_combobox.set("")
    cryptocurrency_label.config(text="")
    currency_label.config(text="")
    label.config(text="")


# Создание графического интерфейса
window = Tk()
window.title("Конвертер криптовалют")
window.geometry("400x440")


# Словари для криптовалют и валют
cryptocurrency = {
    "bitcoin": "BTC (Биткойн)",
    "ethereum": "ETH (Эфир)",
    "litecoin": "LTC (Лайткойн)",
    "bitcoin-cash": "BCH (Биткойн Кэш)",
    "binancecoin": "BNB (Бинанс Коин)",
    "eos": "EOS",
    "ripple": "XRP (Риппл)",
    "stellar": "XLM (Стеллар)",
    "chainlink": "LINK (ЧейнЛинк)",
    "polkadot": "DOT (Полкадот)"
}

currency = {
    "usd": "United States Dollar (Американский доллар)",
    "eur": "Euro (Евро)",
    "gbp": "British Pound Sterling (Британский\nфунт стерлингов)",
    "cny": "Chinese Yuan (Китайский юань)",
    "rub": "Russian Ruble (Российский рубль)"
}


# Элементы интерфейса
Label(text="Криптовалюта", font="Arial 11").pack(padx=10, pady=10)  # Метка для криптовалюты
cryptocurrency_combobox = ttk.Combobox(values=list(cryptocurrency.keys()))
cryptocurrency_combobox.bind("<<ComboboxSelected>>", update_cryptocurrency_label)
cryptocurrency_combobox.pack(padx=10, pady=10)

cryptocurrency_label = ttk.Label()  # Метка для отображения выбранной криптовалюты
cryptocurrency_label.pack(padx=10, pady=10)

Label(text="Валюта", font="Arial 11").pack(padx=10, pady=10)  # Метка для валюты
currency_combobox = ttk.Combobox(values=list(currency.keys()))
currency_combobox.bind("<<ComboboxSelected>>", update_currency_label)
currency_combobox.pack(padx=10, pady=10)

currency_label = ttk.Label()  # Метка для отображения выбранной валюты
currency_label.pack(padx=10, pady=10)

ttk.Button(text="Получить курс обмена", command=show_exchange).pack(pady=10)  # Кнопка для получения курса обмена

label = ttk.Label(font=("Arial", 9))  # Метка для отображения результата
label.pack(padx=10, pady=10)

ttk.Button(text="Очистить", command=clear).pack(pady=10)  # Кнопка для очистки полей и результата


window.mainloop()  # Запуск основного цикла приложения