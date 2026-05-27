# TaskCampus

TaskCampus es una aplicacion web para gestionar tareas academicas. Permite registrar, listar, filtrar, editar, eliminar y ver un resumen de tareas estudiantiles.

El proyecto fue desarrollado con enfoque Spec Driven Development siguiendo el flujo de Spec Kit: especificacion, plan, tareas e implementacion.

## Estructura

```text
taskcampus/
├── specs/
│   ├── taskcampus-spec.md
│   ├── plan.md
│   └── tasks.md
├── frontend/
│   ├── index.html
│   ├── src/app.ts
│   └── dist/app.js
├── backend/
│   ├── app.py
│   ├── tests.py
│   └── data/tasks.json
├── README.md
└── .gitignore
```

## Tecnologias

- Frontend: HTML, Tailwind y TypeScript.
- Backend: Python.
- Persistencia: archivo JSON.
- Control de versiones: Git y GitHub.

## Instalacion del backend

No requiere instalar dependencias externas.

```bash
cd backend
python app.py
```

La API queda disponible en:

```text
http://127.0.0.1:8000
```

## Instalacion del frontend

Para abrir el frontend con servidor local:

```bash
cd frontend
python -m http.server 5173
```

Abrir en el navegador:

```text
http://127.0.0.1:5173
```

El archivo TypeScript principal esta en `frontend/src/app.ts`. El JavaScript listo para navegador esta en `frontend/dist/app.js`.

Opcionalmente, para recompilar TypeScript:

```bash
cd frontend
npm install
npm run build
```

## Endpoints disponibles

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/tasks` | Listar tareas y filtrar por `status`, `priority` o `subject` |
| GET | `/tasks/{id}` | Consultar una tarea |
| POST | `/tasks` | Crear una tarea |
| PUT | `/tasks/{id}` | Actualizar una tarea |
| DELETE | `/tasks/{id}` | Eliminar una tarea |
| GET | `/tasks/summary` | Mostrar resumen estadistico |

## Ejemplo de tarea

```json
{
  "title": "Practica de programacion movil",
  "description": "Construir aplicacion TaskCampus",
  "subject": "Programacion Movil",
  "due_date": "2026-05-22",
  "priority": "alta",
  "status": "pendiente"
}
```

## Pruebas

Ejecutar pruebas del backend:

```bash
cd backend
python -m unittest tests.py
```

Tambien se realizo una prueba manual desde el frontend creando una tarea, verificando que el resumen se actualice y limpiando los datos de prueba.

## Flujo Git y GitHub

Repositorio remoto:

```text
https://github.com/EA-Programmer/Sistema-de-Gestion-de-Tareas.git
```

Ramas usadas:

- `main`: rama estable.
- `feature/backend`: implementacion de API REST.
- `feature/frontend`: implementacion de interfaz TypeScript.
- `docs/readme`: documentacion final.

Commits principales:

- `docs: define TaskCampus specification`
- `feat: implement Python task API`
- `feat: build TypeScript task interface`
- `docs: document installation and delivery`

Comandos usados para publicar:

```bash
git remote add origin https://github.com/EA-Programmer/Sistema-de-Gestion-de-Tareas.git
git push -u origin main
git push -u origin feature/backend
git push -u origin feature/frontend
git push -u origin docs/readme
```

Pull requests creados como evidencia:

- PR #1: `feature/backend` hacia `main`.
- PR #2: `feature/frontend` hacia `main`.
- PR #3: `docs/readme` hacia `main`.

## Integrantes

- Elias Astudillo
