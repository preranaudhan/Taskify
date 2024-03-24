# importing the required modules  
import tkinter as tk                    # importing the tkinter module as tk  
from tkinter import ttk                 # importing the ttk module from the tkinter library  
from tkinter import messagebox          # importing the messagebox module from the tkinter library  
import sqlite3 as sql                   # importing the sqlite3 module as sql  
import  pickle
from datetime import datetime

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Declare task_field and due_date_field as global variables
task_field = None
due_date_field = None

# defining the function to add tasks to the list
def add_task():
    global task_field, due_date_field  # Declare that we're using the global variables

    task_string = task_field.get()
    due_date = due_date_field.get()

    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Task Field is Empty.')
    elif not is_valid_date(due_date):
        messagebox.showinfo('Error', 'Invalid Due Date Format or Date is not valid.')
    else:
        task_listbox.insert('end', f"{task_string} (Due: {due_date})")
        the_cursor.execute('insert into tasks (title, due_date) values (?, ?)', (task_string, due_date))
        the_connection.commit()

# defining the function to delete a task from the list  
def delete_task():
    selected_index = task_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        task_listbox.delete(index)
        task_title = task_listbox.get(index).split(" (Due:")[0]
        the_cursor.execute('delete from tasks where title = ?', (task_title,))
        the_connection.commit()
    else:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')
        
# Mark to compeleted task
def markcompleted():
    marked= task_listbox.curselection()
    temp=marked[0]
    #store the text of selected item in a string
    temp_marked=task_listbox.get(marked)
    #update it
    temp_marked=temp_marked+" ✔ "
    # deleted in the insert it 
    task_listbox.delete(temp)
    task_listbox.insert(temp,temp_marked)
    
# Mark to not completed Work
def marknotcompleted():
        notmarked= task_listbox.curselection()
        temp1=notmarked[0]
        #store the text of selected item in a string
        temp_notmarked=task_listbox.get(notmarked)
        #update it
        temp_notmarked=temp_notmarked+" ❌"
        # deleted in the insert it 
        task_listbox.delete(temp1)
        task_listbox.insert(temp1,temp_notmarked)

# Define the save_tasks function
def save_tasks():
    tasks = task_listbox.get(0, task_listbox.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))

# Define the load_tasks function
def load_tasks():
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        task_listbox.delete(0, tk.END)
        for task in tasks:
            task_listbox.insert(tk.END, task)
    except:
        messagebox.showwarning(title="Warning!", message="Cannot find tasks.dat.")
  
# function to close the application  
def close():   
    # using the destroy() method to close the application  
    guiWindow.destroy()  
  
# function to retrieve data from the database  
def retrieve_database():  
    # using the while loop to iterate through the elements in the tasks list  
    while(len(tasks) != 0):  
        # using the pop() method to pop out the elements from the list  
        tasks.pop()  
    # iterating through the rows in the database table  
    for row in the_cursor.execute('select title from tasks'):  
        # using the append() method to insert the titles from the table in the list  
        tasks.append(row[0])  
  
# main function  
if __name__ == "__main__":  
    # creating an object of the Tk() class  
    guiWindow = tk.Tk()  
    # setting the title of the window  
    guiWindow.title("TASKIFY")  
    # setting the geometry of the window  
    guiWindow.geometry("500x500+750+100")  
    # disabling the resizable option  
    guiWindow.resizable(0, 0)  
  
    # using the connect() method to connect to the database  
    the_connection = sql.connect('listOfTasks.db')  
    # creating the cursor object of the cursor class  
    the_cursor = the_connection.cursor()  
    # using the execute() method to execute a SQL statement  
    the_cursor.execute('create table if not exists tasks (title text)')  
  
    # defining an empty list  
    tasks = []  
      
    # defining frames using the tk.Frame() widget  
    header_frame = tk.Frame(guiWindow, bg = "#FF9898")  
    functions_frame = tk.Frame(guiWindow, bg = "#FF9898")  
    listbox_frame = tk.Frame(guiWindow, bg = "#FF9898")  
  
    # using the pack() method to place the frames in the application  
    header_frame.pack(fill = "both")  
    functions_frame.pack(side = "left", expand = True, fill = "both")  
    listbox_frame.pack(side = "right", expand = True, fill = "both")  
      
    # defining a label using the ttk.Label() widget  
    header_label = ttk.Label(  
        header_frame,  
        text = "TASKIFY",  
        font = ("Brush Script MT", "30"),  
        background = "#000000",  
        foreground = "#FFFFFF"  
    )  
    # using the pack() method to place the label in the application  
    header_label.pack(padx = 20, pady = 20)  
  
    # defining another label using the ttk.Label() widget  
    task_label = ttk.Label(  
        functions_frame,  
        text = "   Enter the Task:  ",  
        font = ("Consolas", "14"),  
        background = "#000000",  
        foreground = "#FFFFFF"  
    )  
    # using the place() method to place the label in the application  
    task_label.place(x = 30, y = 35)  
    
    due_date_label = ttk.Label(
        functions_frame,
        text="Due Date(DD/MM/YYYY):",
        font=("Consolas", "13"),
        background="#000000",
        foreground="#FFFFFF"
    )
    due_date_label.place(x=30, y=100)
    
    # defining an entry field using the ttk.Entry() widget  
    task_field = ttk.Entry(  
        functions_frame,  
        font = ("Consolas", "15"),  
        width = 18,  
        background = "#FFFFFF",  
        foreground = "#000000"  
    )  
    # using the place() method to place the entry field in the application  
    task_field.place(x = 30, y = 60) 
    
    due_date_field = ttk.Entry(
      functions_frame,
      font=("Consolas", "15"),
      width=17,
      background="#FFFFFF",
      foreground="#000000"
    )
    due_date_field.place(x=30, y=120)
  
    # adding buttons to the application using the ttk.Button() widget  
    add_button = ttk.Button(  
        functions_frame,  
        text = "Add Task",  
        width = 24,  
        command = add_task  
    )  
    markcompleted_button=ttk.Button(
        
        functions_frame,  
        text = " Mark Completed",  
        width = 24,  
        command = markcompleted
        )
    
    del_button = ttk.Button(  
        functions_frame,  
        text = "Delete Task",  
        width = 24,  
        command = delete_task  
    ) 
    marknotcompleted_button=ttk.Button(
        
        functions_frame,  
        text = " Mark Not Completed",  
        width = 24,  
        command = marknotcompleted
        )
    save_button = ttk.Button(
    functions_frame,
    text="Save Tasks",
    width=24,
    command=save_tasks
    )

    load_button = ttk.Button(
    functions_frame,
    text="Load Tasks",
    width=24,
    command=load_tasks
    )

    exit_button = ttk.Button(  
        functions_frame,  
        text = "Exit",  
        width = 24,  
        command = close  
    )  
    # using the place() method to set the position of the buttons in the application  
    add_button.place(x = 35, y = 160)
    markcompleted_button.place(x=35,y=180)
    del_button.place(x = 35, y = 200)
    marknotcompleted_button.place(x=35,y=220)
    save_button.place(x=35,y=240)
    load_button.place(x=35,y=260)
    exit_button.place(x = 35, y = 280)  
  
    # defining a list box using the tk.Listbox() widget  
    task_listbox = tk.Listbox(  
        listbox_frame,  
        width = 30,  
        height = 20,  
        selectmode = 'SINGLE',  
        background = "#FFFFFF",  
        foreground = "#000000",  
        selectbackground = "#CD853F",  
        selectforeground = "#FFFFFF"  
    )  
    # using the place() method to place the list box in the application  
    task_listbox.place(x = 10, y = 20)  
  
    # calling some functions  
    retrieve_database()  
    # using the mainloop() method to run the application  
    guiWindow.mainloop()  
    # establishing the connection with database  
    the_connection.commit()  
    the_cursor.close()
