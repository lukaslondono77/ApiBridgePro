# 🚀 ApiBridge Pro - Guía Rápida en Español

## ¿Qué es ApiBridge Pro?

ApiBridge Pro es un **puente universal para APIs** que te permite:
- Conectar cualquier API externa a través de un solo endpoint
- Unificar respuestas de diferentes proveedores (ej: múltiples APIs de clima)
- Controlar costos con presupuestos
- Proteger datos sensibles automáticamente
- Monitorear todo con métricas y dashboards

---

## 📦 Instalación

```bash
# Instalar el paquete
pip install apibridge-pro

# O instalar desde el código
cd ApiBridgePro
pip install -e .
```

---

## 🎯 Uso Básico

### Opción 1: Usar como servidor (Recomendado)

```bash
# Iniciar el servidor (puerto 8000 por defecto)
apibridge

# Con puerto personalizado
apibridge --port 9000

# Ver ayuda
apibridge --help
```

Luego accede a:
- **Dashboard:** http://localhost:8000/admin
- **Docs API:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

### Opción 2: Usar en código Python

```python
from apibridgepro import Gateway, BudgetGuard, build_connector_policies, load_config

# Cargar configuración
config = load_config("connectors.yaml")
policies = build_connector_policies(config)

# Crear guardián de presupuesto
budget = BudgetGuard(redis_url=None)  # Modo memoria
await budget.init()

# Crear gateway
gateway = Gateway(policies, budget)

# Usar el gateway
# (ver ejemplos más abajo)
```

---

## ⚙️ Configuración Básica

### 1. Configurar claves de API

Crea variables de entorno:

```bash
# En macOS/Linux (agrega a ~/.zshrc o ~/.bashrc)
export OPENWEATHER_KEY="tu_clave_aqui"
export WEATHERAPI_KEY="tu_clave_aqui"
export GITHUB_TOKEN="ghp_tu_token_aqui"

# Luego recarga:
source ~/.zshrc  # o source ~/.bashrc
```

### 2. Editar connectors.yaml

El archivo `connectors.yaml` define qué APIs conectas:

```yaml
connectors:
  github:
    base_url: https://api.github.com
    auth:
      type: bearer
      token: ${GITHUB_TOKEN}
    allow_paths:
      - /user
      - /users/.*
    
  weather_unified:
    providers:
      - name: openweather
        base_url: https://api.openweathermap.org/data/2.5
        auth:
          type: api_key_query
          key: ${OPENWEATHER_KEY}
      - name: weatherapi
        base_url: http://api.weatherapi.com/v1
        auth:
          type: api_key_query
          key: ${WEATHERAPI_KEY}
    transforms:
      response:
        jmes: "{temp_c: main.temp, humidity: main.humidity, provider: @}"
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Hacer request a GitHub

```bash
# Desde terminal
curl http://localhost:8000/proxy/github/user

# O desde Python
import requests
response = requests.get("http://localhost:8000/proxy/github/user")
print(response.json())
```

### Ejemplo 2: Clima unificado (múltiples APIs)

```bash
# ApiBridge automáticamente elige la API más rápida/disponible
curl "http://localhost:8000/proxy/weather_unified/weather?q=Bogota"
```

### Ejemplo 3: Usar programáticamente

```python
from fastapi import Request
from starlette.requests import Request as StarletteRequest

# Simular un request
request = Request(...)  # Tu objeto request
response = await gateway.proxy("github", "user", request)
```

---

## 🔒 Funciones Avanzadas

### Protección PII (Datos Sensibles)

```yaml
pii_protection:
  enabled: true
  auto_scan: true  # Detecta automáticamente emails, teléfonos, etc.
  action: redact   # Opciones: redact, encrypt, tokenize, hash
```

### Control de Presupuesto

```yaml
budget:
  monthly_usd: 100.0
  action: warn  # warn, block, or log
```

### Rate Limiting

```yaml
rate_limit:
  capacity: 100
  refill_per_sec: 10  # 100 requests cada 10 segundos
```

---

## 📊 Monitoreo

### Dashboard Web
Accede a: http://localhost:8000/admin

Muestra:
- Presupuesto usado
- Estado de proveedores
- Estadísticas de cache
- Rate limits

### Métricas Prometheus
```bash
curl http://localhost:8000/metrics
```

### Logs
Los logs incluyen:
- Requests procesados
- Errores
- Tiempo de respuesta
- Proveedores usados

---

## 🛠️ Comandos Útiles

```bash
# Ver salud del sistema
curl http://localhost:8000/health

# Ver métricas
curl http://localhost:8000/metrics

# Ver documentación API
open http://localhost:8000/docs

# Modo desarrollo (auto-reload)
apibridge  # Ya tiene auto-reload por defecto

# Modo producción (sin reload)
apibridge --no-reload
```

---

## 🎓 Casos de Uso Comunes

### 1. Unificar múltiples APIs de clima
```yaml
# ApiBridge elige automáticamente la más rápida
weather_unified:
  providers: [openweather, weatherapi, ...]
```

### 2. Normalizar respuestas diferentes
```yaml
transforms:
  response:
    jmes: "{temp: main.temp, humidity: main.humidity}"
```

### 3. Proteger datos sensibles
```yaml
pii_protection:
  enabled: true
  action: encrypt
```

### 4. Controlar costos
```yaml
budget:
  monthly_usd: 50.0
  action: block  # Bloquea si excede el límite
```

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito Redis?**  
R: No, funciona en memoria. Redis es opcional para presupuestos distribuidos.

**P: ¿Cómo agrego una nueva API?**  
R: Edita `connectors.yaml` y agrega una nueva entrada bajo `connectors:`

**P: ¿Puedo usar esto en producción?**  
R: Sí, está diseñado para producción. Usa `--no-reload` y configura variables de entorno.

**P: ¿Cómo veo qué está pasando?**  
R: Usa el dashboard en `/admin` o las métricas en `/metrics`

---

## 📚 Más Información

- GitHub: https://github.com/lukaslondono77/ApiBridgePro
- PyPI: https://pypi.org/project/apibridge-pro/
- Docs completos: Mira los archivos `.md` en el repositorio

---

## 🆘 Troubleshooting

**Error: "No module named apibridgepro"**  
→ Instala: `pip install apibridge-pro`

**Error: "CORS warning"**  
→ Configura: `export ALLOWED_ORIGINS=https://tudominio.com`

**Error: "API key not found"**  
→ Verifica variables de entorno con `env | grep KEY`

**El servidor no inicia**  
→ Verifica que el puerto 8000 esté libre: `lsof -i :8000`

---

¡Listo para empezar! 🎉

