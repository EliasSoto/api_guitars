# 🎸 Guitarras Personalizadas — API (FastAPI)

Backend del proyecto web para la **venta y personalización de guitarras eléctricas**.  
Permite a los usuarios registrarse, crear pedidos personalizados, gestionar envíos, calificar guitarras y explorar un catálogo de guitarras preensambladas.

---

## 🚀 Tecnologías

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- JWT (Auth)
- PostgreSQL

---

## 🔧 Instalación del Proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/EliasSoto/api_guitarras.git
   ```

2. **Entrar al directorio**
   ```bash
   cd api_guitars
   ```

3. **Crear un entorno virtual**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Iniciar servidor de desarrollo**
   ```bash
   uvicorn app.main:app --reload
   ```

---

### ⚙️ Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# URL de conexión a la base de datos (compatible con PostgreSQL y servicios como Supabase)
URL_DATABASE=postgresql://usuario:contraseña@host:puerto/nombre_base_de_datos

# Configuración para autenticación JWT
SECRET_KEY_TOKEN=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

---

## 📁 Estructura de carpetas

```bash
.
├── core/              # Configuración principal del proyecto (seguridad, dependencias, auth, etc.)
├── database/          # Conexión a la base de datos y manejo de sesiones
├── models/            # Modelos SQLAlchemy que representan las tablas de la base de datos
├── repositories/      # Lógica de acceso a datos (CRUD y queries personalizados)
├── routers/           # Endpoints de la API organizados por entidad o funcionalidad
├── schemas/           # Esquemas Pydantic para validaciones de entrada/salida
├── utils/             # Funciones auxiliares (formato, validaciones, etc.)
├── main.py            # Punto de entrada principal del servidor FastAPI
└── .env               # Variables de entorno (nunca debe subirse al repositorio)
```

## ▶️ Ejecución y Documentación Interactiva

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

Abrir en el navegador:

```bash
http://127.0.0.1:8000/docs
```

---

## ✅ Estado del Proyecto

- ✅ Registro y login con JWT
- ✅ Gestión de usuarios y direcciones
- ✅ Catálogo de guitarras
- ✅ Guitarras personalizadas por usuarios
- ✅ Pedidos y seguimiento de envíos
- ✅ Reseñas por usuario y promedio por guitarra
- ✅ Wishlist de guitarras
- ✅ Roles diferenciados (usuario / admin)
- ✅ Paginación, validaciones y filtros

---

## 🧑‍💻 Autores

Desarrollado por **Elías Soto** **Álvaro Ramos** — 2025