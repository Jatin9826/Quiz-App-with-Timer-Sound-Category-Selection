import tkinter as tk
from tkinter import messagebox, ttk
import json, os, random, requests, base64, csv, winsound

# ——— Fetch trivia categories from API ———

def fetch_categories():
    res = requests.get("https://opentdb.com/api_category.php").json()
    return res.get("trivia_categories", [])

# ——— Fetch questions based on chosen category ———

def fetch_questions(amount=10, category_id=None):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple&encode=base64"
    if category_id:
        url += f"&category={category_id}"
    res = requests.get(url).json()
    questions = []
    if res["response_code"] == 0:
        for it in res["results"]:
            def dec(s): return base64.b64decode(s).decode('utf-8')
            q = dec(it["question"])
            corr = dec(it["correct_answer"])
            inc = [dec(x) for x in it["incorrect_answers"]]
            opts = inc + [corr]
            random.shuffle(opts)
            questions.append({"question": q, "options": opts, "answer": corr})
    return questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Quiz App – Timer, Sound, Categories")
        root.geometry("750x550")
        root.configure(bg="#8646E8")  # Dark theme

        self.categories = fetch_categories()
        self.setup_selection_screen()

    def setup_selection_screen(self):
        frm = tk.Frame(self.root, bg="#4479E1")
        frm.pack(pady=50)

        tk.Label(frm, text="Select Category:", font=("Arial", 14), bg="#2E3440", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.cat_var = tk.StringVar()
        cat_names = ["Any"] + [c["name"] for c in self.categories]
        ttk.Combobox(frm, values=cat_names, state="readonly", textvariable=self.cat_var).grid(row=0, column=1)

        tk.Label(frm, text="Number of Questions (5–20):", font=("Arial", 14), bg="#2E3440", fg="white").grid(row=1, column=0, pady=5)
        self.num_var = tk.IntVar(value=10)
        tk.Spinbox(frm, from_=5, to=20, textvariable=self.num_var, width=5).grid(row=1, column=1)

        tk.Button(frm, text="Start Quiz", font=("Arial", 14), bg="#F10C0C", fg="white", activebackground="#135F02", command=self.start_quiz).grid(row=2, columnspan=2, pady=20)

    def start_quiz(self):
        sel = self.cat_var.get()
        cat_id = next((c["id"] for c in self.categories if c["name"] == sel), None)
        count = self.num_var.get()
        self.questions = fetch_questions(count, cat_id)
        if not self.questions:
            messagebox.showerror("No Questions", "Not enough questions available. Try fewer or another category.")
            return

        self.time_per_q = 20
        self.qn_index = 0
        self.score = 0
        self.user_ans = [None] * len(self.questions)

        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_quiz_ui()
        self.show_question()

    def setup_quiz_ui(self):
        self.lbl_q = tk.Label(self.root, text="", wraplength=650, font=("Arial", 16), bg="#2E3440", fg="white")
        self.lbl_q.pack(pady=20)

        self.opt_var = tk.StringVar()
        self.rbs = [tk.Radiobutton(self.root, text="", variable=self.opt_var, value="", font=("Arial", 14), anchor="w", justify="left", bg="#2E3440", fg="white", selectcolor="#4C566A") for _ in range(4)]
        for rb in self.rbs:
            rb.pack(fill="x", padx=40, pady=5)

        self.lbl_timer = tk.Label(self.root, text="", font=("Arial", 14), fg="red", bg="#2E3440")
        self.lbl_timer.pack()

        frm = tk.Frame(self.root, bg="#2E3440")
        frm.pack(pady=10)
        tk.Button(frm, text="Previous", command=self.prev_q, width=12, bg="#5E81AC", fg="white", activebackground="#81A1C1").grid(row=0, column=0, padx=10)
        tk.Button(frm, text="Next", command=self.next_q, width=12, bg="#5E81AC", fg="white", activebackground="#81A1C1").grid(row=0, column=1, padx=10)
        tk.Button(frm, text="Submit", command=self.submit_quiz, bg="#A3BE8C", fg="white", font=("Arial", 12, "bold"), width=12).grid(row=0, column=2, padx=10)

    def show_question(self):
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        self.remaining = self.time_per_q
        self.update_timer()

        q = self.questions[self.qn_index]
        self.lbl_q.config(text=f"Q{self.qn_index+1}: {q['question']}")
        self.opt_var.set(self.user_ans[self.qn_index] or "")
        for i, txt in enumerate(q["options"]):
            self.rbs[i].config(text=txt, value=txt)

    def update_timer(self):
        self.lbl_timer.config(text=f"Time Left: {self.remaining}s")

        if self.remaining <= 0:
            winsound.Beep(600, 500)
            self.auto_next()
            return
        elif self.remaining <= 5:
            winsound.Beep(1000, 300)

        self.remaining -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def auto_next(self):
        self.save_ans()
        if self.qn_index < len(self.questions)-1:
            self.qn_index += 1
            self.show_question()
        else:
            self.submit_quiz()

    def next_q(self):
        self.save_ans()
        if self.qn_index < len(self.questions)-1:
            self.qn_index += 1
            self.show_question()

    def prev_q(self):
        self.save_ans()
        if self.qn_index > 0:
            self.qn_index -= 1
            self.show_question()

    def save_ans(self):
        self.user_ans[self.qn_index] = self.opt_var.get()

    def submit_quiz(self):
        self.save_ans()
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        self.score = sum(1 for i, q in enumerate(self.questions) if self.user_ans[i] == q["answer"])
        self.export_csv()

        messagebox.showinfo("Result", f"Score: {self.score}/{len(self.questions)}")
        self.root.quit()

    def export_csv(self):
        fname = "score.csv"
        header = ["Category", "Questions", "Correct", "Percent"]
        pct = round(self.score/len(self.questions)*100, 2)

        if not os.path.exists(fname):
            with open(fname, "w", newline="") as f:
                csv.writer(f).writerow(header)
        with open(fname, "a", newline="") as f:
            csv.writer(f).writerow([self.cat_var.get(), len(self.questions), self.score, f"{pct}%"])

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = QuizApp(tk_root)
    tk_root.mainloop()
