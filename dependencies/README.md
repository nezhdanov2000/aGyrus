# 📦 Dependencies

Папка содержит файлы зависимостей для разных компонентов проекта.

## 📋 Файлы зависимостей

### `requirements.txt` - Общие зависимости
Основные зависимости, необходимые для работы проекта:
- Конфигурация и окружение
- Разработка и тестирование  
- Логирование и утилиты

```bash
pip install -r dependencies/requirements.txt
```

### `requirements-logistic-regression.txt` - Компоненты логистической регрессии
Зависимости для логистической регрессии:
- numpy, scikit-learn
- pandas для обработки данных
- Опциональные NLP библиотеки

```bash
pip install -r dependencies/requirements-logistic-regression.txt
```

### `requirements-gpt2.txt` - GPT-2 компоненты
Зависимости для работы с GPT-2:
- transformers, torch
- Оригинальные GPT-2 зависимости
- Опциональные библиотеки для производительности

```bash
pip install -r dependencies/requirements-gpt2.txt
```

## 🚀 Установка

### Полная установка (все компоненты):
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-logistic-regression.txt
pip install -r dependencies/requirements-gpt2.txt
```

### Только компоненты логистической регрессии:
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-logistic-regression.txt
```

### Только GPT-2 компоненты:
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-gpt2.txt
```

## 📊 Размеры пакетов

| Компонент | Размер | Время установки |
|-----------|--------|----------------|
| Общие | ~50MB | ~2 мин |
| Логистическая регрессия | ~200MB | ~5 мин |
| GPT-2 | ~2GB | ~15 мин |

## 🔧 Рекомендации

- **Для разработки**: установите все зависимости
- **Для продакшена**: устанавливайте только нужные компоненты
- **Для тестирования**: достаточно общих + логистической регрессии зависимостей
