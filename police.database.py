import tkinter as tk
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bihar_police.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS police (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rank TEXT,
    station TEXT,
    phone TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------

def add_record():
    window = tk.Toplevel(root)
    window.title("Add Record")

    tk.Label(window, text="Name").pack()
    name = tk.Entry(window)
    name.pack()

    tk.Label(window, text="Rank").pack()
    rank = tk.Entry(window)
    rank.pack()

    tk.Label(window, text="Station").pack()
    station = tk.Entry(window)
    station.pack()

    tk.Label(window, text="Phone").pack()
    phone = tk.Entry(window)
    phone.pack()

    def save():
        cursor.execute("INSERT INTO police (name, rank, station, phone) VALUES (?, ?, ?, ?)",
                       (name.get(), rank.get(), station.get(), phone.get()))
        conn.commit()
        window.destroy()

    tk.Button(window, text="Save", command=save).pack()


def view_records():
    window = tk.Toplevel(root)
    window.title("Police Records")

    # Table headings
    headers = ["ID", "Name", "Rank", "Station", "Phone"]

    for col, header in enumerate(headers):
        tk.Label(window, text=header, borderwidth=1, relief="solid", width=15, bg="lightgrey").grid(row=0, column=col)

    cursor.execute("SELECT * FROM police")
    records = cursor.fetchall()

    # Fill table rows
    for row_num, row_data in enumerate(records, start=1):
        for col_num, value in enumerate(row_data):
            tk.Label(window, text=value, borderwidth=1, relief="solid", width=15).grid(row=row_num, column=col_num)

def delete_record():
    window = tk.Toplevel(root)
    window.title("Delete Record")

    tk.Label(window, text="Enter ID").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()

    def delete():
        cursor.execute("DELETE FROM police WHERE id=?", (id_entry.get(),))
        conn.commit()
        window.destroy()

    tk.Button(window, text="Delete", command=delete).pack()


def modify_record():
    window = tk.Toplevel(root)
    window.title("Modify Record")

    tk.Label(window, text="Enter ID").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()

    tk.Label(window, text="New Name").pack()
    name = tk.Entry(window)
    name.pack()

    def update():
        cursor.execute("UPDATE police SET name=? WHERE id=?",
                       (name.get(), id_entry.get()))
        conn.commit()
        window.destroy()

    tk.Button(window, text="Update", command=update).pack()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Bihar Police Database")
root.geometry("600x400")
root.configure(bg="#0b3d91")

frame = tk.Frame(root, bg="red")
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=320)

tk.Label(frame, text="BIHAR POLICE DATABASE", bg="red", fg="white",
         font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(frame, text="Add Record", width=20, command=add_record).pack(pady=5)
tk.Button(frame, text="View Records", width=20, command=view_records).pack(pady=5)
tk.Button(frame, text="Modify Record", width=20, command=modify_record).pack(pady=5)
tk.Button(frame, text="Delete Record", width=20, command=delete_record).pack(pady=5)
tk.Button(frame, text="Exit", width=20, command=root.quit).pack(pady=5)

root.mainloop()
