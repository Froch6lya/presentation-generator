from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")
rugpt3_model = GPT2LMHeadModel.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")

def generate_slide_text(topic: str) -> str:
    prompt = f"Напиши краткий текст по теме: {topic}."

    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Настройки генерации:
    # - do_sample для разнообразия вариантов;
    # - temperature для баланса креативности и связности;
    # - top_p top_k для контроля качества;
    # - max_length количество токенов.
    max_tokens = 90
    outputs = rugpt3_model.generate(
        input_ids,
        do_sample=True,
        max_length=max_tokens,
        temperature=0.2,
        top_p=0.95,
        top_k=30,
        num_return_sequences=1,
        no_repeat_ngram_size=3
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_text = text[len(prompt):].strip()
    return generated_text


#print(generate_slide_text( "Роснефть, добыча нефти за 2023 год"))