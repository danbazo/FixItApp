Flujo: creación de trabajo → invitación → presupuesto → aceptación → review

Cliente inicia sesión → Click en "Crear nuevo trabajo".

Cliente completa WorkRequest: título, descripción, fotos, barrio → Envía.

Sistema guarda work_requests (status: open).

Cliente selecciona técnicos de la lista (filtrada por specialty + barrio) → crea registros en work_request_technicians → cambia work_request.status a awaiting_quotes.

Notificación (email/opcional) → técnicos invitados reciben aviso en su dashboard.

Técnico accede, revisa fotos y descripción. Si necesita más info puede:

Enviar mensaje (si chat implementado) o solicitar más info por función futura.

Técnico hace POST /quotes con quote_items (desglose) → status sent.

Cliente visualiza presupuestos en la vista del work_request.

Cliente compara y acepta uno: cambiar quotes.status a accepted, work_request.status a closed (o a in_progress si querés).

Post-trabajo: cliente evalúa → crear reviews con target_id = technician.user_id.

Admin revisa certificados: por cada technician_specialty con certificate_status='pending', el admin aprueba/rechaza; al aprobar se actualiza visible = true.

Puntos de control:

Un rubro no aprobado no aparece en búsquedas públicas (filtrar visible=true).

DNI y certificado visibles para admin y almacenados en files o technician_certificates.
