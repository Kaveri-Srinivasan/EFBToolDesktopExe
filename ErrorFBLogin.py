import tkinter as tk
from tkinter import messagebox
import mysql.connector
import tkinter.font as font
#import Sampletest as ExeSampletest
import Errorfeedback as Productionfile



def validate_login(Email , password):
    try:
        db_connection = mysql.connector.connect(
            host="20.204.163.178",
            user="Admin",
            password="Admin@123",
            database="EFBMasterData"
        )

        cursor = db_connection.cursor()

        # Execute a query to fetch user details based on the provided username and password
        query = "SELECT Role FROM Users WHERE Email = %s AND Password = %s"
        cursor.execute(query, (Email, password))
        result = cursor.fetchone()

        if result:
            role = result[0]
            if role == "Editor":
                messagebox.showinfo("Login Successful", f"Welcome, {Email}!") 
                Productionfile.callErrorExe(Email)
            else:
                messagebox.showerror("Access Denied", "You don't have access to login.")
        else:
            messagebox.showerror("Invalid Credentials", "Please enter valid credentials.")

        cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")




def login_clicked():
    username = entry_username.get()
    password = entry_password.get()
    validate_login(username, password)

#def logout_clicked():
    #print("Logout button clicked.")
    #entry_username.delete(0, tk.END)
    #entry_password.delete(0, tk.END)
    #ExeSampletest.close_application()
    #root.destroy()
    

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry('350x180')
root.resizable(False, False)
root.configure(bg='navyblue')
# Create a bold font with increased size
bold_font = font.Font(weight='bold', size=12)
   
    # Common width for labels and entry widgets
label_width = 12  # Adjust this value as needed
labelerrorwidth = 20
# Create and place the widgets
label_username = tk.Label(root,anchor="w", justify="left", width=label_width,
          font=bold_font, text="Email:")
label_password = tk.Label(root,anchor="w", justify="left", width=label_width,
          font=bold_font, text="Password:")

entry_username = tk.Entry(root,justify="left", width=labelerrorwidth,font=bold_font)
entry_password = tk.Entry(root,justify="left", width=labelerrorwidth ,show="*",font=bold_font)

button_login = tk.Button(root, text="Login",bg='green', fg='white',width=label_width, font=bold_font, command=login_clicked,cursor="hand2", highlightbackground="gray")



# Place the widgets using the grid layout
label_username.grid(row=1, column=0, padx=10, pady=12, sticky=tk.W)
label_password.grid(row=2, column=0, padx=10, pady=12, sticky=tk.W)
entry_username.grid(row=1, column=1, padx=10, pady=10)
entry_password.grid(row=2, column=1, padx=10, pady=10)
#button_login.grid(row=2, column=0, pady=15)
button_login.place(x=120,y=120)
#button_logout.grid(row=2, column=1, pady=15)

# Run the main loop
root.mainloop()
