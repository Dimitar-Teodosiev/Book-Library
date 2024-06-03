import tkinter
from tkinter import simpledialog, messagebox, PhotoImage
import sqlite3

book_index = 1
conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books
             (name TEXT, author TEXT, pages INTEGER)''')


def add_book():
    c.execute("SELECT name FROM books")
    temporary = c.fetchall()
    _list = [item for t in temporary for item in t]
    while True:
        try:
            book_name = simpledialog.askstring(" ", "Enter book name:")
            if (book_name not in _list) and (not book_name == "") and (book_name.lower() != "none"):
                break
            else:
                messagebox.showerror(title="Error", message="You can't enter 'None'\nor an already existing book")
        except AttributeError:
            messagebox.showerror(title="Error", message="You can't leave blank")
    book_author = simpledialog.askstring(" ", "Enter book author:")
    book_pages = int(simpledialog.askstring(" ", "Enter pages:"))
    c.execute("INSERT INTO books VALUES (?, ?, ?)", (book_name, book_author, book_pages))
    next_button.config(state="normal")
    previous_button.config(state="normal")
    search_button.config(state="normal")
    remove_button.config(state="normal")


def search_book():
    book_name = search_text.get()
    if (book_name.lower() != "none") and (book_name != ""):
        c.execute("SELECT * FROM books WHERE name = (:book_name)", {"book_name": book_name})
        temporary = c.fetchall()
        if len(temporary) == 0:
            messagebox.askokcancel(title="Not found", message=f"{book_name} was not found!")
        else:
            messagebox.askokcancel(title="Found",
                                   message=f"Book: {' '.join(str(temporary)).replace("(", "").replace(")", "")}")
    else:
        messagebox.showerror(title="Error", message="You can't search 'None'\nor leave blank")


def remove_book():
    book_name = simpledialog.askstring(" ", "Enter book name:")
    c.execute("DELETE FROM books WHERE name = (:book_name)", {"book_name": book_name})
    rows_deleted = c.rowcount
    if rows_deleted == 0:
        messagebox.askokcancel(title="Not found", message=f"{book_name} was not found!")
    else:
        messagebox.askokcancel(title="Found", message=f"{book_name} was deleted.")


def next_book():
    global book_index
    c.execute('SELECT COUNT(*) FROM books')
    result = c.fetchone()[0]
    if result != 0:
        if book_index == result:
            book_index = 1
        else:
            book_index += 1
        c.execute("SELECT * FROM books WHERE rowid = :book_index", {"book_index": book_index})
        temporary = c.fetchall()
        messagebox.askokcancel(title=f"Book#{book_index}",
                               message=f"Book: {' '.join(str(temporary)).replace("(", "").replace(")", "")}")
    else:
        next_button.config(state="disabled")


def previous_book():
    global book_index
    c.execute('SELECT COUNT(*) FROM books')
    result = c.fetchone()[-1]
    if result != 0:
        if book_index == 1:
            book_index = result
        else:
            book_index -= 1
        c.execute("SELECT * FROM books WHERE rowid = :book_index", {"book_index": book_index})
        temporary = c.fetchall()
        messagebox.askokcancel(title=f"Book#{book_index}",
                               message=f"Book: {' '.join(str(temporary)).replace("(", "").replace(")", "")}")
    else:
        previous_button.config(state="disabled")


conn.commit()

window = tkinter.Tk()
window.title("Library")
window.config(padx=20, pady=20, bg="saddle brown")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=620, height=620, bg="saddle brown", highlightbackground="saddle brown")
myimg = PhotoImage(file="Minecraft-Bookshelf.png")
canvas.create_image(310, 310, image=myimg)
canvas.grid(row=0, column=0, columnspan=3, pady=10)

search_text = tkinter.Entry(window, width=55, highlightthickness=1, highlightbackground="black")
search_text.grid(row=1, column=0, columnspan=3, pady=10)

button_style = {
    "bg": "white",
    "padx": 10,
    "pady": 5
}

search_button = tkinter.Button(window, text="Search", command=search_book, state="disabled", **button_style)
search_button.grid(row=1, column=2, pady=5)

remove_button = tkinter.Button(window, text="Remove", command=remove_book, state="disabled", **button_style)
remove_button.grid(row=2, column=1, pady=5)

add_button = tkinter.Button(window, text="Add", command=add_book, state="normal", **button_style)
add_button.grid(row=3, column=1, pady=5)

next_button = tkinter.Button(window, text="Next", command=next_book, state="disabled", **button_style)
next_button.grid(row=3, column=2, padx=10, pady=5)

previous_button = tkinter.Button(window, text="Previous", command=previous_book, state="disabled", **button_style)
previous_button.grid(row=3, column=0, padx=10, pady=5)

window.mainloop()
