from sqlalchemy.orm import Session
from app.models.order import Order
from fastapi import HTTPException, status
from app.schemas import order as order_schema
from app.schemas.order import OrderListResponse
from app.models.order_detail import OrderDetail

### FUNCIONES PARA USUARIOS ADMIN ###

# Función para crear una nuevo pedido.
def create_order(db: Session, user_id: int, order: order_schema.OrderCreate):  
    try:
        # Crear el pedido
        db_order = Order(
            user_id=user_id,
            order_date=order.order_date,
            total_price=order.total_price,
            status=order.status,
            payment_method=order.payment_method,
            quantity=order.quantity,
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Crear registros en OrderDetail para cada guitarra
        for guitar_id in order.guitar_ids:
            order_detail = OrderDetail(order_id=db_order.id, guitar_id=guitar_id)
            db.add(order_detail)

        db.commit()  # Confirmar los detalles

        # Obtener los guitar_ids desde OrderDetail
        guitar_ids = db.query(OrderDetail.guitar_id).filter(OrderDetail.order_id == db_order.id).all()
        db_order.guitar_ids = [g[0] for g in guitar_ids]

        return db_order

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el pedido: {str(e)}"
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