"""Translate memory failures and remote quota messages separately."""

import re


def describe_generation_error(error: Exception):
    message = str(error)
    lowered = message.lower()
    if isinstance(error, MemoryError) or any(marker in lowered for marker in (
        "failed to allocate memory", "out of memory", "not enough memory", "bad allocation",
    )):
        return 503, (
            "Не хватило оперативной памяти для обработки фотографии. "
            "Закройте лишние приложения и вкладки, перезапустите backend и попробуйте снова. "
            "Это не лимит генераций — ожидание обновления квоты не требуется."
        )
    if "zerogpu" in lowered and "quota" in lowered:
        wait = re.search(r"Try again in\s+(\d+):(\d{2}):(\d{2})", message, re.IGNORECASE)
        detail = "Закончилась доступная GPU-квота Hugging Face для создания 3D-моделей."
        if wait:
            hours, minutes, seconds = map(int, wait.groups())
            detail += f" До обновления квоты осталось: {hours} ч {minutes} мин {seconds} с."
        else:
            detail += " Сервис не сообщил время обновления квоты. Попробуйте позже."
        return 429, detail
    return 502, f"Не удалось создать 3D-модель: {type(error).__name__}: {error}"
