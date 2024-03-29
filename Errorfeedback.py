import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import tkinter as tk
from tkinter import *
from tkinter import Label, Entry, Button, messagebox, ttk
import tkinter.font as font
from datetime import datetime
from PIL import ImageGrab
from tkinter import filedialog
import io


# Global variable to store the screenshot path
binary_data=""
#screenshot_path = ""
added_rows = 1
selected_class_values = ["Bike", "Car", "Escooter", "Person", "Unknown"]
correct_class_values = ["Bike", "Car", "Escooter", "Person", "Unknown"]
error_field_entries=[]
error_field_values_third_frame = []
resizable=(0,0)

def update_scrollregion(canvas,frame, root):
    canvas.update_idletasks()  # Update the canvas
    width = max(frame.winfo_reqwidth(), root.winfo_width())  # Get the width of the widest widget
    height = max(frame.winfo_reqheight(), root.winfo_height())  # Get the height of the frame
    canvas.config(scrollregion=(0, 0, width, height))
    
def callErrorExe(Email,Center):
    def image_to_binary(image):
        with io.BytesIO() as buffer:
            image.save(buffer, format="PNG")
            return buffer.getvalue()
    def capture_screenshot():
        global binary_data  # Use the global variable
 
        try:
          
            screenshot = ImageGrab.grab()
            binary_data = image_to_binary(screenshot)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot: {str(e)}")
        else:
            messagebox.showinfo("Screenshot", "Screenshot captured and saved to Database")


    def save_to_database():
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(
                host='20.204.163.178',
                database='EFBMasterData',
                user='Admin',
                password='Admin@123'
            )
            
            if conn.is_connected():
                print('Connected to MySQL database')

                cursor = conn.cursor()

                # Create table if not exists
                cursor.execute('''CREATE TABLE IF NOT EXISTS EFBMasterTable
                                (S_No INT AUTO_INCREMENT PRIMARY KEY,editor_id VARCHAR(255), job_id VARCHAR(255), maker_name VARCHAR(255),
                                error_field VARCHAR(255), error_type VARCHAR(255), error_category VARCHAR(255),center_location VARCHAR(255),  
                                error_2d_count VARCHAR(255), error_3d_count VARCHAR(255), object_id VARCHAR(255), 
                                Selected_class VARCHAR(255), Correct_class VARCHAR(255), screenshot_path LONGBLOB,
                                Audited_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                Recieved_date DATE, Production_date DATE, Acknowledged VARCHAR(255),
                                Reason_for_Rejection VARCHAR(255))''')

                # Sample values
                editor_id = Email
                job_id = job_id_entry.get()
                maker_name = maker_name_entry.get()
                second_frame_filled = any([error_type_comboboxes[i].get() or error_category_comboboxes[i].get() or 
                                       error_2d_entries[i].get() or error_3d_entries[i].get() or 
                                       object_ids_entries[i].get() for i in range(len(error_field_values))])

            # Check if any fields are filled
                if not (any([job_id, maker_name]) and second_frame_filled):
                    messagebox.showwarning("Warning", "Please fill in at least one field.")
                    return

                # Insert values from the second frame (error frame)
                for i, error_field_value in enumerate(error_field_values):
                    error_type = error_type_comboboxes[i].get()
                    error_category = error_category_comboboxes[i].get()
                    error_2d_count = error_2d_entries[i].get()
                    error_3d_count = error_3d_entries[i].get()
                    object_id = object_ids_entries[i].get()
                    if error_2d_count and not error_2d_count.isdigit():
                        messagebox.showwarning("Warning", "2D Error Count must be numeric.")
                        return
                    if error_3d_count and not error_3d_count.isdigit():
                        messagebox.showwarning("Warning", "3D Error Count must be numeric.")
                        return
                    # Check if at least one dropdown value is selected
                    if error_type or error_category or error_2d_count or error_3d_count or object_id:
                        cursor.execute('''INSERT INTO EFBMasterTable
                                        (editor_id, job_id, maker_name, 
                                        error_field, error_type, error_category,center_location, 
                                        error_2d_count, error_3d_count, object_id, screenshot_path) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)''', 
                                        (editor_id, job_id, maker_name, 
                                        error_field_value, error_type, error_category,Center, 
                                        error_2d_count, error_3d_count, object_id, binary_data))

                # Insert values from the third frame (extra frame)
                for entry in error_field_values_third_frame:
                    error_field = "Selected class wrongly"
                    error_type = entry[1].get()
                    error_category = entry[2].get()
                    selected_class = entry[3].get()
                    correct_class = entry[4].get()
                    object_id = entry[5].get()

                    # Check if at least one dropdown value is selected
                    if error_type or error_category or selected_class or correct_class or object_id:
                        cursor.execute('''INSERT INTO EFBMasterTable 
                                        (editor_id, job_id, maker_name, 
                                        error_field, error_type, error_category,center_location, 
                                        selected_class, correct_class, object_id,screenshot_path) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)''', 
                                        (editor_id, job_id, maker_name, 
                                        error_field, error_type, error_category,Center, 
                                        selected_class, correct_class, object_id,binary_data))

                conn.commit()
                messagebox.showinfo("Success", "Data saved to database successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print('MySQL connection closed')

    def add_row():
            # Maximum number of rows allowed
            max_rows = 5
            # Check if the current number of rows is less than the maximum limit
            if len(error_field_values_third_frame) < max_rows:

                # Create labels and entry widgets for the new row
                error_field_label = Label(extra_frame, text="Selected class wrongly", width=25,font=9)
                error_field_label.grid(row=len(error_field_values_third_frame) + 1, column=0, pady=5)
            
                error_type_combobox = ttk.Combobox(extra_frame, values=error_type_values, state="readonly", width=15,font=9)
                error_type_combobox.grid(row=len(error_field_values_third_frame) + 1, column=1, pady=5)
                error_category_combobox = ttk.Combobox(extra_frame, values=error_category_values, state="readonly", width=15,font=9)
                error_category_combobox.grid(row=len(error_field_values_third_frame) + 1, column=2, pady=5)
                selected_class_combobox = ttk.Combobox(extra_frame, values=selected_class_values, state="readonly", width=15,font=9)
                selected_class_combobox.grid(row=len(error_field_values_third_frame) + 1, column=3, pady=5)
                correct_class_combobox = ttk.Combobox(extra_frame, values=correct_class_values, state="readonly", width=15,font=9)
                correct_class_combobox.grid(row=len(error_field_values_third_frame) + 1, column=4, pady=5)
                object_id_entry = Entry(extra_frame, width=25,font=9)
                object_id_entry.grid(row=len(error_field_values_third_frame) + 1, column=5, pady=5)
                # Add the new entry widgets to the list
                update_scrollregion(canvas,frame, root)
                error_field_values_third_frame.append((error_field_label, error_type_combobox, error_category_combobox,
                                            selected_class_combobox, correct_class_combobox, object_id_entry))
                
            else:
                messagebox.showwarning("Maximum Rows Reached", "You can only add up to 5 rows.")
    def reset_fields():
    # Reset entry widgets
        job_id_entry.delete(0, 'end')
        maker_name_entry.delete(0, 'end')

        for entry in error_2d_entries:
            entry.delete(0, 'end')

        for entry in error_3d_entries:
            entry.delete(0, 'end')

        for entry in object_ids_entries:
            entry.delete(0, 'end')

        for var in error_type_vars:
            var.set("")

        for var in error_category_vars:
            var.set("")
        for var, combobox in zip(error_type_vars, error_type_comboboxes):
            var.set("")
            combobox.set("")

        for var, combobox in zip(error_category_vars, error_category_comboboxes):
            var.set("")
            combobox.set("")

        # Clear error field values from the third frame
        for entry in error_field_values_third_frame:
            entry[1].set("") 
            entry[2].set("")  
            entry[3].set("") 
            entry[4].set("") 
            entry[5].delete(0, 'end')  
    # GUI setup
    root = tk.Tk()
    root.title("EFB Tool")
    root.resizable(True, True)

    if root.winfo_screenwidth() > 1366:
        root.geometry('1450x850')
        root.resizable(*resizable)
    else:
        root.geometry('1350x850')
        root.resizable(True, True)

    # Create a Canvas to contain the entire application
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar for vertical scrolling
    scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side=tk.LEFT, fill="y")

    # Add a scrollbar for horizontal scrolling
    scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill="x")

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame inside the canvas to contain all the widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")


    editor_frame = Frame(frame, bd=3, relief="groove")
    editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    error_frame = Frame(frame, bd=3, relief="groove")
    error_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    extra_frame = Frame(frame, bd=3, relief="groove")
    extra_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    button_frame = Frame(frame)
    button_frame.pack(side=tk.BOTTOM,pady=10)

    # Create a bold font with increased size
    bold_font = font.Font(weight='bold', size=12)

    # Common width for labels and entry widgets
    label_width = 19  
    labelerrorwidth = 27

    Label(editor_frame, text="Editor ID:", anchor="center", justify="center", width=14, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=0, pady=5)
    editor_name_entry = Entry(editor_frame, width=25,font=9)
    editor_name_entry.grid(row=0, column=1, pady=5,padx=32)
    editor_name_entry.insert(0, Email)
    editor_name_entry.config(state="readonly")

    Label(editor_frame, text="Job ID:", anchor="center", justify="center", width=14, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=2, pady=5)
    job_id_entry = Entry(editor_frame, width=15,font=9)
    job_id_entry.grid(row=0, column=3, pady=5,padx=32)

    Label(editor_frame, text="Maker Name:", anchor="center", justify="center", width=14, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=4, pady=5,padx=5)
    maker_name_entry = Entry(editor_frame, width=23,font=9)
    maker_name_entry.grid(row=0, column=5, padx=20,pady=5)

    # Header for Error Field
    Label(error_frame, text="Error Field", anchor="center", justify="center", width=labelerrorwidth, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=0, pady=5)

    # Values for Error Field
    error_field_values = [
        "Estimation wrong", "Missed to annotate", "Tight cuboid", "Tracking wrong",
        "Ground level", "Orientation wrong", "Loose cuboid",
        "Alignment wrong", "No need to annotate", "Placement wrong", "Class type selected wrongly",
        "Include person flag wrong", "Position size unconfident flag wrong", "No error"
        ]

    for i, error_field_value in enumerate(error_field_values):
        Label(error_frame, text=error_field_value, width=labelerrorwidth,font=9).grid(row=i + 1, column=0)

        # Error Type
    Label(error_frame, text="Error Type", anchor="center", justify="center", width=label_width, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=1, pady=5)
    error_type_values = ["No Error", "Geometry Precision", "Class Precision", "Attribute Error", "Recall Error"]
    error_type_vars = [tk.StringVar() for _ in range(len(error_field_values))]
    error_type_comboboxes = [ttk.Combobox(error_frame, textvariable=var, values=error_type_values, state="readonly",
    width=15,font=9) for var in error_type_vars]
    for i, combobox in enumerate(error_type_comboboxes):
        combobox.grid(row=i + 1, column=1, pady=5)

    # Error Category
    Label(error_frame, text="Error Category", anchor="center", justify="center", width=label_width, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=2, pady=5)
    error_category_values = ["Careless", "Concept", "Difficult", "No Error"]
    error_category_vars = [tk.StringVar() for _ in range(len(error_field_values))]
    error_category_comboboxes = [
    ttk.Combobox(error_frame, textvariable=var, values=error_category_values, state="readonly",
    width=15,font=9) for var in error_category_vars]
    for i, combobox in enumerate(error_category_comboboxes):
        combobox.grid(row=i + 1, column=2, pady=5)

    # 2D Error Count
    Label(error_frame, anchor="center", justify="center", width=15, bg="blue", fg='white', text="2D Error Count",
    font=bold_font).grid(row=0, column=3, pady=5)
    error_2d_entries = [Entry(error_frame, width=12,font=9) for _ in range(len(error_field_values))]
    for i, entry in enumerate(error_2d_entries):
            entry.grid(row=i + 1, column=3, pady=5)

    # 3D Error Count
    Label(error_frame, anchor="center", justify="center", width=15, bg="blue", fg='white', text="3D Error Count",
    font=bold_font).grid(row=0, column=4, pady=5)
    error_3d_entries = [Entry(error_frame, width=12,font=9) for _ in range(len(error_field_values))]
    for i, entry in enumerate(error_3d_entries):
        entry.grid(row=i + 1, column=4, pady=5)

    # Object IDs
    Label(error_frame, text="Object IDs", anchor="center", justify="center", width=23, bg="blue", fg='white',
    font=bold_font).grid(row=0, column=5, pady=5)
    object_ids_entries = [Entry(error_frame, width=23,font=9) for _ in range(len(error_field_values))]
    for i, entry in enumerate(object_ids_entries):
        entry.grid(row=i + 1, column=5, pady=5)

    Label(extra_frame, text="Error Field", width=labelerrorwidth, bg="blue", fg='white', font=bold_font).grid(row=0, column=0, pady=15)
    error_field_label = Label(extra_frame, text="Selected class wrongly", width=labelerrorwidth,font=9)
    error_field_label.grid(row=1, column=0, pady=5)

    Label(extra_frame, text="Error Type", width=15, bg="blue", fg='white', font=bold_font).grid(row=0, column=1, pady=5)
    Label(extra_frame, text="Error Category", width=15, bg="blue", fg='white', font=bold_font).grid(row=0, column=2, pady=5)
    Label(extra_frame, text="Selected Class", width=15, bg="blue", fg='white', font=bold_font).grid(row=0, column=3, pady=5)
    Label(extra_frame, text="Correct Class", width=15, bg="blue", fg='white', font=bold_font).grid(row=0, column=4, pady=5)
    Label(extra_frame, text="Object ID", width=23, bg="blue", fg='white', font=bold_font).grid(row=0, column=5, pady=5)

    # Add Row Button for additional error fields
    add_row_button_extra = Button(extra_frame, text="Add Row", command=add_row, bg='Green', fg='white', font=bold_font)
    add_row_button_extra.grid(row=0, column=6, pady=5)

    # Initialize the list to store error field entry widgets
    error_field_entries = []

    # Initialize the first row of widgets
    add_row()
    
    # Save to Database Button
    save_button = Button(root, text="Save to Database", bg='blue', fg='white', font=bold_font, command=lambda: [save_to_database(), reset_fields()])
    save_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    # Capture Screenshot Button
    screenshot_button = Button(root, text="Take Snapshot", command=capture_screenshot, bg='blue', fg='white', font=bold_font)
    screenshot_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    #buttonreset=Button(root,text="Reset",command=reset_fields,bg='blue', fg='white', font=bold_font)
    #buttonreset.pack(side=tk.TOP, padx=10, pady=10)
    root.mainloop()
#callErrorExe("kaveri@nextwealth.com","Salem")    
