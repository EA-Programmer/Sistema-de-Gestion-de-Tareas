type Priority = "baja" | "media" | "alta";
type TaskStatus = "pendiente" | "en proceso" | "finalizada";

interface Task {
  id: number;
  title: string;
  description: string;
  subject: string;
  due_date: string;
  priority: Priority;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

interface Summary {
  total: number;
  pending: number;
  finished: number;
  high_priority: number;
}

const API_URL = "http://127.0.0.1:8000";

const elements = {
  apiStatus: document.querySelector<HTMLDivElement>("#apiStatus")!,
  taskForm: document.querySelector<HTMLFormElement>("#taskForm")!,
  taskId: document.querySelector<HTMLInputElement>("#taskId")!,
  title: document.querySelector<HTMLInputElement>("#title")!,
  description: document.querySelector<HTMLTextAreaElement>("#description")!,
  subject: document.querySelector<HTMLInputElement>("#subject")!,
  dueDate: document.querySelector<HTMLInputElement>("#dueDate")!,
  priority: document.querySelector<HTMLSelectElement>("#priority")!,
  status: document.querySelector<HTMLSelectElement>("#status")!,
  formTitle: document.querySelector<HTMLHeadingElement>("#formTitle")!,
  submitBtn: document.querySelector<HTMLButtonElement>("#submitBtn")!,
  cancelEditBtn: document.querySelector<HTMLButtonElement>("#cancelEditBtn")!,
  formMessage: document.querySelector<HTMLParagraphElement>("#formMessage")!,
  filterSubject: document.querySelector<HTMLInputElement>("#filterSubject")!,
  filterStatus: document.querySelector<HTMLSelectElement>("#filterStatus")!,
  filterPriority: document.querySelector<HTMLSelectElement>("#filterPriority")!,
  clearFiltersBtn: document.querySelector<HTMLButtonElement>("#clearFiltersBtn")!,
  taskList: document.querySelector<HTMLDivElement>("#taskList")!,
  emptyState: document.querySelector<HTMLParagraphElement>("#emptyState")!,
  summaryTotal: document.querySelector<HTMLElement>("#summaryTotal")!,
  summaryPending: document.querySelector<HTMLElement>("#summaryPending")!,
  summaryFinished: document.querySelector<HTMLElement>("#summaryFinished")!,
  summaryHigh: document.querySelector<HTMLElement>("#summaryHigh")!,
};

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Error inesperado");
  }
  return data as T;
}

function buildQuery(): string {
  const params = new URLSearchParams();
  if (elements.filterSubject.value.trim()) params.set("subject", elements.filterSubject.value.trim());
  if (elements.filterStatus.value) params.set("status", elements.filterStatus.value);
  if (elements.filterPriority.value) params.set("priority", elements.filterPriority.value);
  const query = params.toString();
  return query ? `?${query}` : "";
}

async function loadTasks(): Promise<void> {
  try {
    const [tasks, summary] = await Promise.all([
      request<Task[]>(`/tasks${buildQuery()}`),
      request<Summary>("/tasks/summary"),
    ]);
    renderTasks(tasks);
    renderSummary(summary);
    setApiStatus(true);
  } catch (error) {
    setApiStatus(false);
    showMessage(error instanceof Error ? error.message : "No se pudo conectar con la API", true);
  }
}

function renderSummary(summary: Summary): void {
  elements.summaryTotal.textContent = String(summary.total);
  elements.summaryPending.textContent = String(summary.pending);
  elements.summaryFinished.textContent = String(summary.finished);
  elements.summaryHigh.textContent = String(summary.high_priority);
}

function renderTasks(tasks: Task[]): void {
  elements.taskList.innerHTML = "";
  elements.emptyState.classList.toggle("hidden", tasks.length > 0);

  for (const task of tasks) {
    const card = document.createElement("article");
    card.className = "rounded border border-slate-300 bg-white p-4 shadow-sm";
    card.innerHTML = `
      <div class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div class="min-w-0">
          <h3 class="text-lg font-semibold">${escapeHtml(task.title)}</h3>
          <p class="mt-1 text-sm text-slate-700">${escapeHtml(task.description)}</p>
          <p class="mt-2 text-sm text-slate-600">${escapeHtml(task.subject)} | Entrega: ${escapeHtml(task.due_date)}</p>
        </div>
        <div class="flex flex-wrap gap-2 md:justify-end">
          <span class="${priorityClass(task.priority)} rounded px-2 py-1 text-xs font-semibold">${label(task.priority)}</span>
          <span class="${statusClass(task.status)} rounded px-2 py-1 text-xs font-semibold">${label(task.status)}</span>
        </div>
      </div>
      <div class="mt-4 flex flex-wrap gap-2">
        <button class="edit-btn rounded border border-slate-300 px-3 py-2 text-sm font-semibold hover:bg-slate-100" type="button">Editar</button>
        <button class="delete-btn rounded bg-rose-700 px-3 py-2 text-sm font-semibold text-white hover:bg-rose-800" type="button">Eliminar</button>
      </div>
    `;

    card.querySelector<HTMLButtonElement>(".edit-btn")!.addEventListener("click", () => startEdit(task));
    card.querySelector<HTMLButtonElement>(".delete-btn")!.addEventListener("click", () => deleteTask(task.id));
    elements.taskList.appendChild(card);
  }
}

async function saveTask(event: SubmitEvent): Promise<void> {
  event.preventDefault();
  const payload = {
    title: elements.title.value.trim(),
    description: elements.description.value.trim(),
    subject: elements.subject.value.trim(),
    due_date: elements.dueDate.value,
    priority: elements.priority.value,
    status: elements.status.value,
  };
  const editingId = elements.taskId.value;

  try {
    if (editingId) {
      await request<Task>(`/tasks/${editingId}`, { method: "PUT", body: JSON.stringify(payload) });
      showMessage("Tarea actualizada.");
    } else {
      await request<Task>("/tasks", { method: "POST", body: JSON.stringify(payload) });
      showMessage("Tarea registrada.");
    }
    resetForm();
    await loadTasks();
  } catch (error) {
    showMessage(error instanceof Error ? error.message : "No se pudo guardar", true);
  }
}

function startEdit(task: Task): void {
  elements.taskId.value = String(task.id);
  elements.title.value = task.title;
  elements.description.value = task.description;
  elements.subject.value = task.subject;
  elements.dueDate.value = task.due_date;
  elements.priority.value = task.priority;
  elements.status.value = task.status;
  elements.formTitle.textContent = "Editar tarea";
  elements.submitBtn.textContent = "Actualizar tarea";
  elements.cancelEditBtn.classList.remove("hidden");
  elements.title.focus();
}

async function deleteTask(id: number): Promise<void> {
  const confirmed = window.confirm("Deseas eliminar esta tarea?");
  if (!confirmed) return;

  try {
    await request<{ message: string }>(`/tasks/${id}`, { method: "DELETE" });
    showMessage("Tarea eliminada.");
    await loadTasks();
  } catch (error) {
    showMessage(error instanceof Error ? error.message : "No se pudo eliminar", true);
  }
}

function resetForm(): void {
  elements.taskForm.reset();
  elements.taskId.value = "";
  elements.formTitle.textContent = "Registrar tarea";
  elements.submitBtn.textContent = "Guardar tarea";
  elements.cancelEditBtn.classList.add("hidden");
}

function clearFilters(): void {
  elements.filterSubject.value = "";
  elements.filterStatus.value = "";
  elements.filterPriority.value = "";
  loadTasks();
}

function setApiStatus(ok: boolean): void {
  elements.apiStatus.textContent = ok ? "API: conectada" : "API: sin conexion";
  elements.apiStatus.className = ok
    ? "rounded border border-emerald-300 bg-emerald-50 px-3 py-2 text-sm text-emerald-800"
    : "rounded border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-800";
}

function showMessage(message: string, isError = false): void {
  elements.formMessage.textContent = message;
  elements.formMessage.className = `mt-3 text-sm ${isError ? "text-rose-700" : "text-teal-700"}`;
}

function priorityClass(priority: Priority): string {
  return {
    baja: "bg-slate-100 text-slate-700",
    media: "bg-amber-100 text-amber-800",
    alta: "bg-rose-100 text-rose-800",
  }[priority];
}

function statusClass(status: TaskStatus): string {
  return {
    pendiente: "bg-sky-100 text-sky-800",
    "en proceso": "bg-violet-100 text-violet-800",
    finalizada: "bg-emerald-100 text-emerald-800",
  }[status];
}

function label(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function escapeHtml(value: string): string {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

elements.taskForm.addEventListener("submit", saveTask);
elements.cancelEditBtn.addEventListener("click", resetForm);
elements.clearFiltersBtn.addEventListener("click", clearFilters);
elements.filterSubject.addEventListener("input", loadTasks);
elements.filterStatus.addEventListener("change", loadTasks);
elements.filterPriority.addEventListener("change", loadTasks);

loadTasks();
