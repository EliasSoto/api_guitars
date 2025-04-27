import bcrypt, re
from datetime import datetime

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

# Validación del formato de la fecha de nacimiento y rango aceptable.
def validate_birth_date(birth_date: str) -> str:
    if birth_date is None:
        return birth_date
    
    # Validación precisa del formato DD/MM/YYYY.
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
    if not re.match(pattern, birth_date):
        raise ValueError('La fecha de nacimiento debe tener el formato DD/MM/YYYY y ser una fecha válida.')
    
    # Se obtiene separa la fecha en partes.
    day, month, year = map(int, birth_date.split('/'))
    
    # Se obtiene la fecha actual y se calcula la edad mínima.
    current_date = datetime.now()
    
    # Se crea una fecha con el año, mes y día de nacimiento.
    new_birth_date = datetime(year, month, day)
            
    # Se verifica que la fecha de nacimiento no se posterior a a la fecha actual.
    if new_birth_date > current_date:
        raise ValueError('La fecha de nacimiento no puede ser posterior a la fecha actual.')
    
    # Se verifica que la fecha de nacimiento no anterior al 1900.
    if year < 1900:
        raise ValueError('La fecha de nacimiento no puede ser anterior al año 1900.')
    
    return birth_date