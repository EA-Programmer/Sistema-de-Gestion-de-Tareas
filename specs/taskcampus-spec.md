# Especificacion del sistema TaskCampus

## Problema

Los estudiantes universitarios necesitan organizar tareas academicas, fechas de entrega y estados de avance en un solo lugar.

## Objetivo

Desarrollar una aplicacion web para registrar, consultar, actualizar y eliminar tareas academicas, con filtros y resumen estadistico.

## Usuarios

Estudiantes universitarios que gestionan actividades de distintas asignaturas.

## Historias de usuario

- Como estudiante, quiero registrar tareas para organizar mis actividades.
- Como estudiante, quiero listar mis tareas para revisar todo lo pendiente.
- Como estudiante, quiero filtrar tareas por estado para identificar mis pendientes.
- Como estudiante, quiero filtrar tareas por prioridad para atender primero lo urgente.
- Como estudiante, quiero filtrar tareas por asignatura para enfocarme en una materia.
- Como estudiante, quiero editar tareas para corregir datos o actualizar su avance.
- Como estudiante, quiero eliminar tareas para mantener limpia mi lista.
- Como estudiante, quiero marcar tareas como finalizadas para controlar mi avance.
- Como estudiante, quiero ver un resumen para conocer mi carga academica.

## Requisitos funcionales

- RF01. Registrar tareas con titulo, descripcion, asignatura, fecha de entrega, prioridad y estado.
- RF02. Listar todas las tareas registradas.
- RF03. Consultar una tarea por identificador.
- RF04. Editar una tarea existente.
- RF05. Eliminar una tarea.
- RF06. Filtrar tareas por estado.
- RF07. Filtrar tareas por prioridad.
- RF08. Filtrar tareas por asignatura.
- RF09. Mostrar resumen con total de tareas, tareas pendientes, tareas finalizadas y tareas de alta prioridad.

## Requisitos no funcionales

- RNF01. La interfaz debe ser clara, sencilla y usable en pantallas de escritorio.
- RNF02. El backend debe exponer una API REST.
- RNF03. El backend debe persistir los datos en un archivo JSON.
- RNF04. El frontend debe estar desarrollado con TypeScript, HTML y Tailwind.
- RNF05. El codigo debe estar versionado con Git y publicado en GitHub.
- RNF06. El proyecto debe incluir documentacion de instalacion, ejecucion y endpoints.

## Modelo de datos

Una tarea contiene:

- id: identificador entero unico.
- title: titulo obligatorio.
- description: descripcion obligatoria.
- subject: asignatura obligatoria.
- due_date: fecha de entrega en formato YYYY-MM-DD.
- priority: baja, media o alta.
- status: pendiente, en proceso o finalizada.
- created_at: fecha de creacion en formato ISO 8601.
- updated_at: fecha de actualizacion en formato ISO 8601.

## Reglas de negocio

- El titulo, descripcion, asignatura y fecha de entrega son obligatorios.
- La prioridad solo puede ser baja, media o alta.
- El estado solo puede ser pendiente, en proceso o finalizada.
- Los filtros son opcionales y pueden combinarse.
- Si una tarea no existe, la API debe responder 404.
- Si los datos enviados son invalidos, la API debe responder 400.

## Endpoints

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | /tasks | Listar tareas y aplicar filtros opcionales |
| GET | /tasks/{id} | Consultar tarea |
| POST | /tasks | Crear tarea |
| PUT | /tasks/{id} | Actualizar tarea |
| DELETE | /tasks/{id} | Eliminar tarea |
| GET | /tasks/summary | Mostrar resumen |

## Criterios de aceptacion

- CA01. Al crear una tarea valida, el sistema la guarda y devuelve sus datos con un id.
- CA02. Al listar tareas, el sistema devuelve todas las tareas persistidas.
- CA03. Al filtrar por estado, prioridad o asignatura, el sistema devuelve solo coincidencias.
- CA04. Al editar una tarea, el sistema actualiza los campos enviados.
- CA05. Al eliminar una tarea, esta deja de aparecer en el listado.
- CA06. El resumen refleja los totales actuales despues de crear, editar o eliminar tareas.
- CA07. El frontend permite ejecutar las operaciones principales consumiendo la API REST.
