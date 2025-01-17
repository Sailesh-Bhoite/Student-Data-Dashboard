import tkinter as tk
from tkinter import ttk
import sqlite3

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def show_student_details(roll_no):
    # Setting up the database connection.
    conn = sqlite3.connect('students.db')

    # Creating a cursor to execute queries.
    c = conn.cursor()

    window1 = tk.Toplevel(relief=tk.SUNKEN)
    window1.configure(height=500, width=500)
    window1.title(f"Roll number {roll_no}")
    window1.geometry(f"{window1.winfo_screenwidth()}x{window1.winfo_screenheight()}")
    window1.minsize(window1.winfo_screenwidth(), window1.winfo_screenheight())
    tk.Label(window1, text="Details of Roll Number "+str(roll_no)).pack()
    note1 = ttk.Notebook(window1)
    note1.pack(expand=1, fill='both')
    tab1 = tk.Frame(note1, bg="red")
    tab1.pack(expand=1, fill='both')
    tab2 = tk.Frame(note1, bg="blue")
    tab2.pack(expand=1, fill='both')
    tab3 = tk.Frame(note1, bg="green")
    tab3.pack(expand=1, fill='both')

    # Giving title to the tabs
    # Personal Details Tab
    note1.add(tab1, text='          Personal Details          ')

    # Academic Details Tab
    note1.add(tab2, text='          Academics Details          ')

    # Payment Details Tab
    note1.add(tab3, text='          Payment Details          ')

    """Academics Section"""
    c.execute(f"SELECT * FROM Academics WHERE RollNo={roll_no}")
    academics_data = c.fetchall()
    # Identifying Year
    if academics_data[0][1] == 'first':
        year = 'First Year'
    elif academics_data[0][1] == 'second':
        year = 'Second Year'
    elif academics_data[0][1] == 'third':
        year = 'Third Year'
    elif academics_data[0][1] == 'fourth':
        year = 'Fourth Year'
    else:
        year = 'Invalid Year'
    # Identifying Semester and Subject List
    subjects = []
    teachers = []
    if academics_data[0][2] == 'one':
        semester = '1'
        subjects = ['DBMS', 'SPOS', 'CNS', 'SPM', 'TOC']
        teachers = ['Teacher 1', 'T2', 'T3', 'T4', 'T5']
    elif academics_data[0][2] == 'two':
        semester = '2'
        subjects = ['V', 'W', 'X', 'Y', 'Z']
        teachers = ['Teacher 11', 'T22', 'T33', 'T44', 'T55']
    else:
        semester = 'Invalid Semester'
    # cgpa marks
    marks = [x for x in academics_data[0][4:7]]

    year_frame = tk.Frame(tab2, bg="yellow")
    year_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    year_label = tk.Label(year_frame, text=year, bg="yellow", font=("Algerian", 40), padx=210)
    year_label.pack(side=tk.LEFT)

    sem_label = tk.Label(year_frame, text=semester, bg="orange", font=("Consolas", 30), padx=30)
    sem_label.pack(side=tk.LEFT, padx=10)

    present_fig, present_ax = plt.subplots(facecolor="lightgreen")
    present_ax.pie([academics_data[0][3], 100 - academics_data[0][3]],
                   labels=[f"{academics_data[0][3]:.2f}%", f"{100 - academics_data[0][3]:.2f}%"],
                   wedgeprops={'edgecolor': 'black'},
                   colors=('green', 'red'), )
    present_ax.set_title('Attendance', fontsize=20)
    presenty_canvas = FigureCanvasTkAgg(present_fig, master=tab2)
    presenty_canvas.get_tk_widget().config(width=350, height=310)
    presenty_canvas.draw()
    presenty_canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)
    # Identifying Submissions
    submit_colors = ["red" if x == 0 else "green" for x in academics_data[0][7:]]
    submission_frame = tk.Frame(tab2, bg="black")
    submission_frame.grid(row=1, column=1, padx=5, pady=5)
    submit_title_label = tk.Label(submission_frame, text="Submissions", font=("Consolas", 45), fg="white", bg="black")
    submit_title_label.pack()
    for i in range(0, len(subjects)):
        subject_label = tk.Label(submission_frame, text=subjects[i], bg=submit_colors[i], width=25, font=("Arial", 20))
        subject_label.pack(pady=5, padx=10)
    # Subject and Teacher Section
    teachers_frame = tk.Frame(tab2, bg="#C576F6")
    teachers_frame.grid(row=0, column=2, padx=5, rowspan=3)
    teachers_title_label = tk.Label(teachers_frame, text="Subjects & Teachers", font=("Bahnschrift SemiBold", 30),
                                    bg='#9417E2', fg='yellow', pady=18)
    teachers_title_label.grid(row=0, column=0, columnspan=2, padx=15, pady=15)
    for i in range(0, len(teachers)):
        tk.Label(teachers_frame, text=subjects[i], font=("Consolas", 30), pady=10, bg="#C576F6", fg="#51087E").grid(
            row=i + 1, column=0, pady=15)
        tk.Label(teachers_frame, text=teachers[i], font=("Consolas", 30), pady=10, bg="#C576F6", fg="#51087E").grid(
            row=i + 1, column=1, pady=15)
    # CGPA Section
    marks_frame = tk.Frame(tab2, bg="yellow")
    marks_frame.grid(row=2, column=0, padx=5, pady=10, columnspan=2)
    fig2, ax2 = plt.subplots(facecolor="lightblue")
    bar = ax2.barh(['FE', 'SE', 'TE'], marks, color=['#0077B6', '#00B4D8', '#00FFFF'])
    ax2.set_title('Pointers')
    ax2.set_xticks(np.arange(0, 10.5, 0.5))
    for bar, value in zip(bar, marks):
        ax2.text(value, bar.get_y() + bar.get_height() / 2, f'{value:.2f}', ha='left', va='center', color='black')
    marks_canvas = FigureCanvasTkAgg(fig2, master=marks_frame)
    marks_canvas.get_tk_widget().config(width=795, height=210)
    marks_canvas.draw()
    marks_canvas.get_tk_widget().pack()

    """Payment Section"""
    c.execute(f"select * from Payment where RollNo={roll_no}")
    payment_record = c.fetchall()
    """[(3, 'third', 90000, 46000, 0, 0)]"""

    if payment_record[0][4] != 0 and payment_record[0][5] != 0:  # If hostel fees are available.
        col_fees_frame = tk.Frame(tab3, bg="lightyellow")
        col_fees_frame.grid(row=0, column=0, padx=30, pady=20)
        col_fees_data = [payment_record[0][2] - payment_record[0][3], payment_record[0][3]]
        fig1, ax1 = plt.subplots(facecolor='lightyellow')
        if payment_record[0][3] != 90_000:  # If College Fees are NOT PAID.
            ax1.pie(col_fees_data,
                    labels=[f"{round(col_fees_data[0] / (col_fees_data[0] + col_fees_data[1]) * 100)}%",
                            f"{round(col_fees_data[1] / (col_fees_data[0] + col_fees_data[1]) * 100)}%"],
                    colors=["red", "green"],
                    wedgeprops=dict(width=0.3, edgecolor='black'),
                    textprops={'fontsize': 15}
                    )
        else:  # If College fees are PAID.
            ax1.pie(col_fees_data,
                    labels=["", "Paid"],
                    colors=["red", "green"],
                    wedgeprops=dict(width=0.3, edgecolor='black'),
                    textprops={'fontsize': 15}
                    )

        ax1.set_title("College Fees", fontsize=25)
        col_fees_canvas = FigureCanvasTkAgg(fig1, master=col_fees_frame)
        col_fees_canvas.get_tk_widget().config(width=580, height=430)
        col_fees_canvas.draw()
        col_fees_canvas.get_tk_widget().pack()

        col_fees_balance_label = tk.Label(col_fees_frame, text=f"Balance: {col_fees_data[0]}", font=("Arial", 20),
                                          bg="lightyellow", fg="red")
        col_fees_paid_label = tk.Label(col_fees_frame, text=f"Paid: {col_fees_data[1]}", font=("Arial", 20),
                                       bg="lightyellow",
                                       fg="green")
        col_fees_total_label = tk.Label(col_fees_frame, text=f"Total: {col_fees_data[0] + col_fees_data[1]}",
                                        font=("Arial", 20), bg="lightyellow")

        col_fees_balance_label.pack(fill=tk.BOTH, expand=1, pady=10)
        col_fees_paid_label.pack(fill=tk.BOTH, expand=1, pady=10)
        col_fees_total_label.pack(fill=tk.BOTH, expand=1, pady=10)

        hos_fees_frame = tk.Frame(tab3, bg="lightblue")
        hos_fees_frame.grid(row=0, column=1, padx=30, pady=20)
        hos_fees_data = [payment_record[0][4] - payment_record[0][5], payment_record[0][5]]
        fig2, ax2 = plt.subplots(facecolor="lightblue")
        if payment_record[0][5] != 35_000:  # If Hostel fees are NOT PAID.
            ax2.pie(hos_fees_data,
                    labels=[f"{round(hos_fees_data[0] / (hos_fees_data[0] + hos_fees_data[1]) * 100)}%",
                            f"{round(hos_fees_data[1] / (hos_fees_data[0] + hos_fees_data[1]) * 100)}%"],
                    colors=["red", "green"],
                    wedgeprops=dict(width=0.3, edgecolor='black'),
                    textprops={'fontsize': 15}
                    )
        else:  # If Hostel fees are PAID.
            ax2.pie(hos_fees_data,
                    labels=["", "Paid"],
                    colors=["red", "green"],
                    wedgeprops=dict(width=0.3, edgecolor='black'),
                    textprops={'fontsize': 15}
                    )
        ax2.set_title("Hostel Fees", fontsize=25)
        hos_fees_canvas = FigureCanvasTkAgg(fig2, master=hos_fees_frame)
        hos_fees_canvas.get_tk_widget().config(width=580, height=430)
        hos_fees_canvas.draw()
        hos_fees_canvas.get_tk_widget().pack()

        hos_fees_balance_label = tk.Label(hos_fees_frame, text=f"Balance: {hos_fees_data[0]}", font=("Arial", 20),
                                          bg="lightblue", fg="red")
        hos_fees_paid_label = tk.Label(hos_fees_frame, text=f"Paid: {hos_fees_data[1]}", font=("Arial", 20),
                                       bg="lightblue",
                                       fg="green")
        hos_fees_total_label = tk.Label(hos_fees_frame, text=f"Total: {hos_fees_data[0] + hos_fees_data[1]}",
                                        font=("Arial", 20), bg="lightblue")

        hos_fees_balance_label.pack(fill=tk.BOTH, expand=1, pady=10)
        hos_fees_paid_label.pack(fill=tk.BOTH, expand=1, pady=10)
        hos_fees_total_label.pack(fill=tk.BOTH, expand=1, pady=10)

    else:  # If there are no hostel fees.
        col_fees_frame = tk.Frame(tab3, bg="lightyellow")
        col_fees_frame.pack(fill=tk.BOTH, expand=1, padx=70, pady=20)
        col_fees_data = [payment_record[0][2] - payment_record[0][3], payment_record[0][3]]
        fig1, ax1 = plt.subplots(facecolor='lightyellow')
        ax1.pie(col_fees_data,
                labels=[f"{round(col_fees_data[0] / (col_fees_data[0] + col_fees_data[1]) * 100)}%",
                        f"{round(col_fees_data[1] / (col_fees_data[0] + col_fees_data[1]) * 100)}%"],
                colors=["red", "green"],
                wedgeprops=dict(width=0.3, edgecolor='black'),
                textprops={'fontsize': 15}
                )
        ax1.set_title("College Fees", fontsize=25)
        col_fees_canvas = FigureCanvasTkAgg(fig1, master=col_fees_frame)
        col_fees_canvas.get_tk_widget().config(width=580, height=430)
        col_fees_canvas.draw()
        col_fees_canvas.get_tk_widget().pack()

        col_fees_balance_label = tk.Label(col_fees_frame, text=f"Balance: {col_fees_data[0]}", font=("Arial", 20),
                                          bg="lightyellow", fg="red")
        col_fees_paid_label = tk.Label(col_fees_frame, text=f"Paid: {col_fees_data[1]}", font=("Arial", 20),
                                       bg="lightyellow",
                                       fg="green")
        col_fees_total_label = tk.Label(col_fees_frame, text=f"Total: {col_fees_data[0] + col_fees_data[1]}",
                                        font=("Arial", 20), bg="lightyellow")

        col_fees_balance_label.pack(fill=tk.BOTH, expand=1, pady=10)
        col_fees_paid_label.pack(fill=tk.BOTH, expand=1, pady=10)
        col_fees_total_label.pack(fill=tk.BOTH, expand=1, pady=10)

    """Personal Section"""
    c.execute(f"select * from Personal where RollNo={roll_no}")
    pr = c.fetchall()
    personal_record = pr[0]
    """[(1, 'Aarav', 'Sharma', 'Male', '15/02/2005', '9876543210', 'aarav.sharma@example.com', 'Cricket,Reading', 'Science Olympiad Winner', 'Rajesh Sharma', '9876543211', 'rajesh.sharma@example.com', 'Engineer', 'Priya Sharma', '9876543212', 'priya.sharma@example.com', 'Teacher', '', '', '', '', '123, MG Road, Mumbai, Maharashtra', 'third')]"""

    # Sector 1: Hobby/Interest
    hobby_list = personal_record[7].split(",")
    hobby_frame = ttk.Frame(tab1, padding=(55, 40))
    hobby_frame.grid(row=0, column=0, padx=50, pady=10)
    ttk.Label(hobby_frame, text="Hobby/Interest", width=15, font=("MS Sans Serif", 30, "bold"), padding=10, background="blue", foreground="light blue", anchor="c").pack(pady=10)
    for hobby in hobby_list:
        ttk.Label(hobby_frame, text=hobby, width=25, font=("Arial", 20), padding=10, background="light blue", anchor="c").pack(pady=10)

    # Sector 2: Profile Information
    profile_frame = ttk.Frame(tab1, padding="10 10 10 10")
    profile_frame.grid(row=0, column=1, padx=5, pady=25)
    ttk.Label(profile_frame, text="General Information", font=("MS Sans Serif", 30, "bold"), foreground="orange").pack(pady=5)
    ttk.Label(profile_frame, text=f"Name: {personal_record[1]} {personal_record[2]}", width=55, font=("Arial", 15), padding=5).pack(pady=5)
    ttk.Label(profile_frame, text=f"Gender: {personal_record[3]}", width=55, font=("Arial", 15), padding=5).pack(pady=5)
    ttk.Label(profile_frame, text=f"DOB: {personal_record[4]}", width=55, font=("Arial", 15), padding=5).pack(pady=5)
    ttk.Label(profile_frame, text=f"Email: {personal_record[6]}", width=55, font=("Arial", 15), padding=5).pack(pady=5)
    ttk.Label(profile_frame, text=f"Phone Number: {personal_record[5]}", width=55, font=("Arial", 15), padding=5).pack(pady=5)

    # Sector 3: Address
    address_frame = ttk.Frame(tab1, padding=(55, 20))
    address_frame.grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(address_frame, text="Address", font=("MS Sans Serif", 30, "bold")).pack()
    ttk.Label(address_frame, text=personal_record[-2], font=("Arial", 15)).pack()

    # Sector 4: Achievements
    achievements_frame = ttk.Frame(tab1, padding=(85, 20))
    achievements_frame.grid(row=2, column=0, padx=5, pady=5)
    ttk.Label(achievements_frame, text="Achievements", font=("algerian", 30, "bold"), foreground="#66ff00", background="#00a35b").pack()
    ttk.Label(achievements_frame, text=personal_record[8], font=("Arial", 15)).pack()

    # Sector 5: Family Information
    family_frame = ttk.Frame(tab1, padding=(5, 20))
    family_frame.grid(row=1, column=1, pady=5, rowspan=2)
    ttk.Label(family_frame, text="Family/Guardian Information", font=("MS Sans Serif", 30, "bold")).grid(row=0, column=0, columnspan=3)

    # Family columns
    if personal_record[15] != '':
        father_frame = ttk.Frame(family_frame, padding=(5, 20))
        father_frame.grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(father_frame, text="Father", font=("Arial", 20, "bold"), background="olive", padding=(100, 15), foreground="yellow").grid(row=0, column=0)
        ttk.Label(father_frame, text=f"Name: {personal_record[9]}\nMobile No: {personal_record[10]}\nEmail: {personal_record[11]}\nOccupation: {personal_record[12]}", font=("Arial", 14), background="yellow").grid(row=1, column=0)

        mother_frame = ttk.Frame(family_frame, padding=(5, 20))
        mother_frame.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(mother_frame, text="Mother", font=("Arial", 20, "bold"), background="olive", padding=(100, 15), foreground="yellow").grid(row=0, column=1)
        ttk.Label(mother_frame, text=f"Name: {personal_record[13]}\nMobile No: {personal_record[14]}\nEmail: {personal_record[15]}\nOccupation: {personal_record[16]}", font=("Arial", 14), background="yellow").grid(row=1, column=1)

    else:
        guardian_frame = ttk.Frame(family_frame, padding=(5, 20))
        guardian_frame.grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(guardian_frame, text="Guardian", font=("Arial", 20, "bold"), background="olive", padding=(100, 15), foreground="yellow").grid(row=0, column=2)
        ttk.Label(guardian_frame, text=f"Name: {personal_record[17]}\nMobile No: {personal_record[18]}\nEmail: {personal_record[19]}\nOccupation: {personal_record[20]}", font=("Arial", 14), background="yellow").grid(row=1, column=2)

    # Confirming all changes
    conn.commit()

    # Closing the sqlite3 connections
    conn.close()
