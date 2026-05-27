from __future__ import annotations

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


DATA_FILE = Path(__file__).parent / "data" / "tasks.json"
ALLOWED_PRIORITIES = {"baja", "media", "alta"}
ALLOWED_STATUSES = {"pendiente", "en proceso", "finalizada"}


class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskStore:
    def __init__(self, path: Path = DATA_FILE) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_tasks(self, filters: dict[str, str] | None = None) -> list[dict[str, Any]]:
        tasks = self._read()
        filters = filters or {}

        status = filters.get("status", "").strip().lower()
        priority = filters.get("priority", "").strip().lower()
        subject = filters.get("subject", "").strip().lower()

        if status:
            tasks = [task for task in tasks if task["status"].lower() == status]
        if priority:
            tasks = [task for task in tasks if task["priority"].lower() == priority]
        if subject:
            tasks = [task for task in tasks if subject in task["subject"].lower()]

        return tasks

    def get_task(self, task_id: int) -> dict[str, Any]:
        for task in self._read():
            if task["id"] == task_id:
                return task
        raise NotFoundError("Tarea no encontrada")

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        tasks = self._read()
        clean = self._validate(payload, partial=False)
        timestamp = now_iso()
        task = {
            "id": self._next_id(tasks),
            **clean,
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        tasks.append(task)
        self._write(tasks)
        return task

    def update_task(self, task_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        tasks = self._read()
        clean = self._validate(payload, partial=True)
        if not clean:
            raise ValidationError("Debe enviar al menos un campo para actualizar")

        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                updated = {**task, **clean, "updated_at": now_iso()}
                tasks[index] = updated
                self._write(tasks)
                return updated
        raise NotFoundError("Tarea no encontrada")

    def delete_task(self, task_id: int) -> None:
        tasks = self._read()
        remaining = [task for task in tasks if task["id"] != task_id]
        if len(remaining) == len(tasks):
            raise NotFoundError("Tarea no encontrada")
        self._write(remaining)

    def summary(self) -> dict[str, int]:
        tasks = self._read()
        return {
            "total": len(tasks),
            "pending": sum(1 for task in tasks if task["status"] == "pendiente"),
            "finished": sum(1 for task in tasks if task["status"] == "finalizada"),
            "high_priority": sum(1 for task in tasks if task["priority"] == "alta"),
        }

    def _read(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValidationError("El archivo JSON de tareas esta corrupto") from exc

    def _write(self, tasks: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

    def _next_id(self, tasks: list[dict[str, Any]]) -> int:
        return max((int(task["id"]) for task in tasks), default=0) + 1

    def _validate(self, payload: dict[str, Any], partial: bool) -> dict[str, str]:
        fields = ["title", "description", "subject", "due_date", "priority", "status"]
        required = [] if partial else fields
        errors: list[str] = []
        clean: dict[str, str] = {}

        for field in required:
            if not str(payload.get(field, "")).strip():
                errors.append(f"{field} es obligatorio")

        for field in fields:
            if field in payload:
                value = str(payload.get(field, "")).strip()
                if not value:
                    errors.append(f"{field} no puede estar vacio")
                clean[field] = value

        if "priority" in clean:
            clean["priority"] = clean["priority"].lower()
            if clean["priority"] not in ALLOWED_PRIORITIES:
                errors.append("priority debe ser baja, media o alta")

        if "status" in clean:
            clean["status"] = clean["status"].lower()
            if clean["status"] not in ALLOWED_STATUSES:
                errors.append("status debe ser pendiente, en proceso o finalizada")

        if "due_date" in clean:
            try:
                datetime.strptime(clean["due_date"], "%Y-%m-%d")
            except ValueError:
                errors.append("due_date debe usar formato YYYY-MM-DD")

        if errors:
            raise ValidationError("; ".join(errors))
        return clean


class TaskCampusHandler(BaseHTTPRequestHandler):
    store = TaskStore()

    def do_OPTIONS(self) -> None:
        self._send_json({"ok": True})

    def do_GET(self) -> None:
        try:
            path, query = self._parsed_request()
            if path == "/tasks":
                filters = {key: values[0] for key, values in query.items() if values and values[0]}
                self._send_json(self.store.list_tasks(filters))
                return
            if path == "/tasks/summary":
                self._send_json(self.store.summary())
                return
            task_id = self._task_id_from_path(path)
            if task_id is not None:
                self._send_json(self.store.get_task(task_id))
                return
            self._send_error(404, "Ruta no encontrada")
        except NotFoundError as exc:
            self._send_error(404, str(exc))
        except ValidationError as exc:
            self._send_error(400, str(exc))

    def do_POST(self) -> None:
        try:
            if self._parsed_request()[0] != "/tasks":
                self._send_error(404, "Ruta no encontrada")
                return
            task = self.store.create_task(self._read_json())
            self._send_json(task, status=201)
        except ValidationError as exc:
            self._send_error(400, str(exc))

    def do_PUT(self) -> None:
        try:
            task_id = self._task_id_from_path(self._parsed_request()[0])
            if task_id is None:
                self._send_error(404, "Ruta no encontrada")
                return
            task = self.store.update_task(task_id, self._read_json())
            self._send_json(task)
        except NotFoundError as exc:
            self._send_error(404, str(exc))
        except ValidationError as exc:
            self._send_error(400, str(exc))

    def do_DELETE(self) -> None:
        try:
            task_id = self._task_id_from_path(self._parsed_request()[0])
            if task_id is None:
                self._send_error(404, "Ruta no encontrada")
                return
            self.store.delete_task(task_id)
            self._send_json({"message": "Tarea eliminada"})
        except NotFoundError as exc:
            self._send_error(404, str(exc))

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValidationError("JSON invalido") from exc
        if not isinstance(payload, dict):
            raise ValidationError("El cuerpo debe ser un objeto JSON")
        return payload

    def _parsed_request(self) -> tuple[str, dict[str, list[str]]]:
        parsed = urlparse(self.path)
        return parsed.path.rstrip("/") or "/", parse_qs(parsed.query)

    def _task_id_from_path(self, path: str) -> int | None:
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "tasks" and parts[1].isdigit():
            return int(parts[1])
        return None

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: int, message: str) -> None:
        self._send_json({"error": message}, status=status)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), TaskCampusHandler)
    print(f"TaskCampus API en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
