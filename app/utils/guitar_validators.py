from datetime import date

# Función para validar el precio de venta, asegurando que no sea menor al precio de compra.
def validate_sale_price(sale_price: float, values: dict) -> float:
    purchase_price = values.get("purchase_price")
    if purchase_price is not None and sale_price <= purchase_price:
        raise ValueError("El precio de venta no puede ser menor al precio de compra.")
    return sale_price

# Función para validar el precio de liquidación, asegurando que no sea mayor al precio de venta.
def validate_liquidation_price(liquidation_price: float, values: dict) -> float:
    sale_price = values.get("sale_price")
    if sale_price is not None and liquidation_price >= sale_price:
        raise ValueError("El precio de liquidación no puede ser mayor al precio de venta.")
    return liquidation_price

# Función para validar la fecha de compra, asegurando que no sea posterior a la fecha actual.
def validate_purchase_date(purchase_date: date) -> date:
    if purchase_date > date.today():
        raise ValueError("La fecha de compra no puede ser posterior a la fecha actual.")
    return purchase_date

# Función para calcular automáticamente el precio neto y el IVA a partir del precio de venta.
def auto_calculate_prices(values: dict) -> dict:
    sale_price = values.get("sale_price")
    if sale_price is not None:
        net_price = round(sale_price / 1.19, 2)
        iva = round(sale_price - net_price, 2)
        values["net_price"] = net_price
        values["iva"] = iva
    return values
