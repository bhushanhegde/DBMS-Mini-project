#! /usr/bin/python3
import pprint
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from tkinter import *
from prettytable import PrettyTable
import ttk
import os
import subprocess
import mysql.connector
from datetime import datetime
import time


db=mysql.connector.connect(host='localhost',user='root',passwd='PASSWORD',database='DATABASENAME')
cur=db.cursor()


root=Tk()
root.title("WELCOME TO AGRI MARKET")

#stored procedure
"""
    DELIMITER $$
    
    CREATE PROCEDURE getMonth(
        IN   month VARCHAR(2))
    BEGIN
        SELECT * FROM payment
        WHERE p_date LIKE CONCAT('____-',month,'%');
    END$$

    DELIMITER ;

"""

T1,T2,T3=0,0,0
def First_page(root):
    global T1,T2,T3
    frame=Frame(root,height=500,width=800,bg='ivory')
    frame.pack()

    label=Label(root,text='WELCOME TO AGRI MARKET',font=('Times new roman',25))
    label.place(x=200,y=50)

    button=Button(root,text='LogIn',font=('times new roman',20),command=check_pass,bg='green')
    button.place(x=350,y=350)

    L1 = tk.Label(root, text="Username", font=("Arial Bold", 15), bg='ivory')
    L1.place(x=150, y=200)
    T1 = tk.Entry(root, width = 30, bd = 5)
    T1.place(x=280, y=200)

    L2 = tk.Label(root, text="Password", font=("Arial Bold", 15), bg='ivory')
    L2.place(x=150, y=250)
    T2 = tk.Entry(root, width = 30, show='*', bd = 5)
    T2.place(x=280, y=250)

    reg_button=Button(root,text='Register',font=("Arial Bold",15),bg='blue',command=create_pass)
    reg_button.place(x=340,y=400)

def check_pass():
    global root,T1,T2,T3
    try:
        with open('password.txt','r')as f:
            lines=f.read()
            if T1.get()+'='+T2.get() in lines and T1.get()!='' and T2.get()!='':
                entity_page()
            else:
                label=Label(root,text='Invalid username or password.Try again',font=('times new roman',15))
                label.place(x=200,y=100)
    except:
        label=Label(root,text='Invalid username or password.Try again',font=('times new roman',15))
        label.place(x=200,y=100)

def create_pass():
    global root,T1,T2,T3


    #to clean up  previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='ivory')
    label.place(x=0,y=0)


    #this window
    L1 = tk.Label(root, text="Username", font=("Arial Bold", 15), bg='ivory')
    L1.place(x=150, y=200)
    T1 = tk.Entry(root, width = 30, bd = 5)
    T1.place(x=380, y=200)

    L2 = tk.Label(root, text="Password", font=("Arial Bold", 15), bg='ivory')
    L2.place(x=150, y=250)
    T2 = tk.Entry(root, width = 30, show='*', bd = 5)
    T2.place(x=380, y=250)

    L2 = tk.Label(root, text="Confirm Password", font=("Arial Bold", 15), bg='ivory')
    L2.place(x=150, y=300)
    T3 = tk.Entry(root, width = 30, show='*', bd = 5)
    T3.place(x=380, y=300)

    reg_button=Button(root,text='Done',font=("Arial Bold",15),bg='blue',command=add_pass)
    reg_button.place(x=440,y=400)


def add_pass():
    global root,T1,T2,T3

    if T2.get()!=T3.get():
        label=Label(root,text='Incorrect Password. Enter again',font=('times new roman',20))
        label.place(x=100,y=100)
    else:
        try:
            with open('password.txt','r')as f:
                data=f.read()
            with open('password.txt','w')as f:
                f.write(data+'\n')
                f.write(T1.get()+'='+T2.get())

            entity_page()
        except:
            with open('password.txt','w')as f:
                f.write(T1.get()+'='+T2.get())

            entity_page()

def entity_page():
    global root
    #cleaning previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='ivory')
    label.place(x=0,y=0)

    #this window
    label=Label(root,text='WELCOME TO AGRI MARKET ',font=('Times new roman',20),bg='blue')
    label.place(x=200,y=20)

    label=Label(root,text='Choose the Entity ',font=('Times new roman',20),bg='white')
    label.place(x=250,y=100)


    Button = tk.Button(root, text="Farmers", font=("Arial", 15),command=farmer)
    Button.place(x=100, y=150+25)

    Button = tk.Button(root, text="Company", font=("Arial", 15),command=company)
    Button.place(x=300, y=150+25)

    Button = tk.Button(root, text="Fertilizer", font=("Arial", 15),command=fertilizer)
    Button.place(x=500, y=150+25)

    Button = tk.Button(root, text="Order", font=("Arial", 15),command=orders)
    Button.place(x=200, y=300+25)

    Button = tk.Button(root, text="Payment", font=("Arial", 15),command=payment)
    Button.place(x=400, y=300+25)

    Button = tk.Button(root, text="GET BOOKING HISTORY", font=("Arial", 15),command=history)
    Button.place(x=200, y=400+25)

#history
def history():
    global root,cur,db
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    cur.execute("CALL getMonth(%s);",[datetime.today().strftime("%m")])
    data=cur.fetchall()
    
    label=Label(root,text="The Transaction History of this month",font=("Arial",15))
    label.place(x=200,y=20)

    button=Button(root,text='BACK',command=entity_page)
    button.place(x=20,y=20)

    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("trans_id",'p_f_id','p_date','p_amount','p_method'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('trans_id',text="Transaction Id")
    table.heading('p_f_id',text="Farmer Id")


    table.heading('p_date',text="Payment Date")
    table.heading('p_amount',text="Amount")
    table.heading('p_method',text="Payment Method")
    #table.heading('f_address',text="Farmer Address")
    table['show']='headings'

    #table.column("f_id",width=100)


    table.pack()



    #cur.execute("SELECT * FROM payment;")

    #data =cur.fetchall()
    #db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

    db.close()
    db=mysql.connector.connect(host='localhost',user='root',passwd='bhushi',database='farmer_app')
    cur=db.cursor()
    


#farmer page
def farmer():
    global root
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Farmer Table',font=('Times new roman',15),bg='white')
    label.place(x=350,y=10)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=entity_page)
    Button.place(x=10, y=50)

    Button = tk.Button(root, text="Insert", font=("Arial", 15),command=insert_farmer)
    Button.place(x=110, y=50)

    Button = tk.Button(root, text="Delete", font=("Arial", 15),command=delete_farmer)
    Button.place(x=210, y=50)

    Button = tk.Button(root, text="Update", font=("Arial", 15),command=update_farmer)
    Button.place(x=310, y=50)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_farmer)
    Button.place(x=410, y=50)

    view_farmer()


def view_farmer():
    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("f_id",'f_name','f_phone','f_mail','f_locality','f_address'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('f_id',text="Farmer Id")
    table.heading('f_name',text="Farmer Name")
    table.heading('f_phone',text="Farmer Phone")
    table.heading('f_mail',text="Farmer Mail")
    table.heading('f_locality',text="Farmer Locality")
    table.heading('f_address',text="Farmer Address")
    table['show']='headings'

    table.column("f_id",width=100)


    table.pack()



    cur.execute("SELECT * FROM farmer;")

    data =cur.fetchall()
    db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

e1,e2,e3,e4,e5,e6=0,0,0,0,0,0
def insert_farmer():
    global e1,e2,e3,e4,e5,e6
    #clean the window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    #create the window
    label=Label(root,text='Farmer_id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=10)

    label=Label(root,text='Farmer_name',font=('Times new roman',20),bg='white')
    label.place(x=50,y=60)

    label=Label(root,text='Farmer_phone',font=('Times new roman',20),bg='white')
    label.place(x=50,y=110)

    label=Label(root,text='Farmer_mail',font=('Times new roman',20),bg='white')
    label.place(x=50,y=160)

    label=Label(root,text='Farmer_locality',font=('Times new roman',20),bg='white')
    label.place(x=50,y=210)

    label=Label(root,text='Farmer_address',font=('Times new roman',20),bg='white')
    label.place(x=50,y=270)

    e1=Entry(root,width=50)
    e2=Entry(root,width=50)
    e3=Entry(root,width=50)
    e4=Entry(root,width=50)
    e5=Entry(root,width=50)
    e6=Entry(root,width=50)

    e1.place(x=350,y=10)
    e2.place(x=350,y=60)
    e3.place(x=350,y=110)
    e4.place(x=350,y=160)
    e5.place(x=350,y=210)
    e6.place(x=350,y=270)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=farmer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=insert_farmer_command)
    Button.place(x=400, y=400)

def insert_farmer_command():
    global root
    try:
        sql="INSERT INTO farmer values(%s,%s,%s,%s,%s,%s);"
        if len(e1.get())>3:
            invalid('farmer')
        else:

            vals=e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),e6.get()
            cur.executemany(sql,[vals])
            db.commit()
            farmer()
    except:
        insert_farmer()
def invalid(page):
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    if page=='farmer':
        label=Label(root,text='Enter valid farmer_id',font=('Times new roman',30),bg='white')
        label.place(x=170,y=200)

        button=Button(root,text='Re-enter',font=('Times new roman',20),command=insert_farmer)
        button.place(x=300,y=400)
    elif page=='company':
        label=Label(root,text='Enter valid company_id',font=('Times new roman',30),bg='white')
        label.place(x=170,y=200)

        button=Button(root,text='Re-enter',font=('Times new roman',20),command=insert_company)
        button.place(x=300,y=400)
def delete_farmer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Farmer Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=farmer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=delete_farmer_command)
    Button.place(x=400, y=400)


def delete_farmer_command():
    try:
        sql="DELETE FROM farmer WHERE f_id=%s;"
        cur.execute(sql,[e1.get()])
        db.commit()
        farmer()
    except:
        l=Label(root,text='Invalid Entry',font=('times new roman',15))
        l.place(x=100,y=300)

def update_farmer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Farmer Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="OK", font=("Arial", 15),command=update)

    Button.place(x=300, y=400)

def update():
    try:
        global e1,e2,e3,e4,e5,e6
        #clean
        label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
        label.place(x=0,y=0)

        sql='SELECT * FROM farmer WHERE f_id=%s;'
        vals=[e1.get()]
        cur.execute(sql,vals)

        label=Label(root,text='Farmer_id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=10)

        label=Label(root,text='Farmer_name',font=('Times new roman',20),bg='white')
        label.place(x=50,y=60)

        label=Label(root,text='Farmer_phone',font=('Times new roman',20),bg='white')
        label.place(x=50,y=110)

        label=Label(root,text='Farmer_mail',font=('Times new roman',20),bg='white')
        label.place(x=50,y=160)

        label=Label(root,text='Farmer_locality',font=('Times new roman',20),bg='white')
        label.place(x=50,y=210)

        label=Label(root,text='Farmer_address',font=('Times new roman',20),bg='white')
        label.place(x=50,y=270)

        e1=Entry(root)
        e2=Entry(root)
        e3=Entry(root)
        e4=Entry(root)
        e5=Entry(root)
        e6=Entry(root)

        data=cur.fetchall()
        arr=[e1,e2,e3,e4,e5,e6]
        count=0
        for val in data[0]:
            arr[count].insert(0,val)
            count+=1

        e1.place(x=350,y=10)
        e2.place(x=350,y=60)
        e3.place(x=350,y=110)
        e4.place(x=350,y=160)
        e5.place(x=350,y=210)
        e6.place(x=350,y=270)

        label=Button(root,text='Modify',font=('Times new roman',20),bg='blue',command=update_command)
        label.place(x=300,y=400)


    except:
        l=Label(root,text='Invalid Farmer_id',font=('times new roman',15))
        l.place(x=100,y=300)
        update_farmer()

def update_command():
    try:
        sql="UPDATE farmer SET f_name=%s,f_phone_no=%s,f_mail=%s,f_locality=%s,f_address=%s WHERE f_id=%s;"
        vals=e2.get(),e3.get(),e4.get(),e5.get(),e6.get(),e1.get()
        cur.executemany(sql,[vals])
        db.commit()
        farmer()
    except:
        update_farmer()
def search_farmer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Farmer Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=farmer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search)
    Button.place(x=400, y=400)
def search():
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)
    try:
        sql='SELECT * FROM farmer WHERE f_id=%s;'
        val=[e1.get()]
        cur.execute(sql,val)

        Button = tk.Button(root, text="OK", font=("Arial", 15),command=farmer)
        Button.place(x=300, y=400)

        for val in cur:
            count=0
            Y=50
            names=['farmer id: ','farmer name: ','farmer phone: ','farmer mail: ','farmer locality: ','farmer address: ']
            for i in val:
                label=Label(root,text=names[count]+str(i),font=('Times new roman',20),bg='tomato')
                label.place(x=10,y=Y)
                Y+=50
                count+=1
        db.commit()
    except:
        l=Label(root,text='Invalid Farmer Id',font=('times new roman',15))
        l.place(x=100,y=300)
        search_farmer()


#company page
def company():
    global root
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Company Table',font=('Times new roman',15),bg='white')
    label.place(x=350,y=10)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=entity_page)
    Button.place(x=10, y=50)

    Button = tk.Button(root, text="Insert", font=("Arial", 15),command=insert_company)
    Button.place(x=110, y=50)

    Button = tk.Button(root, text="Delete", font=("Arial", 15),command=delete_company)
    Button.place(x=210, y=50)

    Button = tk.Button(root, text="Update", font=("Arial", 15),command=update_company)
    Button.place(x=310, y=50)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_company)
    Button.place(x=410, y=50)

    view_company()


def view_company():
    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("c_id",'c_name','c_address'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('c_id',text="Company Id")
    table.heading('c_name',text="Company Name")
    table.heading('c_address',text="Company Address")
    table['show']='headings'

    table.column("c_id",width=100)


    table.pack()



    cur.execute("SELECT * FROM company;")

    data =cur.fetchall()
    db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

def insert_company():
    global e1,e2,e3,e4,e5,e6
    #clean the window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    #create the window
    label=Label(root,text='Company_id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=10)

    label=Label(root,text='Company_name',font=('Times new roman',20),bg='white')
    label.place(x=50,y=110)

    label=Label(root,text='Company_address',font=('Times new roman',20),bg='white')
    label.place(x=50,y=210)

    e1=Entry(root,width=50)
    e2=Entry(root,width=50)
    e3=Entry(root,width=50)

    e1.place(x=350,y=10)
    e2.place(x=350,y=110)
    e3.place(x=350,y=210)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=company)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=insert_company_command)
    Button.place(x=400, y=400)

def insert_company_command():
    try:
        if len(e1.get())>3:
            invalid("company")
        else:
            sql="INSERT INTO company values(%s,%s,%s);"
            vals=e1.get(),e2.get(),e3.get()
            cur.executemany(sql,[vals])
            db.commit()
            company()
    except:
        insert_company()
def delete_company():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Company Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=company)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=delete_company_command)
    Button.place(x=400, y=400)


def delete_company_command():
    try:
        sql="DELETE FROM company WHERE c_id=%s;"
        cur.execute(sql,[int(e1.get())])
        db.commit()
        company()
    except:
        l=Label(root,text='Invalid Entry',font=('times new roman',15))
        l.place(x=100,y=300)

def update_company():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Company Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="OK", font=("Arial", 15),command=update_c)

    Button.place(x=300, y=400)

def update_c():
    try:
        global e1,e2,e3,e4,e5,e6
        #clean
        label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
        label.place(x=0,y=0)

        sql='SELECT * FROM company WHERE c_id=%s;'
        vals=[e1.get()]
        cur.execute(sql,vals)

        label=Label(root,text='Company_id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=10)

        label=Label(root,text='Company_name',font=('Times new roman',20),bg='white')
        label.place(x=50,y=110)

        label=Label(root,text='Company_address',font=('Times new roman',20),bg='white')
        label.place(x=50,y=210)

        e1=Entry(root)
        e2=Entry(root)
        e3=Entry(root)

        data=cur.fetchall()
        arr=[e1,e2,e3]
        count=0
        for val in data[0]:
            arr[count].insert(0,val)
            count+=1

        e1.place(x=350,y=10)
        e2.place(x=350,y=110)
        e3.place(x=350,y=210)

        label=Button(root,text='Modify',font=('Times new roman',20),bg='blue',command=update_command_c)
        label.place(x=300,y=400)


    except:
        l=Label(root,text='Invalid Farmer_id',font=('times new roman',15))
        l.place(x=100,y=300)
        update_company()

def update_command_c():
    try:
        sql="UPDATE company SET c_name=%s,c_address=%s WHERE c_id=%s;"
        vals=e2.get(),e3.get(),e1.get()
        cur.executemany(sql,[vals])
        db.commit()
        company()
    except:
        update_company()
def search_company():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Company Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=company)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_c)
    Button.place(x=400, y=400)
def search_c():
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)
    try:
        sql='SELECT * FROM company WHERE c_id=%s;'
        val=[e1.get()]
        cur.execute(sql,val)

        Button = tk.Button(root, text="OK", font=("Arial", 15),command=company)
        Button.place(x=300, y=400)

        for val in cur:
            count=0
            Y=50
            names=['company id: ','company name: ','company address: ']
            for i in val:
                label=Label(root,text=names[count]+str(i),font=('Times new roman',20),bg='tomato')
                label.place(x=10,y=Y)
                Y+=50
                count+=1
        db.commit()
    except:
        l=Label(root,text='Invalid Company Id',font=('times new roman',15))
        l.place(x=100,y=300)
        search_company()



#fertilizer page
def fertilizer():
    global root
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Fertilizer Table',font=('Times new roman',15),bg='white')
    label.place(x=350,y=10)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=entity_page)
    Button.place(x=10, y=50)

    Button = tk.Button(root, text="Insert", font=("Arial", 15),command=insert_fer)
    Button.place(x=110, y=50)

    Button = tk.Button(root, text="Delete", font=("Arial", 15),command=delete_fer)
    Button.place(x=210, y=50)

    Button = tk.Button(root, text="Update", font=("Arial", 15),command=update_fer)
    Button.place(x=310, y=50)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_fer)
    Button.place(x=410, y=50)

    view_fer()


def view_fer():
    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("fe_formula",'fe_name','fe_content','fe_price','company_id'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('fe_formula',text="Fertilizer Formula")
    table.heading('fe_name',text="Fertilizer name")
    table.heading('fe_content',text="Fertilizer content")
    table.heading('fe_price',text="Fertilizer price")
    table.heading('company_id',text="Company_id")
    #table.heading('f_address',text="Farmer Address")
    table['show']='headings'

    #table.column("f_id",width=100)


    table.pack()



    cur.execute("SELECT * FROM fertilizer;")

    data =cur.fetchall()
    db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

e1,e2,e3,e4,e5,e6=0,0,0,0,0,0
def insert_fer():
    global e1,e2,e3,e4,e5,e6
    #clean the window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    #create the window
    label=Label(root,text='Fertlizer formula',font=('Times new roman',20),bg='white')
    label.place(x=50,y=10)

    label=Label(root,text='Fertlizer name',font=('Times new roman',20),bg='white')
    label.place(x=50,y=60)

    label=Label(root,text='Fertilizer content',font=('Times new roman',20),bg='white')
    label.place(x=50,y=110)

    label=Label(root,text='Fertlizer price',font=('Times new roman',20),bg='white')
    label.place(x=50,y=160)

    label=Label(root,text='Company id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=210)


    e1=Entry(root,width=50)
    e2=Entry(root,width=50)
    e3=Entry(root,width=50)
    e4=Entry(root,width=50)
    e5=Entry(root,width=50)
    #e6=Entry(root,width=50)

    e1.place(x=350,y=10)
    e2.place(x=350,y=60)
    e3.place(x=350,y=110)
    e4.place(x=350,y=160)
    e5.place(x=350,y=210)
    #e6.place(x=350,y=270)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=fertilizer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=insert_fer_command)
    Button.place(x=400, y=400)

def insert_fer_command():
    try:
        sql="INSERT INTO fertilizer values(%s,%s,%s,%s,%s);"
        vals=e1.get(),e2.get(),e3.get(),e4.get(),e5.get()
        cur.executemany(sql,[vals])
        db.commit()
        fertilizer()
    except:
        insert_fer()
def delete_fer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Fertilizer formula:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=fertilizer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=delete_fer_command)
    Button.place(x=400, y=400)


def delete_fer_command():
    try:
        sql="DELETE FROM fertilizer WHERE fe_formula=%s;"
        cur.execute(sql,[e1.get()])
        db.commit()
        fertilizer()
    except:
        l=Label(root,text='Invalid Entry',font=('times new roman',15))
        l.place(x=100,y=300)

def update_fer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Fertlizer formula:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="OK", font=("Arial", 15),command=update_fe)

    Button.place(x=300, y=400)

def update_fe():
    try:
        global e1,e2,e3,e4,e5,e6
        #clean
        label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
        label.place(x=0,y=0)

        sql='SELECT * FROM fertilizer WHERE fe_formula=%s;'
        vals=[e1.get()]
        cur.execute(sql,vals)

        label=Label(root,text='Fertlizer formula',font=('Times new roman',20),bg='white')
        label.place(x=50,y=10)

        label=Label(root,text='Fertlizer name',font=('Times new roman',20),bg='white')
        label.place(x=50,y=60)

        label=Label(root,text='Fertlizer content',font=('Times new roman',20),bg='white')
        label.place(x=50,y=110)

        label=Label(root,text='Fertlizer price',font=('Times new roman',20),bg='white')
        label.place(x=50,y=160)

        label=Label(root,text='comapny_id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=210)


        e1=Entry(root)
        e2=Entry(root)
        e3=Entry(root)
        e4=Entry(root)
        e5=Entry(root)
        #e6=Entry(root)

        data=cur.fetchall()
        arr=[e1,e2,e3,e4,e5,e6]
        count=0
        for val in data[0]:
            arr[count].insert(0,val)
            count+=1

        e1.place(x=350,y=10)
        e2.place(x=350,y=60)
        e3.place(x=350,y=110)
        e4.place(x=350,y=160)
        e5.place(x=350,y=210)
        #e6.place(x=350,y=270)

        label=Button(root,text='Modify',font=('Times new roman',20),bg='blue',command=update_command_fe)
        label.place(x=300,y=400)


    except:
        l=Label(root,text='Invalid Farmer_id',font=('times new roman',15))
        l.place(x=100,y=300)
        update_fer()

def update_command_fe():

    sql="UPDATE fertilizer SET fe_name=%s,fe_content=%s,fe_price=%s,company_id=%s WHERE fe_formula=%s;"
    vals=e2.get(),e3.get(),e4.get(),e5.get(),e1.get()
    cur.executemany(sql,[vals])
    db.commit()
    fertilizer()

def search_fer():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Fertlizer formula:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=fertilizer)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_fe)
    Button.place(x=400, y=400)
def search_fe():
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)
    try:
        sql='SELECT * FROM fertilizer WHERE fe_formula=%s;'
        val=[e1.get()]
        cur.execute(sql,val)

        Button = tk.Button(root, text="OK", font=("Arial", 15),command=fertilizer)
        Button.place(x=300, y=400)

        for val in cur:
            count=0
            Y=50
            names=['fertilizer formula: ','fertilizer name: ','fertilizer content: ','fertilizer price: ','company_id: ']
            for i in val:
                label=Label(root,text=names[count]+str(i),font=('Times new roman',20),bg='tomato')
                label.place(x=10,y=Y)
                Y+=50
                count+=1
        db.commit()
    except:
        l=Label(root,text='Invalid Fertilizer formula',font=('times new roman',15))
        l.place(x=100,y=300)
        search_fer()



#order page
def orders():
    global root
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Orders Table',font=('Times new roman',15),bg='white')
    label.place(x=350,y=10)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=entity_page)
    Button.place(x=10, y=50)

    Button = tk.Button(root, text="Insert", font=("Arial", 15),command=insert_ord)
    Button.place(x=110, y=50)

    Button = tk.Button(root, text="Delete", font=("Arial", 15),command=delete_ord)
    Button.place(x=210, y=50)

    Button = tk.Button(root, text="Update", font=("Arial", 15),command=update_ord)
    Button.place(x=310, y=50)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_ord)
    Button.place(x=410, y=50)

    view_ord()


def view_ord():
    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("or_id",'or_date','or_fid','or_formula','or_to'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('or_id',text="Order Id")
    table.heading('or_date',text="Order Date")


    table.heading('or_fid',text="Ordered Farmer Id")
    table.heading('or_formula',text="Order (item)formula")
    table.heading('or_to',text="Order to")
    #table.heading('f_address',text="Farmer Address")
    table['show']='headings'

    #table.column("f_id",width=100)


    table.pack()



    cur.execute("SELECT * FROM orders;")

    data =cur.fetchall()
    db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

e1,e2,e3,e4,e5,e6=0,0,0,0,0,0
def insert_ord():
    global e1,e2,e3,e4,e5,e6
    #clean the window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    #create the window
    label=Label(root,text='Order Id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=10)

    label=Label(root,text='Order date',font=('Times new roman',20),bg='white')
    label.place(x=50,y=60)

    label=Label(root,text='Order FID',font=('Times new roman',20),bg='white')
    label.place(x=50,y=110)

    label=Label(root,text='Order formula',font=('Times new roman',20),bg='white')
    label.place(x=50,y=160)

    label=Label(root,text='Order to',font=('Times new roman',20),bg='white')
    label.place(x=50,y=210)


    e1=Entry(root,width=50)
    e2=Entry(root,width=50)
    e3=Entry(root,width=50)
    e4=Entry(root,width=50)
    e5=Entry(root,width=50)
    #e6=Entry(root,width=50)

    e1.place(x=350,y=10)
    e2.place(x=350,y=60)
    e2.insert(0,datetime.now())
    e3.place(x=350,y=110)
    e4.place(x=350,y=160)
    e5.place(x=350,y=210)
    #e6.place(x=350,y=270)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=orders)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=insert_ord_command)
    Button.place(x=400, y=400)

def insert_ord_command():
    try:
        sql="INSERT INTO orders values(%s,%s,%s,%s,%s);"
        vals=e1.get(),e2.get(),e3.get(),e4.get(),e5.get()
        cur.executemany(sql,[vals])
        db.commit()
        orders()
    except:
        insert_ord()
def delete_ord():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Order Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=orders)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=delete_ord_command)
    Button.place(x=400, y=400)


def delete_ord_command():
    try:
        sql="DELETE FROM orders WHERE or_id=%s;"
        cur.execute(sql,[e1.get()])
        db.commit()
        orders()
    except:
        l=Label(root,text='Invalid Entry',font=('times new roman',15))
        l.place(x=100,y=300)

def update_ord():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Order Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="OK", font=("Arial", 15),command=update_or)

    Button.place(x=300, y=400)

def update_or():
    try:
        global e1,e2,e3,e4,e5,e6
        #clean
        label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
        label.place(x=0,y=0)

        sql='SELECT * FROM orders WHERE or_id=%s;'
        vals=[e1.get()]
        cur.execute(sql,vals)

        label=Label(root,text='Order Id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=10)

        label=Label(root,text='Order Date',font=('Times new roman',20),bg='white')
        label.place(x=50,y=60)

        label=Label(root,text='Order f_id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=110)

        label=Label(root,text='Order formula',font=('Times new roman',20),bg='white')
        label.place(x=50,y=160)

        label=Label(root,text='Order to',font=('Times new roman',20),bg='white')
        label.place(x=50,y=210)


        e1=Entry(root)
        e2=Entry(root)
        e3=Entry(root)
        e4=Entry(root)
        e5=Entry(root)
        #e6=Entry(root)

        data=cur.fetchall()
        arr=[e1,e2,e3,e4,e5,e6]
        count=0
        for val in data[0]:
            arr[count].insert(0,val)
            count+=1

        e1.place(x=350,y=10)
        e2.place(x=350,y=60)
        #e2.insert(0,datetime.now())
        e3.place(x=350,y=110)
        e4.place(x=350,y=160)
        e5.place(x=350,y=210)
        #e6.place(x=350,y=270)

        label=Button(root,text='Modify',font=('Times new roman',20),bg='blue',command=update_command_ord)
        label.place(x=300,y=400)


    except:
        l=Label(root,text='Invalid Order_id',font=('times new roman',15))
        l.place(x=100,y=300)
        update_ord()

def update_command_ord():

    sql="UPDATE orders SET or_date=%s,or_fid=%s,or_formula=%s,or_to=%s WHERE or_id=%s;"
    vals=e2.get(),e3.get(),e4.get(),e5.get(),e1.get()
    cur.executemany(sql,[vals])
    db.commit()
    orders()

def search_ord():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Order Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=orders)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_or)
    Button.place(x=400, y=400)
def search_or():
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)
    try:
        sql='SELECT * FROM orders WHERE or_id=%s;'
        val=[e1.get()]
        cur.execute(sql,val)

        Button = tk.Button(root, text="OK", font=("Arial", 15),command=orders)
        Button.place(x=300, y=400)

        for val in cur:
            count=0
            Y=50
            names=['order Id: ','Order date: ','Order fid: ','Order formula: ','order to: ']
            for i in val:
                label=Label(root,text=names[count]+str(i),font=('Times new roman',20),bg='tomato')
                label.place(x=10,y=Y)
                Y+=50
                count+=1
        db.commit()
    except:
        l=Label(root,text='Invalid order id',font=('times new roman',15))
        l.place(x=100,y=300)
        search_ord()




#payment page
def payment():
    global root
    #clean previous window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Payment Table',font=('Times new roman',15),bg='white')
    label.place(x=350,y=10)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=entity_page)
    Button.place(x=10, y=50)

    Button = tk.Button(root, text="Insert", font=("Arial", 15),command=insert_pay)
    Button.place(x=110, y=50)

    Button = tk.Button(root, text="Delete", font=("Arial", 15),command=delete_pay)
    Button.place(x=210, y=50)

    Button = tk.Button(root, text="Update", font=("Arial", 15),command=update_pay)
    Button.place(x=310, y=50)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_pay)
    Button.place(x=410, y=50)

    view_pay()


def view_pay():
    frame=Frame(root,bd=5,relief=RIDGE,bg='tomato')
    frame.place(x=10,y=100,width=750,height=400)

    x_scroll=Scrollbar(frame,orient=HORIZONTAL)
    y_scroll=Scrollbar(frame,orient=VERTICAL)

    table=ttk.Treeview(frame,columns=("trans_id",'p_f_id','p_date','p_amount','p_method'),xscrollcommand=x_scroll.set,
    yscrollcommand=y_scroll.set)

    x_scroll.pack(side=BOTTOM,fill=X)
    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)
    table.heading('trans_id',text="Transaction Id")
    table.heading('p_f_id',text="Farmer Id")


    table.heading('p_date',text="Payment Date")
    table.heading('p_amount',text="Amount")
    table.heading('p_method',text="Payment Method")
    #table.heading('f_address',text="Farmer Address")
    table['show']='headings'

    #table.column("f_id",width=100)


    table.pack()



    cur.execute("SELECT * FROM payment;")

    data =cur.fetchall()
    db.commit()
    if len(data)!=0:
        for row in data:
            table.insert('',END,values=row)

e1,e2,e3,e4,e5,e6=0,0,0,0,0,0
def insert_pay():
    global e1,e2,e3,e4,e5,e6
    #clean the window
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)


    #create the window
    label=Label(root,text='Transaction Id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=10)

    label=Label(root,text='Transaction farmer id',font=('Times new roman',20),bg='white')
    label.place(x=50,y=60)

    label=Label(root,text='Transaction date',font=('Times new roman',20),bg='white')
    label.place(x=50,y=110)

    label=Label(root,text='Transaction amount',font=('Times new roman',20),bg='white')
    label.place(x=50,y=160)

    label=Label(root,text='Transaction method',font=('Times new roman',20),bg='white')
    label.place(x=50,y=210)


    e1=Entry(root,width=50)
    e2=Entry(root,width=50)
    e3=Entry(root,width=50)

    e4=Entry(root,width=50)
    e5=Entry(root,width=50)
    #e6=Entry(root,width=50)

    e1.place(x=350,y=10)
    e2.place(x=350,y=60)
    #e2.insert(0,datetime.now())

    e3.place(x=350,y=110)
    e3.insert(0,datetime.now())
    e4.place(x=350,y=160)
    #e5.place(x=350,y=210)
    e5 = StringVar(root)
    e5.set("Debit card") # default value

    w= OptionMenu(root, e5, "Credit Card", "UPI", "Cheque","Cash")
    w.place(x=350,y=210)

#mainloop()

    #e6.place(x=350,y=270)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=payment)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=insert_pay_command)
    Button.place(x=400, y=400)

def insert_pay_command():
    try:
        sql="INSERT INTO payment values(%s,%s,%s,%s,%s);"
        vals=e1.get(),e2.get(),e3.get(),e4.get(),e5.get()
        cur.executemany(sql,[vals])
        db.commit()
        payment()
    except:
        insert_pay()
def delete_pay():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Transaction Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=payment)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Commit", font=("Arial", 15),command=delete_pay_command)
    Button.place(x=400, y=400)


def delete_pay_command():
    try:
        sql="DELETE FROM payment WHERE trans_id=%s;"
        cur.execute(sql,[e1.get()])
        db.commit()
        payment()
    except:
        l=Label(root,text='Invalid Entry',font=('times new roman',15))
        l.place(x=100,y=300)

def update_pay():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window
    label=Label(root,text='Transaction Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="OK", font=("Arial", 15),command=update_pa)

    Button.place(x=300, y=400)

def update_pa():
    try:
        global e1,e2,e3,e4,e5,e6
        #clean
        label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
        label.place(x=0,y=0)

        sql='SELECT * FROM payment WHERE trans_id=%s;'
        vals=[e1.get()]
        cur.execute(sql,vals)

        label=Label(root,text='Transaction Id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=10)

        label=Label(root,text='Farmer_id',font=('Times new roman',20),bg='white')
        label.place(x=50,y=60)

        label=Label(root,text='Transaction date',font=('Times new roman',20),bg='white')
        label.place(x=50,y=110)

        label=Label(root,text='Transaction amount',font=('Times new roman',20),bg='white')
        label.place(x=50,y=160)

        label=Label(root,text='Transaction method',font=('Times new roman',20),bg='white')
        label.place(x=50,y=210)


        e1=Entry(root)
        e2=Entry(root)
        e3=Entry(root)
        e4=Entry(root)
        e5=Entry(root)
        #e6=Entry(root)

        data=cur.fetchall()
        arr=[e1,e2,e3,e4,e5,e6]
        count=0
        for val in data[0]:
            if count==5:
                continue
            arr[count].insert(0,val)
            count+=1

        e1.place(x=350,y=10)
        e2.place(x=350,y=60)

        e3.place(x=350,y=110)
        #e3.insert(0,datetime.now())
        e4.place(x=350,y=160)
        #e5.place(x=350,y=210)
        #e6.place(x=350,y=270)
        e5 = StringVar(root)
        e5.set("Debit card") # default value

        w= OptionMenu(root, e5, "Credit Card", "UPI", "Cheque","Cash")
        w.place(x=350,y=210)

        label=Button(root,text='Modify',font=('Times new roman',20),bg='blue',command=update_command_pay)
        label.place(x=300,y=400)


    except:
        l=Label(root,text='Invalid Order_id',font=('times new roman',15))
        l.place(x=100,y=300)
        update_pay()

def update_command_pay():

    sql="UPDATE payment SET p_f_id=%s,p_date=%s,p_amount=%s,p_method=%s WHERE trans_id=%s;"
    vals=e2.get(),e3.get(),e4.get(),e5.get(),e1.get()
    cur.executemany(sql,[vals])
    db.commit()
    payment()
def search_pay():
    global e1
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)

    #window2
    label=Label(root,text='Transaction Id:',font=('Times new roman',20),bg='tomato')
    label.place(x=100,y=200)

    e1=Entry(root,width=50)
    e1.place(x=300,y=200)

    Button = tk.Button(root, text="Back", font=("Arial", 15),command=payment)
    Button.place(x=200, y=400)

    Button = tk.Button(root, text="Search", font=("Arial", 15),command=search_pa)
    Button.place(x=400, y=400)
def search_pa():
    #clean
    label=Label(root,text=' '*800,font=('Times new roman',500),bg='tomato')
    label.place(x=0,y=0)
    try:
        sql='SELECT * FROM payment WHERE trans_id=%s;'
        val=[e1.get()]
        cur.execute(sql,val)

        Button = tk.Button(root, text="OK", font=("Arial", 15),command=payment)
        Button.place(x=300, y=400)

        for val in cur:
            count=0
            Y=50
            names=['Transaction Id: ','Transaction fid: ','Transaction date: ','Transaction amount: ','Transaction method: ']
            for i in val:
                label=Label(root,text=names[count]+str(i),font=('Times new roman',20),bg='tomato')
                label.place(x=10,y=Y)
                Y+=50
                count+=1
        db.commit()
    except:
        l=Label(root,text='Invalid order id',font=('times new roman',15))
        l.place(x=100,y=300)
        search_pay()


First_page(root)
root.mainloop()
