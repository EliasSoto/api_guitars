import bcrypt, re
from datetime import date, datetime

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Función para verificar si la contraseña es correcta
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Función para validar el dígito verificador del RUT.
def calculate_check_digit(rut: str) -> str:
    rut = rut[::-1]
    multipliers = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]
    total = sum(int(rut[i]) * multipliers[i] for i in range(len(rut)))
    rest = total % 11
    check_digit = 11 - rest
    if check_digit == 11:
        return '0'
    elif check_digit == 10:
        return 'K'
    return str(check_digit)

# Función para validar el RUT completo.
def validate_rut(rut: str) -> str:
    if len(rut) < 9 or len(rut) > 10:
        raise ValueError('El RUT debe tener entre 9 y 10 caracteres y guión "-"')
    
    # Se eliminan los púntos y se convierte a mayúsculas.
    rut = re.sub(r'\.', '', rut).upper()
    
    # Se verifica que el RUT tenga un formato válido.
    if not re.match(r'^\d{7,8}-[0-9K]$', rut):
        raise ValueError('El RUT debe tener el formato 12.345.678-K.')
    
    # Se separa el RUT y el dígito verificador.
    rut_numeric = rut[:-2]
    check_digit = rut[-1]
    
    calculated_check_digit = calculate_check_digit(rut_numeric)
    
    # Se comprueba el dígito verificador con la función para verificar.
    if calculated_check_digit != check_digit:
        raise ValueError(f'El dígito verificador del RUT: {rut} es incorrecto.')
    
    return rut

# Validación del número de teléfono.
def validate_phone_number(phone: str):
    if phone is None:
        return phone
    
    phone_clean = re.sub(r'\D', '', phone)  # Se eliminan los caracteres no numéricos.
    if len(phone_clean) != 9:
        raise ValueError('El número de teléfono debe tener 9 dígitos.')
    return phone_clean

# Validación de la fecha de nacimiento.
def validate_birth_date(birth_date: str) -> str:
    try:
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")
    
    today = date.today()
    age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
    if age < 13 or age > 65:
        raise ValueError("La edad debe estar entre 13 y 65 años.")
    
    return birth_date

# Validación de la fecha de nacimiento para administradores.
def validate_birth_date_admin(birth_date: str) -> str:
    try:
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")
    
    today = date.today()
    age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
    if age < 18 or age > 65:
        raise ValueError("La edad debe estar entre 18 y 65 años.")
    
    return birth_date