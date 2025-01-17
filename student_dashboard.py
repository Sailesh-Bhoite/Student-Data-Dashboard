from data import display_records
from home1 import *  # This imports tkinter as tk and ttk.


window = tk.Tk()
window.title("Student Data Dashboard")
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.minsize(window.winfo_screenwidth(), window.winfo_screenheight())

style = ttk.Style()

canvas = tk.Canvas(window, bg="light blue")
canvas.pack(fill=tk.BOTH, expand=True)

# Other button styling
style.configure(
    "TButton",
    font=("Consolas", 13, "bold"),
    background="blue"
)

header_label = ttk.Label(window, text="Student Data Dashboard", font=("Algerian", 50, "bold"), background="light blue")
header_label.place(x=200, y=50)

# All the result will be displayed on the below canvas.
show_canvas = tk.Canvas(canvas)
canvas.create_window((100, 150), window=show_canvas, anchor="nw", height=500, width=1050)

# Creating a scrollbar.
frame_scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=show_canvas.yview)
frame_scrollbar.place(x=1150, y=150, height=500, anchor="nw")

# Configure show_canvas for 'yscrollcommand'
show_canvas.configure(yscrollcommand=frame_scrollbar.set)

# Making a frame
show_frame = ttk.Frame(show_canvas, style="show_frame.TFrame", height=200, width=1000)
show_canvas.create_window((0, 0), window=show_frame, anchor="nw")

# Adding the contents to show_frame
student_record = display_records()
for i, student_detail in enumerate(student_record):
    roll_label = ttk.Label(show_frame, text=f"{student_detail[0]}", style="detail_label.TLabel")
    name_label = ttk.Label(show_frame, text=f"{student_detail[1]} {student_detail[2]}", style="detail_label.TLabel")
    view_button = ttk.Button(show_frame, text="View", style="detail_view.TButton", command=lambda sd=student_detail: show_student_details(sd[0]))
    roll_label.grid(row=i, column=0)
    name_label.grid(row=i, column=1)
    view_button.grid(row=i, column=2, sticky="e")

# detail_label styling
style.configure(
    "detail_label.TLabel",
    font=("Consolas", 20, "bold"),
    padding=(130, 10)
)
# detail view button styling
style.configure(
    "detail_view.TButton",
    background="green",
    foreground="green",
    font=("Consolas", 20, "bold")
)
show_frame.bind("<Configure>", lambda e: show_canvas.configure(scrollregion=show_canvas.bbox("all")))

window.mainloop()
