from tkinter import *
import tkinter.messagebox as messagebox
import mysql.connector as mysql
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


# Connect to MySQL database
db = mysql.connect(host="localhost", user="root", password="manager", database="studentregistration")
mycursor = db.cursor()

# Function to handle database operations
def execute_query(query, params=None):
    try:
        if params:
            mycursor.execute(query, params)
        else:
            mycursor.execute(query)
        db.commit()
        return True
    except mysql.Error as e:
        print(f"MySQL Error: {str(e)}")
        db.rollback()
        return False

# Function to handle the Add button click
def add_student():
    if not logged_in:
        messagebox.showwarning("Warning", "Please login first.")
        return

    id = e1.get()
    name = e2.get()
    section = e3.get()

    if id and name and section:
        query = "INSERT INTO student (idnumber, name, section) VALUES (%s, %s, %s)"
        params = (id, name, section)
        if execute_query(query, params):
            messagebox.showinfo("Success", "Student added successfully!")
            clear_entries()
            show_students()
        else:
            messagebox.showerror("Error", "Failed to add student.")
    else:
        messagebox.showwarning("Warning", "Please enter all the fields.")

# Function to handle the Edit button click
# ...

# Function to handle the Edit button click
def edit_student():
    if not logged_in:
        messagebox.showwarning("Warning", "Please login first.")
        return

    selected_items = listbox.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select student(s) to edit.")
        return

    for selected_item in selected_items:
        student_data = listbox.item(selected_item)['values']
        id = student_data[0]
        name = e2.get()
        section = e3.get()

        if id:
            query = "UPDATE student SET name = %s, section = %s WHERE idnumber = %s"
            params = (name, section, id)
            if execute_query(query, params):
                messagebox.showinfo("Success", "Student updated successfully!")
                clear_entries()
                show_students()
            else:
                messagebox.showerror("Error", "Failed to update student.")
        else:
            messagebox.showwarning("Warning", "Please enter the ID number.")

# Function to handle the Delete button click
def delete_student():
    if not logged_in:
        messagebox.showwarning("Warning", "Please login first.")
        return

    selected_items = listbox.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select student(s) to delete.")
        return

    if messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected student(s)?"):
        for selected_item in selected_items:
            student_data = listbox.item(selected_item)['values']
            id = student_data[0]

            if id:
                query = "DELETE FROM student WHERE idnumber = %s"
                params = (id,)
                if execute_query(query, params):
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    clear_entries()
                    show_students()
                else:
                    messagebox.showerror("Error", "Failed to delete student.")
            else:
                messagebox.showwarning("Warning", "Please enter the ID number.")

# Function to show the list of students
def show_students():
    if not logged_in:
        messagebox.showwarning("Warning", "Please login first.")
        return

    query = "SELECT idnumber, name, section FROM student"
    mycursor.execute(query)
    records = mycursor.fetchall()
    

    # Clear existing data in the listbox
    listbox.delete(*listbox.get_children())

    # Populate the listbox with fetched records
    for record in records:
        listbox.insert("", "end", values=record)

# Function to clear the entry fields
def clear_entries():
    e1.delete(0, "end")
    e2.delete(0, "end")
    e3.delete(0, "end")

# Function to handle the Login button click
def login():
    global logged_in
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        logged_in = True
        messagebox.showinfo("Success", "Login successful!")
        # Hide the login window and show the student registration window
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

    clear_login_entries()

# Function to clear the login entry fields
def clear_login_entries():
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")

def search_students():
    search_query = search_entry.get()

    if not search_query:
        messagebox.showerror("Error", "Please enter a search query.")
        return

    listbox.delete(*listbox.get_children())  # Clear the listbox

    # Search and display matching students
    for student in student:
        if search_query.lower() in student[1].lower():
            listbox.insert("", "end", values=student)
        # Search Frame
        # Search Frame
        search_frame = Frame(main_frame, bg="#f1f1f1")
        search_frame.pack()

        search_label = Label(search_frame, text="Search:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        search_entry = Entry(search_frame, font=("Arial", 12), width=30)            
        search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        search_button = Button(search_frame, text="Search", command=search_students, image=search_icon, compound="left", bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
        search_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

# Function to handle the Logout button click
def logout():
    global logged_in
    logged_in = False
    main_frame.pack_forget()  # Hide the main frame
    login_frame.pack()  # Show the login frame

def show_section_distribution():
    if not logged_in:
        messagebox.showwarning("Warning", "Please login first.")
        return

    query = "SELECT section, COUNT(*) FROM student GROUP BY section"
    mycursor.execute(query)
    records = mycursor.fetchall()

    sections = []
    counts = []

    for record in records:
        sections.append(record[0])
        counts.append(record[1])

    # Create the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=sections, autopct='%1.1f%%')
    plt.title("Section Distribution")

    # Display the pie chart
    plt.show()
    



    clear_entries()  # Clear the search entry field

# Configuration options
window_title = "Student Registration"
window_width = 800
window_height = 500
icon_path = "C:/Users/Nikita thakur/OneDrive/Desktop/Studentregistration/student_registration_icon.png"
button_icons_path = {
    "add": "C:/Users/Nikita thakur/Desktop/Studentregistration/add.png",
    "edit": "C:/Users/Nikita thakur/Desktop/Studentregistration/edit.png",
    "delete": "C:/Users/Nikita thakur/Desktop/Studentregistration/delete.png",
    "show": "C:/Users/Nikita thakur/Desktop/Studentregistration/showlist.png"  
}
column_headings = ('ID Number', 'Name', 'Section')

# Create the main window
root = Tk()
root.geometry(f"{window_width}x{window_height}")
root.title(window_title)

# Load button icons
root.iconphoto(True, PhotoImage(file=icon_path).subsample(1))
button_icons = {
    name: PhotoImage(file=path).subsample(2)
    for name, path in button_icons_path.items()
}

# Load and resize the background image
background_image = Image.open("C:/Users/Nikita thakur/Desktop/Studentregistration/background_image1.jpg")
background_image = background_image.resize((window_width, window_height), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(background_image)

# Create a label with the background image and place it in the root window
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Styling
root.configure(bg="#f1f1f1")

# Login Frame
login_frame = Frame(root, bg="#f1f1f1")
login_frame.pack(pady=10)

Label(login_frame, text="Username:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1").grid(row=0, column=0, padx=10, pady=5, sticky="e")
Label(login_frame, text="Password:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1").grid(row=1, column=0, padx=10, pady=5, sticky="e")

username_entry = Entry(login_frame, font=("Arial", 12), width=30)
password_entry = Entry(login_frame, font=("Arial", 12), width=30, show="*")

username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

login_button = Button(login_frame, text="Login", command=login, bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
login_button.grid(row=2, column=1, pady=10)

# Main Frame
main_frame = Frame(root, bg="#f1f1f1")

# Heading
Label(main_frame, text="Student Registration", fg="#333", font=("Arial", 18, "bold"), bg="#f1f1f1").pack(pady=10)

# Student Entry Form
student_frame = Frame(main_frame, bg="#f1f1f1")
student_frame.pack()

Label(student_frame, text="ID Number:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1").grid(row=0, column=0, padx=10, pady=5, sticky="e")
Label(student_frame, text="Name:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1").grid(row=1, column=0, padx=10, pady=5, sticky="e")
Label(student_frame, text="Section:", fg="#333", font=("Arial", 12, "bold"), bg="#f1f1f1").grid(row=2, column=0, padx=10, pady=5, sticky="e")

e1 = Entry(student_frame, font=("Arial", 12), width=30)
e2 = Entry(student_frame, font=("Arial", 12), width=30)
e3 = Entry(student_frame, font=("Arial", 12), width=30)

e1.grid(row=0, column=1, padx=10, pady=5, sticky="w")
e2.grid(row=1, column=1, padx=10, pady=5, sticky="w")
e3.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Buttons
buttons_frame = Frame(main_frame, bg="#f1f1f1")
buttons_frame.pack(pady=10)

add_button = Button(buttons_frame, text="Add", command=add_student, image=button_icons["add"], compound="left", bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
edit_button = Button(buttons_frame, text="Edit", command=edit_student, image=button_icons["edit"], compound="left", bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
delete_button = Button(buttons_frame, text="Delete", command=delete_student, image=button_icons["delete"], compound="left", bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
show_button = Button(buttons_frame, text="Show Students", command=show_students, image=button_icons["show"], compound="left", bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
search_icon = PhotoImage(file="C:/Users/Nikita thakur/Desktop/Studentregistration/search.png").subsample(2)

add_button.pack(side="left", padx=10)
edit_button.pack(side="left", padx=10)
delete_button.pack(side="left", padx=10)
show_button.pack(side="left", padx=10)


# Logout Button
logout_button = Button(main_frame, text="Logout", command=logout)
logout_button.pack(pady=10)

# Section Distribution Button
section_distribution_button = Button(main_frame, text="Section Distribution", command=show_section_distribution, bg="#333", fg="#fff", font=("Arial", 12, "bold"), relief="flat")
section_distribution_button.pack(pady=10)


# Student List
list_frame = Frame(main_frame, bg="#f1f1f1")
list_frame.pack(pady=10)

# Create the treeview with scrollbars
tree_scroll = Scrollbar(list_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

listbox = ttk.Treeview(list_frame, columns=column_headings, show="headings", yscrollcommand=tree_scroll.set)

# Configure column headings
for column in column_headings:
    listbox.heading(column, text=column)

# Configure column widths
listbox.column(column_headings[0], width=100)
listbox.column(column_headings[1], width=200)
listbox.column(column_headings[2], width=100)

# Assign scrollbars to the treeview
tree_scroll.config(command=listbox.yview)

listbox.pack(fill=BOTH, expand=1)

# Show the login frame initially
login_frame.pack()

# Run the GUI
root.mainloop()
