from sqlalchemy.orm import Session
from app.models.order import Order
from fastapi import HTTPException, status
from app.schemas import order as order_schema
from app.schemas.order import OrderListResponse
from app.models.order_detail import OrderDetail
from app.models.guitar import Guitar
from datetime import date
from app.schemas.guitar import GuitarRead

### FUNCIONES PARA USUARIOS ADMIN ###

# Función para obtener las guitarras del usuario ordenadas por pedidos.
def get_user_ordered_guitars(db: Session, user_id: int):
    # Obtener todos los IDs de pedidos del usuario
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene pedidos registrados."
        )

    order_ids = [order.id for order in orders]

    # Obtener todos los detalles de pedido que coincidan con esos pedidos
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id.in_(order_ids)).all()
    if not order_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras en los pedidos del usuario."
        )

    # Obtener guitarras únicas basadas en los IDs de guitarra encontrados
    guitar_ids = list({detail.guitar_id for detail in order_details})
    guitars = db.query(Guitar).filter(Guitar.id.in_(guitar_ids)).all()

    return guitars

# Función para crear un nuevo pedido.
def create_order(db: Session, user_id: int, order: order_schema.OrderCreate):  
    try:
        if not order.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pedido debe contener al menos una guitarra con su cantidad."
            )

        # Validar existencia de guitarras y stock
        validated_items = []
        total_price = 0
        for item in order.items:
            guitar = db.query(Guitar).filter(Guitar.id == item.guitar_id).first()
            if not guitar:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Guitarra con ID {item.guitar_id} no encontrada."
                )
            if guitar.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No hay suficiente stock para la guitarra ID {item.guitar_id}."
                )

            # Determinar precio correcto
            price_to_use = guitar.liquidation_price if guitar.liquidation_price else guitar.sale_price

            # Guardar tupla con los datos necesarios
            validated_items.append((guitar, item.quantity, price_to_use))

            # Sumar al total del pedido
            total_price += price_to_use * item.quantity

        # Crear la orden
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

        # Crear los detalles del pedido y actualizar stock
        for guitar, quantity, price_to_use in validated_items:
            order_detail = OrderDetail(
                order_id=db_order.id,
                guitar_id=guitar.id,
                quantity=quantity,
                unit_price=price_to_use,
                total_price=price_to_use * quantity
            )
            db.add(order_detail)
            guitar.stock -= quantity

        db.commit()
        db.refresh(db_order)
        return db_order

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

    # Consulta base ordenada por ID ascendente
    query = db.query(Order).order_by(Order.id.asc())

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
    offset = (page - 1) * limit

    # Consultamos los pedidos del usuario ordenados por ID ascendente
    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Consultamos el total de pedidos del usuario
    total_orders = db.query(Order).filter(Order.user_id == user_id).count()

    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron pedidos en esta página."
        )

    return OrderListResponse(orders=orders, total=total_orders)
