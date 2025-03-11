import io
import os
import random

from pptx import Presentation
from pydantic import BaseModel
from text_generator import generate_slide_text
from image_generaor import generate_slide_image



class PresentationRequest(BaseModel):
    topic: str
    slides_count: int
    theme: str


def create_presentation(topic: str, slides_count: int, theme: str) -> io.BytesIO:
    # Выбор шаблона в зависимости от темы
    if theme.lower() == "dark":
        template_path = "themes/dark.pptx"
    elif theme.lower() == "light":
        template_path = "themes/light.pptx"
    else:
        raise ValueError("Некорректная тема. Используйте 'dark' или 'light'.")

    prs = Presentation(template_path)

    # Добавляем титульный слайд (макет с индексом 0)
    title_layout = prs.slide_layouts[0]
    title_slide = prs.slides.add_slide(title_layout)
    title_placeholder = title_slide.placeholders[0]
    title_placeholder.text = topic

    # Допустимые макеты для обычных слайдов: используем макеты с индексами 1, 2, 3
    allowed_layouts = list(prs.slide_layouts)[1:4]

    for _ in range(slides_count):
        layout = random.choice(allowed_layouts)
        slide = prs.slides.add_slide(layout)

        # Генерируем текст для слайда
        slide_text = generate_slide_text(topic)

        # Получаем список плейсхолдеров в слайде
        placeholders = list(slide.placeholders)

        # Обработка в зависимости от количества плейсхолдеров
        if len(placeholders) == 1:
            # Единственный placeholder используется для текста
            placeholders[0].text = slide_text
        elif len(placeholders) == 2:
            # Первый для заголовка, второй для текста
            placeholders[0].text = "тут будет заголовок"
            placeholders[1].text = slide_text
        elif len(placeholders) >= 3:
            # Первый для заголовка, второй для текста, третий для изображения
            placeholders[0].text = "тут будет заголовок"
            placeholders[1].text = slide_text
            image_prompt = f"{topic} illustration"
            image_path = generate_slide_image(image_prompt)
            try:
                placeholders[2].insert_picture(image_path)
            except Exception as e:
                print(f"Ошибка при вставке изображения: {e}")

            # Удаляем временный файл с изображением, если он существует
            if os.path.exists(image_path):
                os.remove(image_path)

    # Добавление завершающего слайда
    title_layout = prs.slide_layouts[0]
    title_slide = prs.slides.add_slide(title_layout)
    title_placeholder = title_slide.placeholders[0]
    title_placeholder.text = "Спасибо за внимание!"

    ppt_io = io.BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io