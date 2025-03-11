from pptx_generator import create_presentation
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Инициализация приложения
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модель запроса
class PresentationRequest(BaseModel):
    topic: str
    slides_count: int
    theme: str  # "light" или "dark"


# Базовый эндпоинт
@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}


# Поддержка OPTIONS
@app.options("/generate")
async def options_generate():
    response = Response()
    response.headers["Allow"] = "POST, OPTIONS"
    return response


# Генерация презентации
@app.post("/generate")
async def generate_presentation(pres_req: PresentationRequest):
    """
    Генерирует и возвращает презентацию в формате PPTX
    """
    ppt_io = create_presentation(
        topic=pres_req.topic,
        slides_count=pres_req.slides_count,
        theme=pres_req.theme
    )

    return StreamingResponse(
        content=ppt_io,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=presentation.pptx"}
    )


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000
    )