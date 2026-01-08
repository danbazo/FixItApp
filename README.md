# FixIt — Marketplace de Servicios del Hogar

FixIt es una plataforma que conecta **técnicos certificados** con **usuarios** que necesitan servicios de plomería, electricidad, gas, pintura, cerámicos, mantenimiento general y más.  
El objetivo es ofrecer un sistema simple y confiable para encontrar profesionales calificados, solicitar presupuestos y gestionar trabajos del hogar.

---

## Estado del proyecto
Actualmente en **Fase 0 — Diseño del MVP, arquitectura inicial y definición funcional**.

---

## Objetivo del MVP
Crear una plataforma funcional que permita:

- Registro y login de usuarios (clientes y técnicos).
- Búsqueda de técnicos por categoría o ubicación.
- Perfiles de técnicos con certificaciones, experiencia y reseñas.
- Solicitud y respuesta de presupuestos entre usuarios y técnicos.
- Panel de administrador para aprobar técnicos y gestionar el sistema.

---

## Tecnologías principales

### Backend
- **Python + FastAPI**
- **PostgreSQL**
- **SQLAlchemy / Prisma / Tortoise ORM (por definir)**
- **Auth con JWT**
- **Docker (opcional)**

### Frontend
- **React + Vite**
- **TailwindCSS o Chakra UI**
- **React Query para manejo de estado de datos**

### Infraestructura (futuro)
- **AWS Lambda + API Gateway**
- **AWS RDS (o Supabase)**
- **AWS S3** para imágenes y documentos

---

## Estructura del repositorio

/backend → Aplicación FastAPI
/frontend → Aplicación React
/docs → Documentación


## Roadmap de versiones

### MVP v0.1
- Registro/login
- CRUD de técnicos
- Solicitud de presupuestos

### v0.2
- Reviews y rating
- Panel de administrador

### v0.3
- Carga de imágenes y certificaciones

### v1.0
- Implementación en AWS
- Mejoras UX/UI

---

## Contribuciones
Proyecto personal en desarrollo — abierto a feedback, sugerencias y mejoras.
