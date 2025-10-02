#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для тестирования GPT-2 с использованием библиотеки transformers
"""

import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def generate_text(prompt, max_length=100, temperature=0.7, top_k=50, top_p=0.9):
    """
    Генерирует текст на основе заданного промпта
    
    Параметры:
    - prompt: начальный текст (строка)
    - max_length: максимальная длина генерируемого текста
    - temperature: контролирует случайность (меньше = более предсказуемо)
    - top_k: выбирает из top-k наиболее вероятных слов
    - top_p: nucleus sampling (суммарная вероятность)
    """
    print("\n🤖 Загружаю модель GPT-2...")
    
    # Загружаем предобученную модель и токенизатор
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    
    # Переводим модель в режим инференса
    model.eval()
    
    print(f"✅ Модель загружена!\n")
    print(f"📝 Промпт: {prompt}\n")
    print("=" * 60)
    
    # Кодируем входной текст
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    
    # Генерируем текст
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True
        )
    
    # Декодируем результат
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    print(generated_text)
    print("=" * 60)
    
    return generated_text


def interactive_mode():
    """
    Интерактивный режим - можно вводить промпты в консоли
    """
    print("\n" + "=" * 60)
    print("🚀 ИНТЕРАКТИВНЫЙ РЕЖИМ GPT-2")
    print("=" * 60)
    print("\nВведите текст для продолжения (или 'quit' для выхода)")
    print("Вы можете настроить параметры генерации в функции generate_text()\n")
    
    # Загружаем модель один раз
    print("🤖 Загружаю модель GPT-2...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model.eval()
    print("✅ Модель готова!\n")
    
    while True:
        try:
            prompt = input("\n📝 Введите промпт >>> ")
            
            if prompt.lower() in ['quit', 'exit', 'выход']:
                print("\n👋 До свидания!")
                break
                
            if not prompt.strip():
                print("⚠️ Промпт не может быть пустым!")
                continue
            
            print("\n⏳ Генерирую текст...")
            print("=" * 60)
            
            # Кодируем и генерируем
            input_ids = tokenizer.encode(prompt, return_tensors='pt')
            
            with torch.no_grad():
                output = model.generate(
                    input_ids,
                    max_length=150,
                    temperature=0.8,
                    top_k=50,
                    top_p=0.95,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.eos_token_id,
                    do_sample=True
                )
            
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            print(generated_text)
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана. До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎯 ТЕСТ GPT-2")
    print("=" * 60)
    
    # Пример 1: Простая генерация
    print("\n📌 Пример 1: Генерация текста")
    generate_text(
        prompt="Once upon a time",
        max_length=100,
        temperature=0.7
    )
    
    # Пример 2: Другой промпт
    print("\n📌 Пример 2: Другой стиль")
    generate_text(
        prompt="The future of artificial intelligence",
        max_length=120,
        temperature=0.8
    )
    
    # Запрашиваем интерактивный режим
    print("\n" + "=" * 60)
    choice = input("\n🔄 Хотите попробовать интерактивный режим? (y/n): ")
    
    if choice.lower() in ['y', 'yes', 'д', 'да']:
        interactive_mode()
    else:
        print("\n✅ Тестирование завершено!")
