from datetime import date

# Función para validar el precio de venta, asegurando que no sea menor al precio de compra.
def validate_sale_price(sale_price: float, values: dict) -> float:
    purchase_price = values.get("purchase_price")
    if purchase_price is not None and sale_price <= purchase_price:
        raise ValueError("El precio de venta no puede ser menor al precio de compra.")
    return sale_price

# Función para validar la fecha de compra
def validate_purchase_date(purchase_date: date) -> date:
    today = date.today()
    min_date = date(today.year - 5, today.month, today.day)
    if purchase_date > today:
        raise ValueError("La fecha de compra no puede ser posterior a la fecha actual.")
    if purchase_date < min_date:
        raise ValueError("La fecha de compra debe estar dentro de los últimos 5 años.")
    return purchase_date

# Función para validar que si es pastilla puede estar activa, los demás tipos no pueden estar activos
def validate_is_active(is_active: bool, values: dict) -> bool:
    type_ = values.get("type")
    if type_ != "Pastilla" and is_active:
        raise ValueError("Solo las pastillas pueden ser activas.")
    return is_active

# Función para validar los subtipos de componentes según su tipo
def validate_subtype(subtype: str, values: dict) -> str:
    type_ = values.get("type")
    valid_subtypes = {
        "Pastilla": ["S", "H"],
        "Potenciómetro": ["Tono", "Volumen"],
        "Puente": ["Fijo", "Flotante", "Semiflotante"]
    }

    if type_ in valid_subtypes and subtype not in valid_subtypes[type_]:
        raise ValueError(f"Subtipo inválido para el tipo '{type_}'. Opciones válidas: {valid_subtypes[type_]}")
    return subtype
