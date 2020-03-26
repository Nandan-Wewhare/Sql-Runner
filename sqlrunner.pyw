from tkinter import *
import pymysql
from tkinter.ttk import Combobox
from tkinter import messagebox

db = pymysql.connect("localhost", "root", "", "")
cursor = db.cursor()

w1 = Tk()
w1.resizable(0, 0)
w1.minsize(width=400, height=400)
w1.title("SQL RUNNER")
w1.config(bg="khaki1")


def close():
    w1.destroy()


def view():
    w2 = Tk()
    w2.resizable(0, 0)
    w2.minsize(width=600, height=600)
    w2.title("View Something")
    w2.config(bg="powderblue")

    dblist = []
    data1 = "~~Select Database~~"
    dblist.insert(0, data1)
    tablelist = []
    data2 = "~~Select Table~~"
    tablelist.insert(0, data2)

    lblcombodb = Label(w2, text="Select Database:", bg="powderblue", fg="black")
    lblcombodb.place(x=30, y=80)

    sql1 = "show databases"
    cursor.execute(sql1)

    seldb = Combobox(w2, state="readonly")
    seldb.place(x=30, y=100)
    r1 = cursor.fetchall()
    for i in r1:
        dblist.append(i[0])
        seldb['values'] = dblist
    seldb.current(0)

    lblcombotable = Label(w2, text="Select Table:", bg="powderblue", fg="black")
    lblcombotable.place(x=30, y=130)

    seltable = Combobox(w2, state="readonly")
    seltable.place(x=30, y=150)

    def done():
        seltable.delete(0, END)
        if seldb.get() == "~~Select Database~~":
            messagebox.showwarning("Warning", " Please select a Database")
        else:
            sql2 = "use %s" % seldb.get()
            cursor.execute(sql2)
            sql3 = "show tables"
            cursor.execute(sql3)
            r2 = cursor.fetchall()
            if r2 != ():
                del tablelist[1:]
                for j in r2:
                    tablelist.append(j)
                    seltable['values'] = tablelist
                seltable.current(0)
    reslist = []
    lblresult = Label(w2, text="Result:", bg="powderblue", fg="black", font=("", 10, "bold"))
    lblresult.place(x=10, y=300)

    def desc():
        reslist.clear()
        txtresult = Text(w2, width=50, height=15)
        txtresult.place(x=10, y=330)
        if seltable.get() == "~~Select Table~~":
            messagebox.showwarning("WARNING", "Please select a table to describe")
        elif seltable.get() == "":
            messagebox.showerror("ERROR", "No Tables in Database:\n %s" % seldb.get())
        else:
            sql4 = "desc %s" % seltable.get()
            cursor.execute(sql4)
            r3 = cursor.fetchall()
            for k in r3:
                reslist.append(list(k))
                reslist.append("\n")
            txtresult.delete("1.0", END)
            txtresult.insert(INSERT, reslist)
            txtresult.config(state=DISABLED)

    def showval():
        reslist.clear()
        if seltable.get() == "~~Select Table~~" or seldb.get() == "~~Select Database~~":
            messagebox.showwarning("WARNING", "Please select a Database and a Table")
        elif seltable.get() == "":
            messagebox.showerror("ERROR", "No Tables in Database:\n %s" % seldb.get())
        else:
            sql4 = "select * from %s" % seltable.get()
            cursor.execute(sql4)
            r3 = cursor.fetchall()
            if r3 == ():
                txtresult = Text(w2, width=50, height=15)
                txtresult.place(x=10, y=300)
                txtresult.delete("1.0", END)
                txtresult.insert(INSERT, "No Values Available")
            else:
                for k in r3:
                    reslist.append(list(k))
                    reslist.append("\n")
                txtresult = Text(w2, width=50, height=15)
                txtresult.place(x=10, y=300)
                txtresult.delete("1.0", END)
                txtresult.insert(INSERT, reslist)
                txtresult.config(state=DISABLED)

    btnback1 = Button(w2, text="<< Back", width=10, command=w2.destroy)
    btnback1.place(x=10, y=20)

    btndone = Button(w2, text="Done", width=5, command=done)
    btndone.place(x=200, y=100)

    btndesc = Button(w2, text="Describe\nTable", width=10, command=desc)
    btndesc.place(x=150, y=220)

    btnshow = Button(w2, text="Show all\nValues", width=10, command=showval)
    btnshow.place(x=250, y=220)
    w2.mainloop()


def execute():
    w3 = Tk()
    w3.resizable(0, 0)
    w3.minsize(width=300, height=300)
    w3.title("Execute a Query")
    w3.config(bg="mediumorchid1")

    btnback2 = Button(w3, text="<< Back", width=10, command=w3.destroy)
    btnback2.place(x=10, y=20)

    def create():
        w4 = Tk()
        w4.resizable(0, 0)
        w4.minsize(width=600, height=600)
        w4.title("Create")
        w4.config(bg="mediumorchid1")

        btnback3 = Button(w4, text="<< Back", width=10, command=w4.destroy)
        btnback3.place(x=10, y=20)

        sql1 = "show databases"
        cursor.execute(sql1)

        dblistcreate = []
        data1 = "~~Create New Database~~"
        dblistcreate.insert(0, data1)
        seldb = Combobox(w4, state="readonly")
        seldb.place(x=30, y=100)
        r1 = cursor.fetchall()
        for i in r1:
            dblistcreate.append(i[0])
            seldb['values'] = dblistcreate
        seldb.current(0)

        '''def donecreate():
            if seldb.get() == "~~Create New Database~~":
                    #create new database definition
            else:
                sql2 = "use %s" % seldb.get()
                cursor.execute(sql2)'''

        btndonecreate = Button(w4, text="Done", width=5, command=donecreate)
        btndonecreate.place(x=200, y=100)

        lbltable = Label(w4, text="Enter Table Name:", bg="powderblue", fg="black")
        lbltable.place(x=20, y=150)
        txttable = Entry(w4, width=20)
        txttable.place(x=130, y=150)

        lblcolno = Label(w4, text="No. of columns:", bg="powderblue", fg="black")
        lblcolno.place(x=20, y=180)
        spincolno = Spinbox(w4, from_=1, to=10, width=5)
        spincolno.place(x=160, y=180)

        w4.mainloop()

    def update():
        pass

    def delete():
        pass

    btncreate = Button(w3, text="Create", width=10, command=create)
    btncreate.place(x=70, y=70)

    btnupdate = Button(w3, text="Update", width=10, command=update)
    btnupdate.place(x=110, y=120)

    btndelete = Button(w3, text="Delete", width=10, command=delete)
    btndelete.place(x=150, y=170)

    w3.mainloop()


btnview = Button(w1, text="View\nSomething", width=8, command=view)
btnview.place(x=100, y=150)

btnexe = Button(w1, text="Execute a\n Query", width=8, command=execute)
btnexe.place(x=220, y=150)

btnclose = Button(w1, text="Close", width=8, command=close)
btnclose.place(x=160, y=220)

w1.mainloop()
