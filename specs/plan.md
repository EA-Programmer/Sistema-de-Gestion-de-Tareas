# Plan tecnico de desarrollo

## Enfoque Spec Driven Development

El proyecto sigue el flujo de Spec Kit: Spec -> Plan -> Tasks -> Implement. Primero se define la especificacion funcional, despues el plan tecnico, luego las tareas y finalmente la implementacion.

## Arquitectura

- Frontend: HTML, Tailwind por CDN, TypeScript en `frontend/src/app.ts` y JavaScript compilado en `frontend/dist/app.js`.
- Backend: Python con `http.server`, API REST y persistencia en `backend/data/tasks.json`.
- Persistencia: archivo JSON local con arreglo de tareas.
- Control de versiones: ramas por fase y commits atomicos.

## Decisiones tecnicas

- Se usa Python estandar para evitar dependencias externas y facilitar la ejecucion.
- La API devuelve JSON y habilita CORS para permitir consumo desde el frontend.
- El frontend maneja formularios, filtros, edicion, eliminacion y resumen desde una sola pantalla.
- Tailwind se carga desde CDN para cumplir el requisito visual sin configurar build complejo.

## Flujo de ramas propuesto

- `main`: rama estable.
- `feature/specs`: especificacion, plan y tareas.
- `feature/backend`: API REST y pruebas del backend.
- `feature/frontend`: interfaz web y consumo de API.
- `docs/readme`: documentacion final y evidencias.

## Pruebas

- Pruebas unitarias del backend para crear, listar, filtrar, actualizar, eliminar y generar resumen.
- Prueba manual del frontend con el servidor backend activo.

## Riesgos

- GitHub y pull requests dependen de tener un repositorio remoto creado y accesible.
- Si el navegador no tiene sesion activa de GitHub, el usuario debera iniciar sesion.
