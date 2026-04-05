import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import date

# ==================== OOP CLASSES ====================
class Student:
    def __init__(self, name, student_id, physics, chemistry, biology, monthly_fee):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.marks = {
            "Physics": float(physics),
            "Chemistry": float(chemistry),
            "Biology": float(biology)
        }
        self.monthly_fee = float(monthly_fee)

    def total_marks(self):
        return sum(self.marks.values())

    def average(self):
        return round(self.total_marks() / 3, 2)

    def get_grade(self):
        avg = self.average()
        if 75 <= avg <= 100:
            return "A"
        elif 60 <= avg < 75:
            return "B"
        elif 45 <= avg < 60:
            return "C"
        elif 35 <= avg < 45:
            return "S"
        else:
            return "F"

    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "marks": self.marks,
            "monthly_fee": self.monthly_fee
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["student_id"],
                   data["marks"]["Physics"], data["marks"]["Chemistry"], data["marks"]["Biology"],
                   data["monthly_fee"])


class StudentManager:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists("students.json"):
            with open("students.json", "r") as f:
                self.students = [Student.from_dict(s) for s in json.load(f)]

    def save_data(self):
        with open("students.json", "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    # === ADD STUDENT ===
    def add_student(self, name, student_id, physics, chemistry, biology, monthly_fee):
        if not name or not student_id:
            raise ValueError("Name and Student ID are required!")
        if any(s.student_id == student_id for s in self.students):
            raise ValueError("Student ID already exists!")
        # Validate marks
        for m in [physics, chemistry, biology]:
            if not (0 <= float(m) <= 100):
                raise ValueError("Marks must be between 0 and 100!")
        if float(monthly_fee) < 0:
            raise ValueError("Monthly fee cannot be negative!")
        self.students.append(Student(name, student_id, physics, chemistry, biology, monthly_fee))
        self.save_data()

    # === SEARCH ===
    def search_by_id(self, student_id):
        return next((s for s in self.students if s.student_id == student_id), None)

    # === ALL STUDENTS ===
    def get_all_students(self):
        return self.students

    # === TOTAL FEE INVENTORY ===
    def get_total_fees(self):
        return sum(s.monthly_fee for s in self.students)

    # === GENERATE REPORT CARD (CSV) ===
    def generate_report_card(self, student):
        filename = f"report_card_{student.student_id}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Kothalawala Academy - Student Report Card"])
            writer.writerow(["Date:", date.today().strftime("%Y-%m-%d")])
            writer.writerow([""])
            writer.writerow(["Student Name:", student.name])
            writer.writerow(["Student ID:", student.student_id])
            writer.writerow([""])
            writer.writerow(["Subject", "Marks", "Grade"])
            for sub, mark in student.marks.items():
                writer.writerow([sub, mark, ""])
            writer.writerow(["Total Marks", student.total_marks(), ""])
            writer.writerow(["Average", student.average(), student.get_grade()])
            writer.writerow([""])
            writer.writerow(["Monthly Enrollment Fee", f"Rs {student.monthly_fee:.2f}"])
            writer.writerow([""])
            writer.writerow(["Note: Grade Scale -> A:[75-100], B:[60-75), C:[45-60), S:[35-45), F:[0-35)"])
        return filename


# ==================== GUI ====================
class StudentGUI:
    def __init__(self):
        self.manager = StudentManager()
        self.root = tk.Tk()
        self.root.title("Kothalawala Academy - Student Management System")
        self.root.geometry("1000x720")

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_add_tab(notebook)
        self.create_search_tab(notebook)
        self.create_all_students_tab(notebook)
        self.create_fee_inventory_tab(notebook)
        self.create_report_tab(notebook)

        self.root.mainloop()

    def create_add_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Add Student")

        ttk.Label(frame, text="Student Name:").grid(row=0, column=0, pady=8, padx=15, sticky="w")
        name_entry = ttk.Entry(frame, width=50)
        name_entry.grid(row=0, column=1, pady=8)

        ttk.Label(frame, text="Student ID:").grid(row=1, column=0, pady=8, padx=15, sticky="w")
        id_entry = ttk.Entry(frame, width=50)
        id_entry.grid(row=1, column=1, pady=8)

        ttk.Label(frame, text="Physics:").grid(row=2, column=0, pady=8, padx=15, sticky="w")
        phy_entry = ttk.Entry(frame, width=50)
        phy_entry.grid(row=2, column=1, pady=8)

        ttk.Label(frame, text="Chemistry:").grid(row=3, column=0, pady=8, padx=15, sticky="w")
        chem_entry = ttk.Entry(frame, width=50)
        chem_entry.grid(row=3, column=1, pady=8)

        ttk.Label(frame, text="Biology:").grid(row=4, column=0, pady=8, padx=15, sticky="w")
        bio_entry = ttk.Entry(frame, width=50)
        bio_entry.grid(row=4, column=1, pady=8)

        ttk.Label(frame, text="Monthly Enrollment Fee (Rs):").grid(row=5, column=0, pady=8, padx=15, sticky="w")
        fee_entry = ttk.Entry(frame, width=50)
        fee_entry.grid(row=5, column=1, pady=8)

        def add():
            try:
                self.manager.add_student(name_entry.get(), id_entry.get(),
                                         phy_entry.get(), chem_entry.get(), bio_entry.get(),
                                         fee_entry.get())
                messagebox.showinfo("Success", "Student added successfully!")
                for e in [name_entry, id_entry, phy_entry, chem_entry, bio_entry, fee_entry]:
                    e.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(frame, text="Add Student", command=add).grid(row=6, column=1, pady=20)

    def create_search_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Search by ID")

        ttk.Label(frame, text="Enter Student ID:").pack(pady=10)
        search_entry = ttk.Entry(frame, width=40)
        search_entry.pack(pady=5)

        result_text = tk.Text(frame, height=18, width=90)
        result_text.pack(pady=10)

        def search():
            result_text.delete(1.0, tk.END)
            student = self.manager.search_by_id(search_entry.get())
            if not student:
                result_text.insert(tk.END, "Student not found.")
                return
            avg = student.average()
            grade = student.get_grade()
            result_text.insert(tk.END,
                f"Name: {student.name}\n"
                f"ID: {student.student_id}\n\n"
                f"Physics: {student.marks['Physics']}\n"
                f"Chemistry: {student.marks['Chemistry']}\n"
                f"Biology: {student.marks['Biology']}\n\n"
                f"Total Marks: {student.total_marks()}\n"
                f"Average: {avg} → Grade: {grade}\n"
                f"Monthly Fee: Rs {student.monthly_fee:.2f}"
            )

        ttk.Button(frame, text="Search", command=search).pack()

    def create_all_students_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="All Students")

        result_text = tk.Text(frame, height=25, width=100)
        result_text.pack(pady=10)

        def show_all():
            result_text.delete(1.0, tk.END)
            students = self.manager.get_all_students()
            if not students:
                result_text.insert(tk.END, "No students yet.")
                return
            for s in students:
                result_text.insert(tk.END,
                    f"Name: {s.name} | ID: {s.student_id} | Avg: {s.average()} | Grade: {s.get_grade()}\n"
                )

        ttk.Button(frame, text="Refresh List", command=show_all).pack(pady=5)
        show_all()

    def create_fee_inventory_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Fee Inventory")

        result_text = tk.Text(frame, height=20, width=90)
        result_text.pack(pady=10)

        def show_fees():
            result_text.delete(1.0, tk.END)
            total = self.manager.get_total_fees()
            result_text.insert(tk.END, f"Total Monthly Enrollment Fees Collected: Rs {total:.2f}\n\n")
            result_text.insert(tk.END, "Student-wise Fees:\n")
            for s in self.manager.get_all_students():
                result_text.insert(tk.END, f"{s.name} ({s.student_id}) → Rs {s.monthly_fee:.2f}\n")

        ttk.Button(frame, text="Refresh Fee Summary", command=show_fees).pack(pady=10)
        show_fees()

    def create_report_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Generate Report Card")

        ttk.Label(frame, text="Enter Student ID to generate CSV report card:").pack(pady=15)
        id_entry = ttk.Entry(frame, width=40)
        id_entry.pack(pady=5)

        def generate():
            student = self.manager.search_by_id(id_entry.get())
            if not student:
                messagebox.showerror("Error", "Student not found!")
                return
            filename = self.manager.generate_report_card(student)
            messagebox.showinfo("Success", f"Report card saved as:\n{filename}\n\nYou can open it with Excel!")
            id_entry.delete(0, tk.END)

        ttk.Button(frame, text="Generate CSV Report Card", command=generate).pack(pady=20)

if __name__ == "__main__":
    StudentGUI()