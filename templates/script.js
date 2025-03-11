// В этом файле описана логика отправки запроса на бэкенд
// и скачивания результата.

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("presentationForm");
  const messageEl = document.getElementById("message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Считываем значения из формы
    const topic = document.getElementById("topic").value.trim();
    const theme = document.getElementById("theme").value;
    const slidesCount = parseInt(document.getElementById("slidesCount").value, 10);

    // Минимальная валидация
    if (!topic) {
      messageEl.textContent = "Пожалуйста, введите тему презентации.";
      return;
    }
    if (slidesCount < 1) {
      messageEl.textContent = "Количество слайдов не может быть меньше 1.";
      return;
    }

    // Очищаем возможные старые сообщения
    messageEl.textContent = "Генерация презентации... Подождите, пожалуйста.";

    // Формируем данные для запроса
    const data = {
      topic,
      slides_count: slidesCount,
      theme
    };

    try {
      // Отправляем POST-запрос на наш бэкенд
      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        // Если возникла ошибка на сервере, выводим сообщение
        const errorText = await response.text();
        throw new Error(errorText || "Не удалось сгенерировать презентацию.");
      }

      // Получаем файл (pptx) в виде Blob
      const blob = await response.blob();

      // Создаём временную ссылку на Blob
      const downloadUrl = URL.createObjectURL(blob);

      // Создаём скрытую ссылку для скачивания
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "presentation.pptx"; // Имя файла для сохранения
      document.body.appendChild(link);
      link.click();

      // Удаляем ссылку
      document.body.removeChild(link);

      // Очищаем Blob-URL
      URL.revokeObjectURL(downloadUrl);

      messageEl.textContent = "Презентация успешно сгенерирована и загружена!";
    } catch (error) {
      console.error("Ошибка при генерации презентации:", error);
      messageEl.textContent = `Ошибка: ${error.message}`;
    }
  });
});