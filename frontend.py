"""

Program to manually log data from City Heat usage,
calculate average use per day between logdates
and show in graph
Log_data = Datum
Heat is usage GJ
Flow is usage in m3
Tkinter frontend

"""

from tkinter import *
import backend

def get_selected_row(event):
    try:
        global selected_tuple
        index=list1.curselection()[0]
        selected_tuple=list1.get(index)
        e1.delete(0,END)
        e1.insert(END,selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END,selected_tuple[3])
        # e4.delete(0,END)
        # e4.insert(END,selected_tuple[4])
    except IndexError:
        pass

def view_command():
    list1.delete(0,END)
    for row in backend.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in backend.search(Log_date.get(),Heat.get(),Flow.get(),Toelichting.get()):
        list1.insert(END,row)

def add_command():
    backend.insert(Log_date.get(),Heat.get(),Flow.get(),Toelichting.get())
    list1.delete(0,END)
    list1.insert(END,(Log_date.get(),Heat.get(),Flow.get(),Toelichting.get()))

def delete_command():
    backend.delete(selected_tuple[0])

def update_command():
    backend.update(selected_tuple[0],Log_date.get(),Heat.get(),Flow.get(),Toelichting.get())

def calc_command():
    list1.delete(0,END)
    backend.averagecalculation()
    for row in backend.view():
        list1.insert(END,row)
    # for row in backend.averagecalculation():
    #     list1.insert(END,row)

def graph_command():
    backend.graph_data()


window=Tk()
window.wm_title("My HeatLogger")

l1=Label(window,text="Log Date (yyyy-mm-dd)")
l1.grid(row=0,column=0)
l2=Label(window,text="Heat")
l2.grid(row=1,column=0)
l3=Label(window,text="Flow")
l3.grid(row=2,column=0)
l4=Label(window,text="Toelichting")
l4.grid(row=3,column=0)

Log_date=StringVar()
e1=Entry(window,textvariable=Log_date)
e1.grid(row=0,column=1)

Heat=StringVar()
e2=Entry(window,textvariable=Heat)
e2.grid(row=1,column=1)

Flow=StringVar()
e3=Entry(window,textvariable=Flow)
e3.grid(row=2,column=1)

Toelichting=StringVar()
e4=Entry(window,textvariable=Toelichting)
e4.grid(row=3,column=1)

list1=Listbox(window, height=30,width=100)
list1.grid(row=4,column=0,rowspan=6,columnspan=2)

sb1=Scrollbar(window)
sb1.grid(row=5,column=2,rowspan=4, sticky=NS)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>',get_selected_row)

b1=Button(window,text="View All", width=12,command=view_command)
b1.grid(row=4,column=3)

b2=Button(window,text="Search", width=12,command=search_command)
b2.grid(row=5,column=3)

b3=Button(window,text="Add", width=12,command=add_command)
b3.grid(row=6,column=3)

b4=Button(window,text="Update", width=12,command=update_command)
b4.grid(row=7,column=3)

b5=Button(window,text="Delete", width=12,command=delete_command)
b5.grid(row=8,column=3)

b6=Button(window,text="Close", width=12,command=window.destroy)
b6.grid(row=9,column=3)

b7=Button(window,text="Calc", width=12,command=calc_command)
b7.grid(row=10,column=3)

b8=Button(window,text="Graph", width=12,command=graph_command)
b8.grid(row=11,column=3)

window.mainloop()
