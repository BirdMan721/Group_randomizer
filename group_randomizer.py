import random
import tkinter as tk
from tkinter import messagebox
import os

class NameGroupRandomizer:
    def __init__(self, students, teachers):
        self.students = students
        self.teachers = teachers

    def create_groups(self):
        random.shuffle(self.students)
        teachers_copy = self.teachers[:]
        random.shuffle(teachers_copy)

        groups = []
        num_students = len(self.students)
        num_teachers = len(teachers_copy)

        for i in range(num_students):
            student = self.students[i]
            num_assigned_teachers = 2 if i < num_teachers - num_students else 1
            assigned_teachers = random.sample(teachers_copy, num_assigned_teachers)
            groups.append((student, assigned_teachers))
            for teacher in assigned_teachers:
                teachers_copy.remove(teacher)

        return groups

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Name Group Randomizer")
        self.geometry("450x500")

        self.students = self.load_names_from_file("students.txt")
        self.teachers = self.load_names_from_file("teachers.txt")
        self.groups = self.load_groups_from_file()

        # Create a main frame for organizing the layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame for Students
        self.students_frame = tk.Frame(self.main_frame)
        self.students_frame.grid(row=0, column=0, padx=10)

        self.label1 = tk.Label(self.students_frame, text="Students:")
        self.label1.pack(pady=5)

        self.entry_name1 = tk.Entry(self.students_frame, width=30)
        self.entry_name1.pack(pady=5)

        self.add_button1 = tk.Button(self.students_frame, text="Add Name", command=self.add_student)
        self.add_button1.pack(pady=5)

        self.names_listbox1 = tk.Listbox(self.students_frame)
        self.names_listbox1.pack(pady=5)
        self.update_listbox1()

        self.delete_button1 = tk.Button(self.students_frame, text="Delete Selected Name", command=self.delete_student)
        self.delete_button1.pack(pady=5)

        # Frame for Teachers
        self.teachers_frame = tk.Frame(self.main_frame)
        self.teachers_frame.grid(row=0, column=1, padx=10)

        self.label2 = tk.Label(self.teachers_frame, text="Teachers:")
        self.label2.pack(pady=5)

        self.entry_name2 = tk.Entry(self.teachers_frame, width=30)
        self.entry_name2.pack(pady=5)

        self.add_button2 = tk.Button(self.teachers_frame, text="Add Name", command=self.add_teacher)
        self.add_button2.pack(pady=5)

        self.names_listbox2 = tk.Listbox(self.teachers_frame)
        self.names_listbox2.pack(pady=5)
        self.update_listbox2()

        self.delete_button2 = tk.Button(self.teachers_frame, text="Delete Selected Name", command=self.delete_teacher)
        self.delete_button2.pack(pady=5)

        # Group Management
        self.create_groups_button = tk.Button(self.main_frame, text="Create Groups", command=self.create_groups)
        self.create_groups_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.show_groups_button = tk.Button(self.main_frame, text="Show Last Groups", command=self.show_groups)
        self.show_groups_button.grid(row=2, column=0, columnspan=2, pady=10)


    def add_student(self):
        name = self.entry_name1.get()
        if name:
            self.students.append(name)
            self.update_listbox1()
            self.entry_name1.delete(0, tk.END)
            self.save_names_to_file(self.students, "students.txt")

    def delete_student(self):
        selected_index = self.names_listbox1.curselection()
        if selected_index:
            self.students.pop(selected_index[0])
            self.update_listbox1()
            self.save_names_to_file(self.students, "students.txt")

    def update_listbox1(self):
        self.names_listbox1.delete(0, tk.END)
        for name in self.students:
            self.names_listbox1.insert(tk.END, name)

    def add_teacher(self):
        name = self.entry_name2.get()
        if name:
            self.teachers.append(name)
            self.update_listbox2()
            self.entry_name2.delete(0, tk.END)
            self.save_names_to_file(self.teachers, "teachers.txt")

    def delete_teacher(self):
        selected_index = self.names_listbox2.curselection()
        if selected_index:
            self.teachers.pop(selected_index[0])
            self.update_listbox2()
            self.save_names_to_file(self.teachers, "teachers.txt")

    def update_listbox2(self):
        self.names_listbox2.delete(0, tk.END)
        for name in self.teachers:
            self.names_listbox2.insert(tk.END, name)

    def save_names_to_file(self, names, filename):
        folder_path = "name_group_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w") as file:
            for name in names:
                file.write(f"{name}\n")

    def load_names_from_file(self, filename):
        folder_path = "name_group_data"
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                names = file.read().splitlines()
            return names
        return []

    def save_groups_to_file(self, groups):
        folder_path = "name_group_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, "groups.txt")
        with open(file_path, "w") as file:
            for group in groups:
                group_str = f"Student: {group[0]}, Teachers: {', '.join(group[1])}\n"
                file.write(group_str)

    def load_groups_from_file(self):
        folder_path = "name_group_data"
        file_path = os.path.join(folder_path, "groups.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                groups = file.read().splitlines()
            return groups
        return []

    def create_groups(self):
        if not self.students or not self.teachers:
            messagebox.showerror("No names", "Please add some names to both lists first.")
            return

        randomizer = NameGroupRandomizer(self.students, self.teachers)
        self.groups = randomizer.create_groups()
        self.save_groups_to_file(self.groups)

        group_text = ""
        for group in self.groups:
            group_text += f"Student: {group[0]}, Teachers: {', '.join(group[1])}\n"

        messagebox.showinfo("Groups", group_text)

    def show_groups(self):
        groups = self.load_groups_from_file()
        if not groups:
            messagebox.showinfo("No groups", "No groups to display.")
            return

        group_text = "\n".join(groups)
        messagebox.showinfo("Last Groups", group_text)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
