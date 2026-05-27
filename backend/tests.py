import tempfile
import unittest
from pathlib import Path

from app import NotFoundError, TaskStore, ValidationError


VALID_TASK = {
    "title": "Practica de programacion movil",
    "description": "Construir aplicacion TaskCampus",
    "subject": "Programacion Movil",
    "due_date": "2026-05-22",
    "priority": "alta",
    "status": "pendiente",
}


class TaskStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.store = TaskStore(Path(self.tmp.name) / "tasks.json")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_create_and_list_task(self) -> None:
        task = self.store.create_task(VALID_TASK)

        self.assertEqual(task["id"], 1)
        self.assertEqual(len(self.store.list_tasks()), 1)

    def test_filter_tasks(self) -> None:
        self.store.create_task(VALID_TASK)
        self.store.create_task(
            {
                **VALID_TASK,
                "title": "Lectura",
                "subject": "Etica",
                "priority": "media",
                "status": "finalizada",
            }
        )

        self.assertEqual(len(self.store.list_tasks({"priority": "alta"})), 1)
        self.assertEqual(len(self.store.list_tasks({"status": "finalizada"})), 1)
        self.assertEqual(len(self.store.list_tasks({"subject": "movi"})), 1)

    def test_update_task(self) -> None:
        task = self.store.create_task(VALID_TASK)

        updated = self.store.update_task(task["id"], {"status": "en proceso"})

        self.assertEqual(updated["status"], "en proceso")

    def test_delete_task(self) -> None:
        task = self.store.create_task(VALID_TASK)

        self.store.delete_task(task["id"])

        self.assertEqual(self.store.list_tasks(), [])

    def test_summary(self) -> None:
        self.store.create_task(VALID_TASK)
        self.store.create_task({**VALID_TASK, "title": "Ensayo", "status": "finalizada", "priority": "baja"})

        summary = self.store.summary()

        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["finished"], 1)
        self.assertEqual(summary["high_priority"], 1)

    def test_invalid_priority(self) -> None:
        with self.assertRaises(ValidationError):
            self.store.create_task({**VALID_TASK, "priority": "urgente"})

    def test_not_found(self) -> None:
        with self.assertRaises(NotFoundError):
            self.store.get_task(99)


if __name__ == "__main__":
    unittest.main()
