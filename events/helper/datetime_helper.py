WEEKNAMES = {
    0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт",
    4: "Пт", 5: "Сб", 6: "Вск",
}
MONTHNAMES = {
    1: "января",   2: "февраля",  3: "марта",
    4: "апреля",   5: "мая",      6: "июня",
    7: "июля",     8: "августа",  9: "сентября",
    10: "октября", 11: "ноября",  12: "декабря",
}


def weekday_name(dt):
    return WEEKNAMES[dt.weekday()]


def month_name(dt):
    return MONTHNAMES[dt.month]