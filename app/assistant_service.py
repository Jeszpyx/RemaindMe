from typing import Optional
from constants import enviroment
import httpx
from datetime import datetime, timezone


class AssistantService:

    def __init__(self) -> None:
        self._api_url = f"{enviroment.OLLAMA_HOST}/api/chat"
        self._model = enviroment.OLLAMA_MODEL
        self._notify_system_prompt = f"""Ты — высокоточный парсер напоминаний.
            Твоя задача: точно извлекать из текста ДАТУ/ВРЕМЯ и СОБЫТИЕ.
            Отвечай ТОЛЬКО в формате:<DATETIME>|<EVENT>Жесткие правила:
            1. DATETIME — абсолютная дата и время в формате ГГГГ-ММ-ДД ЧЧ:ММ (UTC)
            2. EVENT — суть события (ровно 3-7 слов)3. СЕЙЧАС: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %Z")} UTC
            4.Временные окна:- Для деловых/рабочих задач: 09:00-18:00- Для личных дел: 10:00-20:00- Для срочных/медицинских: точное время
            5. Приоритеты времени:- Если указан только срок ('через неделю'):     * Рабочие задачи → 14:00    * Личные дела → 16:00- Если указано время суток:    'утром' = 09:00 (рабочее) / 10:00 (личное)    'днем' = 14:00    'вечером' = 18:00 (рабочее) / 19:00 (личное)
            6. Контекстная коррекция:- Ночные часы (22:00-06:00) автоматически сдвигай на утро (+12 часов)- Выходные (сб, вс): +1 час к стандартному времени
            7. Всегда учитывай:- Текущий месяц: Июль (31 день)- Переход месяцев/годов- Только будущие даты!
            Примеры:
            1. 'Забрать документы через неделю' → '2025-07-26 14:00|Забрать документы' (рабочее)
            2. 'Купить велосипед в субботу' → '2025-07-26 16:00|Купить велосипед' (личное, выходной)
            3. 'Отчет к 17:00 в пятницу' → '2025-07-25 17:00|Сдать отчет' (точное время)
            4. 'Заказать пиццу ночью' → '2025-07-19 10:00|Заказать пиццу' (сдвиг с 01:10 на 10:00)5. 'Встреча с другом завтра' → '2025-07-20 16:00|Встреча с другом' (личное)Критические улучшения:- Автоматический сдвиг нереалистичных времен- Учет типа события (рабочее/личное)- Коррекция для выходных- Запрет ночных часов для неэкстренных задач"""
        self._client = httpx.AsyncClient(timeout=60.0)

    async def get_notification_data(self, user_prompt: str) -> Optional[str]:
        """
        Отправляет запрос к Ollama API и возвращает распаршенные данные напоминания

        :param user_prompt: Текст пользователя для анализа
        :return: Строка в формате "DATETIME|EVENT" или None при ошибке
        """
        try:
            payload = {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": self._notify_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
                "think": False,
                "options": {
                "temperature": 0.1,  # Минимизируем "креативность"
                "num_predict": 50,   # Ограничиваем длину ответа
                "stop": ["\n"]       # Останавливаем генерацию при переносе строки
                },
                "template": """
                {{ if .System }}<|system|>
                {{ .System }}<|end|>
                {{ end }}<|user|>
                {{ .Prompt }}<|end|>
                <|assistant|>"""
            }

            print(self._api_url, "_api_url")

            response = await self._client.post(
                self._api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()  # Вызовет исключение для 4XX/5XX ответов

            data = response.json()
            return data.get("message", {}).get("content", "").strip()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Request failed: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


assistant_service = AssistantService()
