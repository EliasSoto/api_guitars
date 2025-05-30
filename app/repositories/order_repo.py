from sqlalchemy.orm import Session
from app.models.order import Order
from fastapi import HTTPException, status
from app.schemas import order as order_schema
from app.schemas.order import OrderListResponse
from app.models.order_detail import OrderDetail
from app.models.guitar import Guitar
from datetime import date

### FUNCIONES PARA USUARIOS ADMIN ###

# Función para crear una nuevo pedido.
def create_order(db: Session, user_id: int, order: order_schema.OrderCreate):  
    try:
        if not order.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pedido debe contener al menos una guitarra con su cantidad."
            )

        # Se valida la existencia de las guitarras y el stock.
        validated_items = []
        total_price = 0
        for item in order.items:
            guitar = db.query(Guitar).filter(Guitar.id == item.guitar_id).first()
            # Si no se encuentra la guitarra, lanzamos una excepción.
            if not guitar:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Guitarra con ID {item.guitar_id} no encontrada."
                )
            # Si la guitarra no tiene stock suficiente, lanzamos una excepción.
            if guitar.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No hay suficiente stock para la guitarra ID {item.guitar_id}."
                )
            validated_items.append((guitar, item.quantity))
            
            # Se calcula el precio total del pedido
            if guitar.liquidation_price:
                # Si hay un precio de liquidación, se usa ese precio
                price_to_use = guitar.liquidation_price
            else:
                # Si no hay precio de liquidación, se usa el precio de venta
                price_to_use = guitar.sale_price

            total_price += price_to_use * item.quantity

        # Se crea el pedido en la base de datos.
        db_order = Order(
            user_id=user_id,
            order_date=date.today(),
            total_price=total_price,
            status=order.status,
            payment_method=order.payment_method,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Se crean los detalles del pedido y se actualiza el stock de las guitarras.
        for guitar, quantity in validated_items:
            order_detail = OrderDetail(
                order_id=db_order.id,
                guitar_id=guitar.id,
                quantity=quantity
            )
            db.add(order_detail)
            guitar.stock -= quantity

        db.commit()
        db.refresh(db_order)
        return db_order

    # Manejo de excepciones para errores específicos.
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el pedido: {str(e)}"
        )
        
# Función para obtener todos los pedidos paginados sin filtrar por usuario.
def get_all_orders_paginated(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    # Consulta base sin filtrar por usuario
    query = db.query(Order)

    # Obtener los pedidos paginados
    orders = query.offset(offset).limit(limit).all()

    # Contar el total
    total = query.count()

    return OrderListResponse(
        orders=orders,
        total=total
    )
        
# Función para los pedidos por id.
def get_order_by_id(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
        
    return db_order
    
# Función para obtener todos los pedidos.
def get_all_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

# Función para actualizar un pedido por id.
def update_order(db: Session, order_id: int, order_data: order_schema.OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    update_data = order_data.dict(exclude_unset=True)

    # Actualizamos todos los campos proporcionados en order_data
    for key, value in update_data.items():
        setattr(db_order, key, value)

    # Se guardan los datos en la base de datos.
    db.commit()
    db.refresh(db_order)
    return db_order

# Función para eliminar un pedido por id.
def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    # Se elimina el pedido de la base de datos.
    db.delete(db_order)
    db.commit()
    return db_order

# Función para obtener pedidos paginados.
def get_orders_paginated(db: Session, page: int, limit: int, user_id: int):
    # Calculamos el offset basado en la página y el límite.
    offset = (page - 1) * limit

    # Consultamos los pedidos con el offset y el limit.
    orders = db.query(Order).filter(Order.user_id == user_id).offset(offset).limit(limit).all()

    # Consultamos el total de pedidos.
    total_orders = db.query(Order).filter(Order.user_id == user_id).count()

    # Si no se encuentran pedidos, lanzamos una excepción.
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron pedidos en esta página."
        )

    # Devolvemos los pedidos junto con el total.
    return OrderListResponse(orders=orders, total=total_orders)

