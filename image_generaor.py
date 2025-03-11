from diffusers import StableDiffusionPipeline
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
sd_pipeline = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
sd_pipeline = sd_pipeline.to(device)

#     Генерирует изображение, сохраняет изображение во временный файл и возвращает путь к файлу
def generate_slide_image(topic: str) -> str:

    image = sd_pipeline(topic).images[0]
    image_path = f"slide_{hash(topic)}.png"
    image.save(image_path)
    return image_path