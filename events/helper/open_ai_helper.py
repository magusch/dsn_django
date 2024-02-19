# -*- coding: utf-8 -*-
from openai import OpenAI


class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI()
        self.answer = None

    def refactor_post(self, event):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Ты редактор-копирайтер для телеграм канала о мероприятиях в Санкт-Петербурге. У нас есть сырая информация по мероприятию необходимо адаптировать её для поста."},
                {"role": "user",
                 "content": f"""Необходимо прочитать текст, заголовок и другую информацию и отредактировать их по следующим инструкциям:
                 Заголовок не должен содержать какие-то даты и упоминания места проведения мероприятия. Необходимо из текста понять какой тип мероприятия (лекция, кинопоказ, концерт, фестиваль и другие) (на кирилице), названия мероприятия на кирилице нужно поставить в кавычки, на латинице кавычки не нужны. Добавить эмодзи в начале по смыслу. В конечном итоге составить заголовк по шаблону "<ЭМОДЗИ> <Тип мероприятия> <Название мероприятия>". Пример (🚀 Лекция «Покорение космоса в СССР»).
                 Текст мероприятия не должен содержать какие-то точные даты, по возможности перевести их в указания дней недель. Также Убрать все ссылки, спец-символы и другие мешающие вещи из текста. Из всего текста выделить основную мысль и выложить её в одном абзаце (1-3 предложения). Стиль написания должен быть упрощённым и понятным, а также не быть от первого лица. Все местоимения перефразировать в третье лицо ("они что-то сделали")
                 Выделить категорию мероприятия. Выделить несколько важных тегов мероприятия. Результат выдать в виде названия информации (заголовк, текст) двоеточие и результат.
                 МЕРОПРИЯТИЕ:
                 Заголовок: {event['title']}
                 Текст: {event['full_text']}
                 """}
            ]
        )

        self.answer = completion.choices[0].message.content

        return self.answer

    def parse_gpt_answer(self):
        if self.answer is None:
            return {}
        data = self.answer.split('\n')
        event_data = {}
        for d in data:
            if d.strip() == '':
                continue
            divided = d.split(':')
            event_data[divided[0].strip()] = divided[-1].strip()
        return event_data

    def new_event_data(self, event):
        replace_phrases = {'Текст': 'full_text', 'Заголовок': 'title', 'Категория': 'category'}
        if self.answer is None:
            self.refactor_post(event)
        ai_event_data = self.parse_gpt_answer()

        ai_event = {}
        for key, new_event_data in ai_event_data.items():
            if key not in replace_phrases.keys(): continue
            ai_event[replace_phrases[key]] = new_event_data
        return ai_event

