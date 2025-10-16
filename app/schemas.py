from pydantic import BaseModel, Field

class RoomInput(BaseModel):
    тип_помещения: str
    площадь_м2: float
    высота_м: float
    целевой_люкс: int
    cri_min: int
    cct_предпочтение_k: int
    ip_min: int
    budget_rub: int = Field(..., alias="бюджет_₽")

    class Config:
        populate_by_name = True  # Позволяет использовать оба варианта названия


class Recommendation(BaseModel):
    бренд: str
    тип_светильника: str
    серия: str
    оценка: float
    количество_светильников: int
    ориентировочная_цена: float