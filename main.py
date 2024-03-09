import pymysql as pm
from tkinter import *
from bookdetails import *
from secrets import *

username = ""
password = ""

mycon = pm.connect(host='localhost', user=USERNAME, password=PASSWORD)
cur = mycon.cursor()
cur.execute("show databases LIKE 'library'")
data = cur.fetchone()
if not data:
    cur.execute("create database library")
    mycon.commit()
cur.execute("use library")
cur.execute("show tables LIKE 'users'")
data = cur.fetchone()
if not data:
    cur.execute("create table users (username VARCHAR(30), password VARCHAR(100), history VARCHAR(500) default '[]', current VARCHAR(100) default '[]')")
cur.execute("show tables LIKE 'books'")
data = cur.fetchone()
if not data:
    cur.execute("create table books (name VARCHAR(30), author VARCHAR(30))")
books = cur.execute("select * from books")
data = cur.fetchall()
with open("booknames.txt") as names:
    text = names.read()
    text = text.split("\n")
    for rec in text:
        rec = eval(rec)
        if rec not in data:
            cur.execute(f"insert into books (name, author) values {rec}")
            mycon.commit()
mycon.close()


def signup(root1=None):
    if root1:
        root1.destroy()
    root2 = Tk()
    root2.config(padx=20, pady=20, bg='white')
    root2.title("Sign Up")
    root2.geometry("500x500")
    root2.after(1, lambda: root2.focus_force())

    def my_show():
        if show_pw.get() == 1:
            pw.config(show='')
        else:
            pw.config(show='*')

    def add(event="<Return>"):
        error = False
        user_error['text'] = ""
        pw_error['text'] = ""
        if len(user.get()) < 6:
            user_error['text'] = "Username should be 6-30 characters long"
            error = True
        if len(pw.get()) < 8:
            pw_error['text'] = "Password should be at least 8 characters long"
            error = True
        if error:
            return
        mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
        cur = mycon.cursor()
        cur.execute(f"select * from users where username='{user.get()}'")
        data = cur.fetchone()
        if data:
            user_error['text'] = "Username already exists"
            return
        global username, password
        username = user.get()
        password = pw.get()
        cur.execute(f"insert into users (username, password) values ('{username}', '{password}')")
        mycon.commit()
        history(root2)
        mycon.close()

    def on_enter(event):
        signin_link['font'] = ('Helvetica', 10)

    def on_leave(event):
        signin_link['font'] = ('Helvetica', 10, "underline")

    Label(root2, text='Library Title', font=('Helvetica', 25, "bold"), foreground='#1295d8', background='white').grid(
        row=1, column=1, columnspan=2, padx=(125, 40), pady=(15, 25))

    Label(root2, text="Username:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=3,
                                                                                                          column=1,
                                                                                                          padx=(80, 10),
                                                                                                          pady=(15, 15))
    username = StringVar()
    user = Entry(root2, textvariable=username, font=('Helvetica', 10), width=25)
    user.grid(row=3, column=2, padx=(10, 10))
    user.focus_set()
    user_error = Label(root2, text="", font=('Helvetica', 10), foreground='red', background='white')
    user_error.grid(row=4, column=1, columnspan=2, padx=(95, 15))

    Label(root2, text="Password:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=5,
                                                                                                          column=1,
                                                                                                          padx=(80, 10),
                                                                                                          pady=(15, 15))
    password = StringVar()
    pw = Entry(root2, textvariable=password, show='*', font=('Helvetica', 10), width=25)
    pw.grid(row=5, column=2, padx=(10, 10))
    pw_error = Label(root2, text="", font=('Helvetica', 10), foreground='red', background='white')
    pw_error.grid(row=6, column=1, columnspan=2, padx=(95, 15))

    show_pw = IntVar(value=0)
    show = Checkbutton(root2, text='Show Password', font=('Helvetica', 10), foreground='#1295d8', background='white',
                       variable=show_pw, onvalue=1, offvalue=0, command=my_show)
    show.grid(row=7, column=1, columnspan=2, padx=(95, 10))
    register = Button(root2, text="Register", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                      activebackground='#096696', activeforeground='white', command=add)
    register.grid(row=8, column=1, columnspan=2, padx=(130, 40), pady=(15, 25))

    root2.bind("<Return>", add)

    signin_link = Button(root2, text="Already have an account?", relief=FLAT, font=('Helvetica', 10, "underline"),
                         foreground='#1295d8', background='white', command=lambda: signin(root2))
    signin_link.grid(row=9, column=1, columnspan=2, padx=(95, 10))
    signin_link.bind("<Enter>", on_enter)
    signin_link.bind("<Leave>", on_leave)

    root2.mainloop()


def signin(root2=None):
    if root2:
        root2.destroy()

    def my_show():
        if show_pw.get() == 1:
            pw.config(show='')
        else:
            pw.config(show='*')

    def check(event="<Return>"):
        error = False
        user_error['text'] = ""
        pw_error['text'] = ""
        if not user.get():
            user_error['text'] = "Username field is empty"
            error = True
        if not pw.get():
            pw_error['text'] = "Password field is empty"
            error = True
        if error:
            return
        mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
        cur = mycon.cursor()
        cur.execute(f"select * from users where username='{user.get()}' and password='{pw.get()}'")
        data = cur.fetchone()
        if not data:
            pw_error['text'] = "Incorrect username or password"
            return
        global username, password
        username = user.get()
        password = pw.get()
        history(root1)
        mycon.close()

    def on_enter(event):
        signup_link['font'] = ('Helvetica', 10)

    def on_leave(event):
        signup_link['font'] = ('Helvetica', 10, "underline")

    root1 = Tk()
    root1.config(padx=20, pady=20, bg='white')
    root1.title('Log In')
    root1.geometry("500x500")

    Label(root1, text='Library Title', font=('Helvetica', 25, "bold"), foreground='#1295d8', background='white').grid(
        row=1, column=1, columnspan=2, padx=(125, 40), pady=(15, 25))

    Label(root1, text="Username:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=3,
                                                                                                          column=1,
                                                                                                          padx=(80, 10),
                                                                                                          pady=(15, 15))
    username = StringVar()
    user = Entry(root1, textvariable=username, font=('Helvetica', 10), width=25)
    user.grid(row=3, column=2, padx=(10, 10))
    user.focus_set()
    user_error = Label(root1, text="", font=('Helvetica', 10), foreground='red', background='white')
    user_error.grid(row=4, column=1, columnspan=2, padx=(95, 15))

    Label(root1, text="Password:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=5,
                                                                                                          column=1,
                                                                                                          padx=(80, 10),
                                                                                                          pady=(15, 15))
    password = StringVar()
    pw = Entry(root1, textvariable=password, show='*', font=('Helvetica', 10), width=25)
    pw.grid(row=5, column=2, padx=(10, 10))
    pw_error = Label(root1, text="", font=('Helvetica', 10), foreground='red', background='white')
    pw_error.grid(row=6, column=1, columnspan=2, padx=(95, 15))

    show_pw = IntVar(value=0)
    show = Checkbutton(root1, text='Show Password', font=('Helvetica', 10), foreground='#1295d8', background='white',
                       variable=show_pw, onvalue=1, offvalue=0, command=my_show)
    show.grid(row=7, column=1, columnspan=2, padx=(95, 10))

    login = Button(root1, text="Log In", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                   activebackground='#096696', activeforeground='white', command=check)
    login.grid(row=8, column=1, columnspan=2, padx=(130, 40), pady=(15, 25))

    root1.bind("<Return>", check)

    signup_link = Button(root1, text="Don't have an account?", relief=FLAT, font=('Helvetica', 10, "underline"),
                         foreground='#1295d8', background='white', command=lambda: signup(root1))
    signup_link.grid(row=9, column=1, columnspan=2, padx=(95, 10))
    signup_link.bind("<Enter>", on_enter)
    signup_link.bind("<Leave>", on_leave)

    root1.mainloop()


def history(root=None):
    def checknumissuer(username):
        mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
        cur = mycon.cursor()
        cur.execute(f"select current from users")
        data = (cur.fetchone())[0]
        data = eval(data)
        error = False
        issue_error['text'] = ""
        if len(data) >= 3:
            issue_error['text'] = "You cannot issue more than 3 books"
            error = True
        if error:
            return
        issuebook(root3)
    if root:
        root.destroy()
    root3 = Tk()
    root3.config(padx=20, pady=20, bg='white')
    root3.title('Issue History')
    root3.geometry("500x500")
    root3.after(1, lambda: root3.focus_force())
    Label(root3, text='Issue History', font=('Helvetica', 25, "bold"), foreground='#1295d8', background='white').grid(
        row=1, column=1, columnspan=2, padx=(125, 40), pady=(15, 25))
    signout = Button(root3, text="Sign Out", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                     activebackground='#096696', activeforeground='white', command=lambda: signin(root3))
    signout.grid(row=1, column=3, padx=(15, 40), pady=(15, 25))

    issue = Button(root3, text="Issue Book", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                   activebackground='#096696', activeforeground='white', command=lambda: checknumissuer(username))
    issue.grid(row=2, column=1, columnspan=2, padx=(130, 40), pady=(5, 5))
    issue_error = Label(root3, text="", font=('Helvetica', 10), foreground='red', background='white')
    issue_error.grid(row=3, column=1, columnspan=2, padx=(95, 15))
    Label(root3, text="Recently Issued", font=('Helvetica', 12, "bold"), foreground='#1295d8', background='white').grid(
        row=4,
        column=1,
        padx=(30, 0),
        pady=(5, 5))
    row_count = 5
    mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
    cur = mycon.cursor()
    cur.execute(f"select history from users where username='{username}' and password='{password}'")
    data = cur.fetchone()
    if data[0] == "[]":
        book_list_history = ["None"]
    else:
        book_list_history = eval(data[0])
    for book in book_list_history:
        if book == "None":
            Label(root3, text="None", font=('Helvetica', 10), foreground='#1295d8', background='white').grid(
                row=row_count, column=1, padx=(30, 0), pady=(5, 0))
            break
        cur.execute(f"select author from books where name='{book}'")
        data = cur.fetchone()
        Label(root3, text=book, font=('Helvetica', 10), foreground='#1295d8', background='white').grid(
            row=row_count, column=1, padx=(30, 0), pady=(5, 0))
        Label(root3, text=data[0], font=('Helvetica', 8), foreground='black', background='white').grid(
            row=row_count + 1, column=1, padx=(30, 0), pady=(0, 10))
        row_count += 2

    Label(root3, text="Currently Issued", font=('Helvetica', 12, "bold"), foreground='#1295d8',
          background='white').grid(row=4,
                                   column=2,
                                   padx=(30, 0),
                                   pady=(5, 5))
    row_count = 5
    cur.execute(f"select current from users where username='{username}' and password='{password}'")
    data = cur.fetchone()
    if data[0] == "[]":
        book_list_curr = ["None"]
    else:
        book_list_curr = eval(data[0])
    for book in book_list_curr:
        if book == "None":
            Label(root3, text="None", font=('Helvetica', 10), foreground='#1295d8', background='white').grid(
                row=row_count, column=2, padx=(30, 0), pady=(5, 0))
            break
        cur.execute(f"select author from books where name='{book}'")
        data = cur.fetchone()
        Label(root3, text=book, font=('Helvetica', 10), foreground='#1295d8', background='white').grid(
            row=row_count, column=2, padx=(30, 0), pady=(5, 0))
        Label(root3, text=data[0], font=('Helvetica', 8), foreground='black', background='white').grid(
            row=row_count + 1, column=2, padx=(30, 0), pady=(0, 10))
        Button(root3, text="Return", fg="white", bg="#1295d8", font=('Helvetica', 10), relief=FLAT,
                               activebackground='#096696', activeforeground='white', command=lambda book=book: return_fn(root3, book_list_history, book_list_curr, book)).grid(row=row_count, column=3, padx=(0, 10), pady=(10, 0), rowspan=2)
        row_count += 2
    mycon.close()


def issuebook(root=None):
    def search(event=None):
        name = book_name.get()
        author = auth.get()
        error = False
        book_error['text'] = ""
        auth_error['text'] = ""
        if not name:
            book_error['text'] = "Title field is empty"
            error = True
        if not author:
            auth_error['text'] = "Author field is empty"
            error = True
        if error:
            return
        mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
        cur = mycon.cursor()
        cur.execute(f"select current from users where username='{username}' and password='{password}'")
        data = cur.fetchone()
        if data[0] == "[]":
            book_list_curr = ["None"]
        else:
            book_list_curr = eval(data[0])
        cur.execute(f"select author from books where name='{name.title()}'")
        author_name = cur.fetchone()
        if not author_name:
            author_name = author.title()
            auth_names = []
        else:
            author_name = author_name[0]
            auth_names = author_name.split()
        if name.title() in book_list_curr and (author.title() in auth_names or author.title() == author_name):
            auth_error['text'] = "Book already issued"
            error = True
        if error:
            return
        cur.execute("select name from books")
        data = cur.fetchall()
        fetch_book_webpg(name)
        summary = show_summary()
        summary += "..."
        i = 0
        while i < len(summary):
            summary = summary[:i] + "\n" + summary[i:]
            i += 70
        summary = "Summary:\n" + summary
        Label(root4, text=summary, font=('Helvetica', 8), foreground='black', background='white').grid(row=7, column=0,
                                                                                                       columnspan=4,
                                                                                                       rowspan=7,
                                                                                                       padx=(0, 0),
                                                                                                       pady=(80, 0))
        end_session()
        issue_bn.grid(row=7, column=0, columnspan=2, padx=(140, 40), pady=(0, 0))
        inform_issue.grid_forget()

    def addtocurrent():
        mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
        cur = mycon.cursor()
        cur.execute("select name from books")
        data = cur.fetchall()
        cur.execute(f"select current from users where username='{username}' and password='{password}'")
        data = cur.fetchone()
        if data[0] == "[]":
            book_list_curr = []
        else:
            book_list_curr = eval(data[0])
        book_list_curr.append((book_name.get()).title())
        cur.execute(f"update users set current=\"{str(book_list_curr)}\" where username='{username}'")
        mycon.commit()
        inform_issue.grid(row=7, column=0, columnspan=2, padx=(140, 40), pady=(0, 0))
        inform_issue['text'] = "Issued"
        issue_bn.grid_forget()
    if root:
        root.destroy()
    root4 = Tk()
    root4.config(padx=20, pady=20, bg='white')
    root4.title('Issue History')
    root4.geometry("500x500")
    root4.after(1, lambda: root4.focus_force())
    Label(root4, text='Issue Book', font=('Helvetica', 25, "bold"), foreground='#1295d8', background='white').grid(
        row=1, column=0, columnspan=2, padx=(135, 35), pady=(15, 25))
    back = Button(root4, text="Back", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                  activebackground='#096696', activeforeground='white', command=lambda: history(root4))
    back.grid(row=1, column=0, padx=(10, 130), pady=(15, 25))
    signout = Button(root4, text="Sign Out", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                     activebackground='#096696', activeforeground='white', command=lambda: signin(root4))
    signout.grid(row=1, column=3, padx=(20, 0), pady=(15, 25))

    Label(root4, text="Title:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=2,
                                                                                                          column=0,
                                                                                                          padx=(70, 10),
                                                                                                          pady=(15, 15))
    title = StringVar()
    book_name = Entry(root4, textvariable=title, font=('Helvetica', 10), width=20)
    book_name.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))
    book_name.focus_set()
    book_error = Label(root4, text="", font=('Helvetica', 10), foreground='red', background='white')
    book_error.grid(row=3, column=0, columnspan=3, padx=(125, 15), pady=(0, 0))

    Label(root4, text="Author:", font=('Helvetica', 12), foreground='#1295d8', background='white').grid(row=4,
                                                                                                          column=0,
                                                                                                          padx=(70, 10),
                                                                                                          pady=(15, 15))
    author = StringVar()
    auth = Entry(root4, textvariable=author, font=('Helvetica', 10), width=20)
    auth.grid(row=4, column=1, padx=(0, 10), pady=(0, 0))
    auth_error = Label(root4, text="", font=('Helvetica', 10), foreground='red',
                       background='white')
    auth_error.grid(row=5, column=0, columnspan=3, padx=(125, 15), pady=(0, 0))
    search_bn = Button(root4, text="Search", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                   activebackground='#096696', activeforeground='white', command=search)
    search_bn.grid(row=6, column=0, columnspan=2, padx=(140, 40), pady=(0, 0))
    issue_bn = Button(root4, text="Issue", fg="white", bg="#1295d8", font=('Helvetica', 12), relief=FLAT,
                       activebackground='#096696', activeforeground='white', command=addtocurrent)
    issue_bn.grid_forget()
    inform_issue = Label(root4, text="", font=('Helvetica', 12), foreground='#1295d8', background='white')
    inform_issue.grid_forget()

    root4.bind("<Return>", search)


def return_fn(root, hist, curr, book):
    mycon = pm.connect(host='localhost', user='root', password='qwerty', database='library')
    cur = mycon.cursor()
    hist.append(book)
    if len(hist) > 5:
        hist.pop(0)
    curr.remove(book)
    cur.execute(f"update users set current=\"{str(curr)}\" where username='{username}'")
    mycon.commit()
    cur.execute(f"update users set history=\"{str(hist)}\" where username='{username}'")
    mycon.commit()
    history(root)

signin()
