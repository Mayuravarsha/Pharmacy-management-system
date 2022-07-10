from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
DB_HOST = "localhost"
DB_NAME = "pharmacy_mang"
login_screen = Tk() 
#conn = psycopg2.connect(dbname=DB_NAME, user="med1001", password="rameshr", host=DB_HOST)
#cur=conn.cursor()
#defining login function
def login():
    #getting form data
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("fill the empty field!!!")
    else:
        try:
            DB_USER = uname
            DB_PASS = pwd
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            global cur
            cur=conn.cursor()
            if(DB_USER[:3]=="med"):
                employee()
            else:
                admin()
        except Exception:
            message.set("Wrong username or password!!!")
#defining loginform function
def Loginform():
    global login_screen
    #Setting title of screen
    login_screen.title("Login Form")
    #setting height and width of screen
    login_screen.geometry("320x280")
    #declaring variable
    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message=StringVar()
    #Creating layout of login form
    Label(login_screen,width="300", text="MedCare Login",font=("",15), bg="orange",fg="white").pack()
    #Username Label
    Label(login_screen, text="Username * ",font=("",9)).place(x=20,y=60)
    #Username textbox
    Entry(login_screen, textvariable=username,width=25).place(x=105,y=62)
    #Password Label
    Label(login_screen, text="Password * ",font=("",9)).place(x=20,y=100)
    #Password textbox
    Entry(login_screen, textvariable=password ,show="*",width=25).place(x=105,y=102)
    #Label for displaying login status[success/failed]
    Label(login_screen, text="",textvariable=message, fg="red").place(x=110,y=125)
    #Login button
    Button(login_screen, text="Login", width=13, height=1, bg="skyblue",font=("",10), command=login).place(x=105,y=155)
    login_screen.mainloop()
def employee():
    for i in login_screen.winfo_children():
       i.destroy()
    login_screen.geometry("900x500")
    frame0=Frame(login_screen,bg="blue")
    frame0.pack()
    b1=Button(frame0, text="Store_Details", width=20, command=SD)
    b1.grid(row=0,column=0,padx=30,pady=20)
    b2=Button(frame0, text="Patients_records", width=20, command=PR)
    b2.grid(row=0,column=1,padx=30,pady=20)
    b3=Button(frame0, text="Billing", width=20, command=Bill)
    b3.grid(row=0,column=2,padx=30,pady=20)
    b4=Button(frame0, text="Medicines", width=20,command=medicine)
    b4.grid(row=0,column=3,padx=30,pady=20)
    global frame1
    frame1=Frame(login_screen)
    frame1.pack()
    login_screen.mainloop()

def admin():
    for i in login_screen.winfo_children():
       i.destroy()
    login_screen.geometry("900x500")
    frame0=Frame(login_screen,bg="green")
    frame0.pack()
    b1=Button(frame0, text="Employees", width=15, command=employee_details)
    b1.grid(row=0,column=0,padx=20,pady=20)
    b2=Button(frame0, text="Patients", width=15, command=Patients)
    b2.grid(row=0,column=1,padx=20,pady=20)
    b3=Button(frame0, text="Bills", width=15, command=admin_bill)
    b3.grid(row=0,column=2,padx=20,pady=20)
    b4=Button(frame0, text="Medicines", width=15,command=admin_med)
    b4.grid(row=0,column=3,padx=20,pady=20)
    b4=Button(frame0, text="Doctors", width=15,command=doctor)
    b4.grid(row=0,column=4,padx=20,pady=20)
    global frame1
    frame1=Frame(login_screen)
    frame1.pack()
    login_screen.mainloop()

def employee_details():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by store_id:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("1", "2", "3") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("employee"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    b2=Button(frame2,text="Search",command=lambda: search("employee","store_id",option.get()))
    b2.grid(row=1,column=0,padx=10)
    b3=Button(frame2,text="+ADD",width=10,bg="blue",fg="white",command=add_emp)
    b3.grid(row=1,column=3,padx=80)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def Patients():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by category:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("Store_id", "doc_id", "p_sex") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("patient"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    l2=Label(frame2,font=("",10),text="Entry the value:")
    l2.grid(row=1,column=0)
    text=StringVar(frame2)
    e1=Entry(frame2,textvariable = text)
    e1.grid(row=1,column=1)
    b2=Button(frame2,text="Search",command=lambda: search("patient",option.get(),text.get()))
    b2.grid(row=1,column=2,padx=10)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def admin_bill():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by store_id:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("1", "2", "3") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("bill"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    b2=Button(frame2,text="Search",command=lambda: search("bill","store_id",option.get()))
    b2.grid(row=1,column=0,padx=10)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def admin_med():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by category:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("drug_id", "drug_name", "manufacturer","store_id") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("medicine"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    l2=Label(frame2,font=("",10),text="Entry the value:")
    l2.grid(row=1,column=0)
    text=StringVar(frame2)
    e1=Entry(frame2,textvariable = text)
    e1.grid(row=1,column=1)
    b2=Button(frame2,text="Search",command=lambda: search("medicine",option.get(),text.get()))
    b2.grid(row=1,column=2,padx=10)
    b3=Button(frame2,text="ADD Stock",width=10,bg="blue",fg="white",command=add_med)
    b3.grid(row=1,column=3,padx=80)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def doctor():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by store_id:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("1", "2", "3") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("doctor"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    b2=Button(frame2,text="Search",command=lambda: search("doctor","store_id",option.get()))
    b2.grid(row=1,column=0,padx=10)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def SD():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    try:
        cur.execute("select distinct store_id from employee")
        store_id=cur.fetchone()[0]
        cur.execute("select storename from pharmacy where store_id=%s",(store_id,))
        storename=cur.fetchone()[0]
    except Exception as e:
        print(e)
        messagebox.showerror("","error retrieving values")
        cur.execute("END")
        return
    l1=Label(frame2,font=("Comic Sans MS",20),text="Store."+str(store_id)+" "+storename)
    l1.pack()
    l2=Label(frame2,font=("Comic Sans MS",15),text="Employees")
    l2.pack()
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1,width='500',height='200')
    frame3.pack(pady=20)
    try:
        cur.execute("select eid,empname,e_address,e_sex,e_contact from employee")
        details=cur.fetchall()
    except Exception as e:
        messagebox.showerror("","error retrieving values")
        cur.execute("END")
        return
    col=['id','name','address','sex','contact']
    t=ttk.Treeview(frame3,height=5,show='headings',columns=col)
    t.column('id',width='50',anchor=CENTER)
    t.column('name',width='80',anchor=CENTER)
    t.column('address',width='200',anchor=CENTER)
    t.column('sex',width='50',anchor=CENTER)
    t.column('contact',width='80',anchor=CENTER)

    t.heading('id',text='ID')
    t.heading('name',text='Name')
    t.heading('address',text='Address')
    t.heading('sex',text='Sex')
    t.heading('contact',text='Contact')
    t.pack(side=TOP,fill=BOTH)
    for i in range(len(details)):
	    t.insert('',i,values=details[i])

def PR():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by category:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("pname", "phone_no", "pid") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("patient"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    l2=Label(frame2,font=("",10),text="Entry the value:")
    l2.grid(row=1,column=0)
    text=StringVar(frame2)
    e1=Entry(frame2,textvariable = text)
    e1.grid(row=1,column=1)
    b2=Button(frame2,text="Search",command=lambda: search("patient",option.get(),text.get()))
    b2.grid(row=1,column=2,padx=10)
    b3=Button(frame2,text="+ADD",width=10,bg="green",fg="white",command=add)
    b3.grid(row=1,column=3,padx=80,)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def Bill():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by PID:")
    l1.grid(row=0,column=0,pady=10)
    pid=StringVar(frame2)
    e1=Entry(frame2,textvariable = pid)
    e1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Search",width=12,command=lambda: search("bill","pid",pid.get()))
    b1.grid(row=1,column=0)
    b2=Button(frame2,text="BILL",width=11,bg="green",fg="white",font=("",10),command=add_bill)
    b2.grid(row=1,column=2,padx=60)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def medicine():
    for i in frame1.winfo_children():
        i.destroy()
    frame2=Frame(frame1)
    frame2.pack(padx=10,pady=10)
    l1=Label(frame2,font=("",10),text="Select by category:")
    l1.grid(row=0,column=0,pady=10)
    option = StringVar(frame2)
    OPTION_TUPLE = ("drug_id", "drug_name", "manufacturer") 
    o1=OptionMenu(frame2,option,*OPTION_TUPLE)
    o1.grid(row=0,column=1,pady=10)
    b1=Button(frame2,text="Show all",bg="orange",fg="white",width=12,font=("",10),command=lambda: showall("medicine"))
    b1.grid(row=0,column=3,padx=80,pady=10)
    l2=Label(frame2,font=("",10),text="Entry the value:")
    l2.grid(row=1,column=0)
    text=StringVar(frame2)
    e1=Entry(frame2,textvariable = text)
    e1.grid(row=1,column=1)
    b2=Button(frame2,text="Search",command=lambda: search("medicine",option.get(),text.get()))
    b2.grid(row=1,column=2,padx=10)
    global frame3
    frame3=Frame(frame1,highlightbackground="black",highlightthicknes=1)
    frame3.pack()

def search(table,option,value):
    if(option=='' or value==''):
        messagebox.showwarning("","fields left blank")
        return
    for i in frame3.winfo_children():
        i.destroy()
    if(table=="medicine"):
        col=['ID','Name','Mfg-date','Exp-date','unit_price','manufacturer','quantity','Store_id']
        width=['50','80','90','90','60','130','50','50']
        if(option=="store_id"):
            option="c."+option
        else:
            option="m."+option
        try:
            cur.execute("select  m.drug_id,drug_name,mfgdate,expdate,price,manufacturer,quantity,store_id from "+table+" as m,contains as c where m.drug_id=c.drug_id and "+option+"=%s",(value,))
            details=cur.fetchall()
        except Exception as e:
            messagebox.showwarning("","type error")
            cur.execute("END")
            return
    elif(table=="doctor"):
        col=['ID','Name','Address','contact','Hospital','Store_id']
        width=['50','80','200','50','120','50']
        try:
            cur.execute("select d.doc_id,doc_name,d_address,d_contact,hospital,a.store_id from "+table+" as d,associated_with as a where d.doc_id=a.doc_id and "+option+"=%s",(value,))
            details=cur.fetchall()
        except Exception as e:
            messagebox.showwarning("","type error")
            cur.execute("END")
            return
    else:
        if(table=="patient"):
            col=['ID','Name','Address','Sex','Contact','Doc_id']
            width=['50','80','200','50','80','50']
        elif(table=="employee"):
            col=['ID','Name','Address','Sex','Salary','Contact','Store_id']
            width=['50','80','200','50','70','80','50']
        else:
            col=['Bill_id','PID','Doc_id','Drug_id','quantity','Amt','Store_id']
            width=['50','50','50','50','50','60','50']
        try:
            cur.execute("select * from "+table+" where "+option+"=%s",(value,))
            details=cur.fetchall()
        except Exception as e:
            messagebox.showwarning("","type error")
            cur.execute("END")
            return
    t=ttk.Treeview(frame3,height=5,show='headings',columns=col)
    for i in range(len(col)):
        t.column(col[i],width=width[i],anchor=CENTER)
        t.heading(col[i],text=col[i])
    t.pack(side=TOP,fill=BOTH)
    for i in range(len(details)):
       t.insert('',i,values=details[i])

def showall(table):
    for i in frame3.winfo_children():
        i.destroy()
    if(table=="medicine"):
        col=['ID','Name','Mfg-date','Exp-date','unit_price','manufacturer','quantity','Store_id']
        width=['50','80','90','90','60','130','50','50']
        try:
            cur.execute("select  m.drug_id,drug_name,mfgdate,expdate,price,manufacturer,quantity,store_id from "+table+" as m,contains as c where m.drug_id=c.drug_id")
            details=cur.fetchall()
        except Exception as e:
            messagebox.showerror("","error retrieving values")
            cur.execute("END")
            return
    elif(table=="doctor"):
        col=['ID','Name','Address','contact','Hospital','Store_id']
        width=['50','80','200','50','120','50']
        try:
            cur.execute("select  d.doc_id,doc_name,d_address,d_contact,hospital,a.store_id from "+table+" as d,associated_with as a where d.doc_id=a.doc_id")
            details=cur.fetchall()
        except Exception as e:
            messagebox.showwarning("","error retrieving values")
            cur.execute("END")
            return
    else:
        if(table=="patient"):
            col=['ID','Name','Address','Sex','Contact','Doc_id']
            width=['50','80','200','50','80','50']
        elif(table=="employee"):
            col=['ID','Name','Address','Sex','Salary','Contact','Store_id']
            width=['50','80','200','50','70','80','50']
        else:
            col=['Bill_id','PID','Doc_id','Drug_id','quantity','Amt','Store_id']
            width=['50','50','50','50','50','60','50']
        try:
            cur.execute("select * from "+table)
            details=cur.fetchall()
        except Exception as e:
            messagebox.showerror("","error retrieving values")
            cur.execute("END")
            return
    t=ttk.Treeview(frame3,height=5,show='headings',columns=col)
    for i in range(len(col)):
        t.column(col[i],width=width[i],anchor=CENTER)
        t.heading(col[i],text=col[i])
    t.pack(side=TOP,fill=BOTH)
    for i in range(len(details)):
       t.insert('',i,values=details[i])

def add():
    for i in frame3.winfo_children():
        i.destroy()
    frame3.pack(padx=10,pady=10,ipadx=10,ipady=10)
    l1=Label(frame3,font=("",10),text="Name")
    l1.grid(row=0,column=0,pady=10,padx=5)
    name=StringVar(frame3)
    e1=Entry(frame3,textvariable = name)
    e1.grid(row=0,column=1,pady=10)
    l2=Label(frame3,font=("",10),text="Sex")
    l2.grid(row=1,column=0,pady=10,padx=5)
    sex=StringVar(frame3)
    OPTION_TUPLE = ("Male", "Female", "Other") 
    o1=OptionMenu(frame3,sex,*OPTION_TUPLE)
    o1.grid(row=1,column=1,pady=5)
    l3=Label(frame3,font=("",10),text="Contact_no")
    l3.grid(row=2,column=0,pady=10,padx=5)
    contact=StringVar(frame3)
    e3=Entry(frame3,textvariable = contact)
    e3.grid(row=2,column=1,pady=10)
    l4=Label(frame3,font=("",10),text="Doc_ID")
    l4.grid(row=3,column=0,pady=10,padx=5)
    doc_id=StringVar(frame3)
    e4=Entry(frame3,textvariable = doc_id)
    e4.grid(row=3,column=1,pady=10)
    l5=Label(frame3,font=("",10),text="Address")
    l5.grid(row=4,column=0,pady=10,padx=5)
    address=StringVar(frame3)
    e5=Entry(frame3,textvariable = address,width=25)
    e5.grid(row=4,column=1,pady=10)
    b1=Button(frame3,text="Submit",width=12,bg="orange",fg="white",command=lambda: submit1(name.get(),sex.get(),contact.get(),doc_id.get(),address.get()))
    b1.grid(row=5,column=1,pady=15)

def add_bill():
    for i in frame3.winfo_children():
        i.destroy()
    frame3.pack(padx=10,pady=10,ipadx=10,ipady=10)
    l1=Label(frame3,font=("",10),text="PID")
    l1.grid(row=0,column=0,pady=10,padx=5)
    pid=StringVar(frame3)
    e1=Entry(frame3,textvariable = pid)
    e1.grid(row=0,column=1,pady=10)
    l2=Label(frame3,font=("",10),text="Drug_name")
    l2.grid(row=1,column=0,pady=10,padx=5)
    name=StringVar(frame3)
    e2=Entry(frame3,textvariable = name)
    e2.grid(row=1,column=1,pady=10)
    l3=Label(frame3,font=("",10),text="Quantity")
    l3.grid(row=2,column=0,pady=10,padx=5)
    quantity=StringVar(frame3)
    e3=Entry(frame3,textvariable = quantity)
    e3.grid(row=2,column=1,pady=10)
    b1=Button(frame3,text="Submit",width=12,bg="orange",fg="white",command=lambda: submit2(pid.get(),name.get(),quantity.get()))
    b1.grid(row=3,column=1,pady=15)

def add_emp():
    for i in frame3.winfo_children():
        i.destroy()
    frame3.pack(padx=10,pady=10,ipadx=10,ipady=10)
    l1=Label(frame3,font=("",10),text="Name")
    l1.grid(row=0,column=0,pady=10,padx=5)
    name=StringVar(frame3)
    e1=Entry(frame3,textvariable = name)
    e1.grid(row=0,column=1,pady=10)
    l2=Label(frame3,font=("",10),text="Sex")
    l2.grid(row=1,column=0,pady=10,padx=5)
    sex=StringVar(frame3)
    OPTION_TUPLE = ("Male", "Female", "Other") 
    o1=OptionMenu(frame3,sex,*OPTION_TUPLE)
    o1.grid(row=1,column=1,pady=5)
    l3=Label(frame3,font=("",10),text="Contact_no")
    l3.grid(row=2,column=0,pady=10,padx=5)
    contact=StringVar(frame3)
    e3=Entry(frame3,textvariable = contact)
    e3.grid(row=2,column=1,pady=10)
    l4=Label(frame3,font=("",10),text="Store_ID")
    l4.grid(row=3,column=0,pady=10,padx=5)
    store_id=StringVar(frame3)
    e4=Entry(frame3,textvariable = store_id)
    e4.grid(row=3,column=1,pady=10)
    l5=Label(frame3,font=("",10),text="Salary")
    l5.grid(row=4,column=0,pady=10,padx=5)
    salary=StringVar(frame3)
    e5=Entry(frame3,textvariable = salary)
    e5.grid(row=4,column=1,pady=10)
    l6=Label(frame3,font=("",10),text="Address")
    l6.grid(row=5,column=0,pady=10,padx=5)
    address=StringVar(frame3)
    e6=Entry(frame3,textvariable = address,width=25)
    e6.grid(row=5,column=1,pady=10)
    b1=Button(frame3,text="Submit",width=12,bg="orange",fg="white",command=lambda: submit3(name.get(),sex.get(),contact.get(),store_id.get(),salary.get(),address.get()))
    b1.grid(row=6,column=1,pady=15)

def add_med():
    for i in frame3.winfo_children():
        i.destroy()
    frame3.pack(padx=10,pady=10,ipadx=10,ipady=10)
    l1=Label(frame3,font=("",10),text="Store_id")
    l1.grid(row=0,column=0,pady=10,padx=5)
    store_id=StringVar(frame3)
    e1=Entry(frame3,textvariable = store_id)
    e1.grid(row=0,column=1,pady=10)
    l2=Label(frame3,font=("",10),text="Drug_id")
    l2.grid(row=1,column=0,pady=10,padx=5)
    drug_id=StringVar(frame3)
    e2=Entry(frame3,textvariable = drug_id)
    e2.grid(row=1,column=1,pady=10)
    l3=Label(frame3,font=("",10),text="add_quantity")
    l3.grid(row=2,column=0,pady=10,padx=5)
    quantity=StringVar(frame3)
    e3=Entry(frame3,textvariable = quantity)
    e3.grid(row=2,column=1,pady=10)
    b1=Button(frame3,text="Add",width=12,bg="orange",fg="white",command=lambda: submit4(store_id.get(),drug_id.get(),quantity.get()))
    b1.grid(row=3,column=1,pady=15)

def submit1(name,sex,contact,doc_id,address):
    try:
        cur.execute("select distinct store_id from employee")
        store_id=cur.fetchone()[0]
        cur.execute("insert into patient (pname,p_address,p_sex,p_contact,doc_id,store_id) values (%s,%s,%s,%s,%s,%s)",(name,address,sex,contact,doc_id,store_id,))
        cur.execute("COMMIT")
    except Exception as e:
        messagebox.showwarning("","fields left blank or type error")
        cur.execute("END")
        add()
        return
    print("[+]successfully inserted patient\n")
    add()

def submit2(pid,name,quantity):
    try:
        cur.execute("select distinct store_id from employee")
        store_id=cur.fetchone()[0]
        cur.execute("select doc_id from patient where pid=%s",(pid,))
        doc_id=cur.fetchone()[0]
        cur.execute("select drug_id from medicine where drug_name=%s",(name,))
        drug_id=cur.fetchone()[0]
        cur.execute("select price from medicine where drug_id=%s",(drug_id,))
        unit_price=cur.fetchone()[0]
        cur.execute("select quantity from contains where drug_id=%s",(drug_id,))
        prev_quan=cur.fetchone()[0]
        amt=float(quantity)*unit_price
        if((prev_quan-int(quantity))>0):
            cur.execute("insert into bill (pid,doc_id,drug_id,quantity,amt,store_id) values (%s,%s,%s,%s,%s,%s)",(pid,doc_id,drug_id,quantity,amt,store_id,))
            cur.execute("COMMIT")
        elif((prev_quan-int(quantity))==0):
            cur.execute("insert into bill (pid,doc_id,drug_id,quantity,amt,store_id) values (%s,%s,%s,%s,%s,%s)",(pid,doc_id,drug_id,quantity,amt,store_id,))
            cur.execute("delete from contains where store_id=%s and drug_id=%s",(store_id,drug_id,))
            cur.execute("COMMIT")
        else:
            messagebox.showwarning("","Quantity exceeded")
            add_bill()
            return
    except Exception as e:
        print(e)
        messagebox.showwarning("","fields left blank or type error")
        cur.execute("END")
        add_bill()
        return
    cur.execute("select * from bill")
    result=cur.fetchall()[-1]
    List=["Bill_id: ","pid: ","doc_id: ","drug_id: ","quantity: ","Amt in rupees: ","store_id: "]
    msg="[+]successfully inserted bill\n\n"
    for i in range(0,len(result)):
        msg+=List[i]+str(result[i])+"\n"
    messagebox.showinfo("",msg)
    add_bill()

def submit3(name,sex,contact,store_id,salary,address):
    try:
        cur.execute("insert into employee (empname,e_address,e_sex,salary,e_contact,store_id) values (%s,%s,%s,%s,%s,%s)",(name,address,sex,salary,contact,store_id,))
        cur.execute("COMMIT")
    except Exception as e:
        messagebox.showwarning("","fields left blank or type error")
        cur.execute("END")
        add_emp()
        return
    messagebox.showinfo("","[+]successfully inserted employee")
    add_emp()

def submit4(store_id,drug_id,quantity):
    try:
        cur.execute("select quantity from contains where drug_id=%s",(drug_id,))
        prev_quan=cur.fetchone()[0]
        cur.execute("update contains set quantity=%s where drug_id=%s and store_id=%s",(prev_quan+int(quantity),drug_id,store_id))
        cur.execute("COMMIT")
    except Exception as e:
        messagebox.showwarning("","fields left blank or type error")
        cur.execute("END")
        add_med()
        return
    messagebox.showinfo("","[+]successfully updated")
    add_med()

Loginform()                                     