"""Supported languages for Fivey.

Uses Django's session/cookie language mechanism so a visitor's choice persists.
Because the deployment doesn't have GNU gettext / polib binaries, translations
are served from these compact Python dictionaries via the ``{% trans %}`` tag
in ``user/templatetags/i18n_extras.py``. Missing keys fall back to English.

To add a new language: add its ISO code to ``LANGUAGES`` in settings.py, add a
dict here, and include it in ``AVAILABLE_LANGUAGES``.
"""

# ISO-code -> (short label on the switcher, native name).
AVAILABLE_LANGUAGES = [
    ("en", ("EN", "English")),
    ("ru", ("RU", "Русский")),
    ("uz", ("UZ", "O'zbek")),
]

# Source (English) string -> translation, per language.
TRANSLATIONS = {
    # ------------------------------------------------------------------ nav
    "Home": {"ru": "Главная", "uz": "Bosh sahifa"},
    "Smart Fridge": {"ru": "Умный холодильник", "uz": "Aqlli muzlatgich"},
    "Markets": {"ru": "Магазины", "uz": "Bozorlar"},
    "Recipes": {"ru": "Рецепты", "uz": "Retseptlar"},
    "Profile": {"ru": "Профиль", "uz": "Profil"},
    "Logout": {"ru": "Выйти", "uz": "Chiqish"},
    "Login": {"ru": "Войти", "uz": "Kirish"},
    "Sign Up": {"ru": "Регистрация", "uz": "Ro'yxatdan o'tish"},
    # -------------------------------------------------------------- hero
    "AI-POWERED SMART FRIDGE": {"ru": "УМНЫЙ ХОЛОДИЛЬНИК НА ИИ", "uz": "AI ASOSIDAGI AQLLI MUZLATGICH"},
    "Your fridge.": {"ru": "Ваш холодильник.", "uz": "Sizning muzlatgichingiz."},
    "Smarter than ever.": {"ru": "Умнее, чем когда-либо.", "uz": "Har qachongidan ham aqlliroq."},
    # ---------------------------------------------------------------- cta
    "Get Started": {"ru": "Начать", "uz": "Boshlash"},
    "Create Your Smart Fridge": {"ru": "Создать умный холодильник", "uz": "Aqlli muzlatgich yaratish"},
    "Ready to make your fridge smarter?": {
        "ru": "Готовы сделать холодильник умнее?",
        "uz": "Muzlatgichingizni aqlliroq qilishga tayyormisiz?",
    },
    "Turn your refrigerator into an intelligent food inventory.": {
        "ru": "Превратите холодильник в интеллектуальный учёт продуктов.",
        "uz": "Muzlatgichingizni aqlli oziq-ovqat inventariga aylantiring.",
    },
    # ------------------------------------------------------------- banners
    "Make it personal!": {"ru": "Сделайте личным!", "uz": "Shaxsiylashtiring!"},
    "Add your date of birth on your profile page and we'll remember to wish you a happy birthday.": {
        "ru": "Добавьте дату рождения на странице профиля, и мы поздравим вас с днём рождения.",
        "uz": "Profil sahifangizda tug'ilgan kuningizni qo'shing, biz sizni tabriklaymiz.",
    },
    "Add birthday": {"ru": "Добавить день рождения", "uz": "Tug'ilgan kunni qo'shish"},
    # ----------------------------------------------------------- markets
    "Food markets, coming soon.": {"ru": "Продуктовые магазины скоро.", "uz": "Oziq-ovqat bozorlari tez orada."},
    "We are preparing smart shopping suggestions based on your fridge inventory.": {
        "ru": "Мы готовим умные рекомендации по покупкам на основе вашего холодильника.",
        "uz": "Muzlatgich inventaringiz asosida aqlli xarid takliflarini tayyorlayapmiz.",
    },
    "Back to home": {"ru": "На главную", "uz": "Bosh sahifaga qaytish"},
}

# ----------------------------------------------------------- auth
EXTRA_TRANSLATIONS = {
    "Fivey": {"ru": "Fivey", "uz": "Fivey"},
    "AI-powered food & health platform": {
        "ru": "ИИ-платформа для питания и здоровья",
        "uz": "Oziq-ovqat va salomatlik uchun AI platforma",
    },
    "Create your account": {"ru": "Создать аккаунт", "uz": "Akkaunt yaratish"},
    "Start managing your food, nutrition and health with AI.": {
        "ru": "Начните управлять питанием и здоровьем с помощью ИИ.",
        "uz": "AI bilan oziq-ovqat va salomatlikni boshqaring.",
    },
    "Full Name": {"ru": "Полное имя", "uz": "To'liq ism"},
    "Username": {"ru": "Имя пользователя", "uz": "Foydalanuvchi nomi"},
    "Email Address": {"ru": "Электронная почта", "uz": "Elektron pochta"},
    "Password": {"ru": "Пароль", "uz": "Parol"},
    "Confirm Password": {"ru": "Подтвердите пароль", "uz": "Parolni tasdiqlang"},
    "Create Account": {"ru": "Создать аккаунт", "uz": "Akkaunt yaratish"},
    "Already have an account?": {"ru": "Уже есть аккаунт?", "uz": "Akkauntingiz bormi?"},
    "Sign In": {"ru": "Войти", "uz": "Kirish"},
    "Don't have an account?": {"ru": "Нет аккаунта?", "uz": "Akkauntingiz yo'qmi?"},
    "Create one": {"ru": "Создать", "uz": "Yaratish"},
    "Access your AI-powered food and health dashboard.": {
        "ru": "Получите доступ к панели питания и здоровья на базе ИИ.",
        "uz": "AI asosidagi oziq-ovqat va salomatlik panelingizga kiring.",
    },
    "Enter your username": {"ru": "Введите имя пользователя", "uz": "Foydalanuvchi nomingizni kiriting"},
    "Enter your password": {"ru": "Введите пароль", "uz": "Parolingizni kiriting"},
    "Your profile": {"ru": "Ваш профиль", "uz": "Sizning profilingiz"},
    "Date of Birth": {"ru": "Дата рождения", "uz": "Tug'ilgan sana"},
    "Add your birthday and we'll wish you a happy birthday on the day.": {
        "ru": "Добавьте день рождения, и мы поздравим вас в этот день.",
        "uz": "Tug'ilgan kuningizni qo'shing, biz o'sha kuni tabriklaymiz.",
    },
    "Save Changes": {"ru": "Сохранить", "uz": "Saqlash"},
    "Back to Home": {"ru": "На главную", "uz": "Bosh sahifaga"},
    "AI Recipes & Calorie Calculator": {
        "ru": "ИИ-рецепты и калькулятор калорий",
        "uz": "AI Retseptlar va Kaloriya Hisoblagich",
    },
    "Recipe Suggestions": {"ru": "Рекомендации по рецептам", "uz": "Retsept bo'yicha tavsiyalar"},
}

# Merge the extra block into the main dictionary.
TRANSLATIONS.update(EXTRA_TRANSLATIONS)
del EXTRA_TRANSLATIONS


def translate(lang, text):
    """Return ``text`` translated into ``lang`` (falling back to English)."""
    if not text:
        return text
    mapping = TRANSLATIONS.get(text)
    if mapping and lang in mapping:
        return mapping[lang]
    return text