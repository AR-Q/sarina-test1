import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ChecklistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checklist App")
        self.geometry("600x600")

        self.tasks = {}

        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill="x")
        title_label = ttk.Label(header_frame, text="My Checklist")
        title_label.pack()

        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill="x", padx=10)
        self.entry_task = ttk.Entry(input_frame, width=40)
        self.entry_task.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_task.bind("<Return>", lambda e: self.add_task())

        self.category_var = tk.StringVar(value="Home")
        self.categories = ["Test", "Test2", "Test3", "Test4"]
        category_menu = ttk.OptionMenu(input_frame, self.category_var, self.categories[0], *self.categories)
        category_menu.config(width=10)
        category_menu.pack(side="left", padx=(0, 8))

        add_btn = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side="left")


        self.tasks_frame = ttk.Frame(self, padding=10)
        self.tasks_frame.pack(fill="both", expand=True, padx=10)


        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill="x", pady=5, padx=10)
        self.btn_done = ttk.Button(button_frame, text="Mark Done", command=self.mark_done)
        self.btn_done.pack(side="left", padx=4)
        self.btn_delete = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        self.btn_delete.pack(side="left", padx=4)
        self.btn_clear = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.pack(side="right", padx=4)

    def add_task(self):
        task_text = self.entry_task.get().strip()
        category = self.category_var.get()
        if not task_text:
            messagebox.showwarning("Input Required", "Please enter a task description!")
            return

        self.entry_task.delete(0, tk.END)

        task_frame = ttk.Frame(self.tasks_frame)
        task_frame.pack(fill="x", pady=2)

        var = tk.BooleanVar()
        check_btn = ttk.Checkbutton(task_frame, variable=var)
        check_btn.pack(side="left", padx=6)


        category_label = ttk.Label(task_frame, text=f"[{category}]")
        category_label.pack(side="left", padx=(0, 6))

        task_label = ttk.Label(task_frame, text=task_text, width=30, anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=4, pady=6)

        datetime_label = ttk.Label(task_frame, text="", foreground="gray")
        datetime_label.pack(side="right", padx=6)

        status_label = ttk.Label(task_frame, text="Pending")
        status_label.pack(side="right", padx=6)

        def toggle_task(event=None):
            if not self.tasks[task_frame]["done"]:
                var.set(not var.get())


        for w in (task_frame, task_label, status_label, datetime_label, category_label):
            w.bind("<Button-1>", toggle_task)

        self.tasks[task_frame] = {
            "text": task_text,
            "category": category,
            "done": False,
            "var": var,
            "label": task_label,
            "status": status_label,
            "datetime": datetime_label,
            "badge": category_label  
        }

    def mark_done(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        any_marked = False

        for task_frame, info in self.tasks.items():
            if info["var"].get() and not info["done"]:
                info["done"] = True
                info["label"].config(foreground="gray")
                info["status"].config(text="Done")
                info["datetime"].config(text=f"{now}")
                info["var"].set(False)
                any_marked = True

        if not any_marked:
            messagebox.showinfo("No Selection", "Please select tasks to mark as done!")

    def delete_selected(self):
        tasks_to_delete = []
        for task_frame, info in self.tasks.items():
            if info["var"].get():
                tasks_to_delete.append(task_frame)

        if not tasks_to_delete:
            messagebox.showinfo("No Selection", "Please select tasks to delete!")
            return

        for task_frame in tasks_to_delete:
            self._remove_task(task_frame)

    def _remove_task(self, task_frame):
        task_frame.destroy()
        del self.tasks[task_frame]

    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Empty List", "Your checklist is already empty!")
            return

        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all tasks?"):
            for task_frame in list(self.tasks.keys()):
                self._remove_task(task_frame)

if __name__ == "__main__":
    app = ChecklistApp()
    app.mainloop()
