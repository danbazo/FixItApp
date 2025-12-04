Sprint 0 — Preparación (1 día)

Crear repo, ramas backend y frontend.

Inicializar README, /docs, wireframes.

Crear entorno local: Python venv, Node, Postgres.

Sprint 1 — Backend inicial (5 días)

Estructura FastAPI (routers, services, models).

Configurar SQLAlchemy y Alembic.

Crear tablas base (users, specialties, technician_profiles).

Seed inicial: populate specialties con rubros.

Endpoints auth (register/login) con JWT.

Entregable: auth + modelos basicos + migraciones.

Sprint 2 — Perfil técnico + certificados (4 días)

Endpoints CRUD technician_profiles.

Endpoint para subir archivos (dev: guardar local; prod: S3).

Implementar technician_specialties CRUD en create/update flujo (subir certificado por rubro).

Admin endpoints para aprobar/rechazar certificados y ver DNI.

Entregable: registro técnico por rubro con subida de archivos + panel admin básico.

Sprint 3 — WorkRequests & Invitations (4 días)

Endpoints para work_requests (crear/listar/GET).

Endpoint /work_requests/{id}/invite que crea work_request_technicians.

Endpoint listar técnicos con filtros (specialty, barrio, visible).

Guardar fotos (S3) como array de URLs.

Entregable: crear trabajo + invitar técnicos + ver en dashboard.

Sprint 4 — Quotes & Quote Items (3 días)

Endpoints para quotes, quote_items.

Validaciones: solo técnicos invitados pueden cotizar (o implementar opción publica más tarde).

Endpoint cliente para ver/aceptar cotización.

Entregable: flujo básico de cotización.

Sprint 5 — Reviews, cálculo rating y tests (3 días)

Endpoints reviews.

Job/trigger para recalcular rating_avg en technician_profiles.

Tests básicos (Pytest) para auth, creación de work_request y quotes.

Entregable: reviews y cálculo de rating.

Sprint 6 — Frontend MVP (10 días, paralelo con sprints anteriores si podés)

Setup React + Vite + Tailwind.

Páginas: Login/Register, Dashboard cliente, Crear trabajo, Seleccionar técnicos, Ver presupuestos, Perfil técnico, Dashboard técnico, Panel admin.

Integrar llamadas API (Axios).

Manejo de JWT (almacenar en localStorage, interceptores).

Upload images (clientes y técnicos).

Estilado básico responsive.

Entregable: frontend funcional conectado a backend.

Sprint 7 — Deploy & Docs (3-5 días)

Deploy backend en Railway/Render (rápido).

DB en Neon / Supabase / RDS.

Frontend en Vercel.

S3 + IAM para archivos (o usar Cloudinary para acelerar).

README con URLs, instrucciones y vídeo demo corto.
