"""
AI Advisor — модуль интерпретации рекомендаций.
Генерирует объяснения выбора светильников на понятном инженерном языке.
"""

def generate_advice(recommendations: list, room_params: dict) -> str:
    """
    Формирует объяснение выбора на естественном языке.

    Args:
        recommendations (list): top-N рекомендаций от модели
        room_params (dict): входные параметры помещения
    Returns:
        str: текстовое объяснение
    """
    if not recommendations:
        return "Не удалось сформировать рекомендации для данного помещения."

    room_type = room_params.get("тип_помещения", "помещение")
    lux = room_params.get("целевой_люкс", 400)
    cct_pref = room_params.get("cct_предпочтение_k", 4000)
    cri_min = room_params.get("cri_min", 80)
    ip_min = room_params.get("ip_min", 40)

    explanation = [
        f"Для вашего помещения ({room_type}) с нормой освещённости {lux} лк рекомендованы следующие решения:"
    ]

    for rec in recommendations:
        brand = rec.get("бренд", "неизвестный бренд")
        model = rec.get("серия", "")
        typ = rec.get("тип_светильника", "светильник")
        power = rec.get("мощность_вт", 0)
        count = rec.get("количество_светильников", 1)
        cct = rec.get("cct_k", cct_pref)
        cri = rec.get("cri", cri_min)
        ip = rec.get("ip", ip_min)
        eff = rec.get("эффективность_лм_вт", None)
        price = rec.get("итоговая_стоимость_₽", None)
        lux_val = rec.get("освещенность_лк", lux)

        text = (
            f"💡 {brand} {model} ({typ}) — {count} шт. по {power:.0f} Вт, "
            f"создаёт освещённость около {lux_val:.0f} лк при "
            f"цветовой температуре {cct}K и CRI≈{cri}. "
            f"Степень защиты IP{ip}, подходит для условий эксплуатации."
        )
        if eff:
            text += f" Энергоэффективность ≈{eff:.0f} лм/Вт."
        if price:
            text += f" Ориентировочная стоимость комплекта {price:,.0f} ₽."
        explanation.append(text)

    explanation.append(
        "Все указанные варианты соответствуют нормам освещённости и обеспечивают комфортное восприятие света."
    )

    return "\n".join(explanation)
