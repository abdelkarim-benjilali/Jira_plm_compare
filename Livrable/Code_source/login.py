import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, scrolledtext, messagebox,ttk
import pandas as pd
import re


# Main window<
root = tk.Tk()
root.title("Server migration")
root.geometry("400x350")
menu_bar = tk.Menu(root)

def show_help():
    help_message = (
        "This is a simple app for comparing PLM and Jira data.\n\n"
        "1. Load both PLM and Jira Excel files.\n"
        "2. Click 'Compare' to view the differences.\n"
        "3. Select the columns you want to overwrite.\n"
        "4. You can choose to export the overwritten data export the results."
    )
    messagebox.showinfo("Help", help_message)

def validate_email(event):
    email = email_entry.get()
    if email == "" or email == "user@example.com":
        email_error.config(text="", fg="black")
        return
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, email):
        email_error.config(text="Invalid email format!", fg="red")
    else:
        email_error.config(text="", fg="black")
#valider les valeurs des liens
def validate_url(event, entry, error_label, placeholder):
    url = entry.get()
    if url == "" or url == placeholder:
        error_label.config(text="", fg="black")
        return
    url_pattern = r"^(https?:\/\/)?(plm\.com|jira\.com)(\/.*)?$"
    if not re.match(url_pattern, url):
        error_label.config(text="Invalid URL! Wrong Url", fg="red")
    else:
        error_label.config(text="", fg="black")
#on click button 
def validate_inputs():
    if email_entry.get() != "user.ev@test.com" or password_entry.get() != "123456789":
        messagebox.showerror("Input Error", "Email or password are incorrect")
        return
    open_home_page()

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='gray')
    
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    
    def on_focus_out(event):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg='gray')
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)




#global variables
df_plm=None
df_jira=None
df_combined=None
column_combobox = None 

def open_file(label,text_area,data_type):
    """ Open an Excel file, display its name, and store its DataFrame globally """
    global df_plm, df_jira  # Access global variables
    
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    
    if file_path:
        try:
            df = pd.read_excel(file_path)  # Read Excel file
            
            # Store the selected DataFrame in the correct variable
            if data_type == "PLM":
                df_plm = df
            elif data_type == "Jira":
                df_jira = df

            # Display file name in the label
            label.config(text=f"Selected: {file_path.split('/')[-1]}")  

            # Display DataFrame in the text area
            text_area.delete("1.0", tk.END)  # Clear previous content
            text_area.insert(tk.END, df.to_string())  # Show Excel data in text area

            
            # Print data to confirm it's loaded
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")


def open_home_page():
    """ Load the main page with buttons to select files """
    for widget in root.winfo_children():
        widget.destroy()
        
    root.geometry("1500x1050")
# Create the "Help" men
    # PLM File Selection
    global label_plm, label_jira,text_area_jira,text_area_plm, df_plm, df_jira,text_area_compare,btn_export,overwrite_plm_radio,overwrite_jira_radio,column_combobox,btn_column_select,overwrite_var  # Make labels global so they can be updated
 # Create a frame for organizing widgets in a grid
    menu_bar = tk.Menu(root)
    
    # Create the "Help" menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help?", command=show_help)
    
    # Add the Help menu to the menu bar
    menu_bar.add_cascade(label="Help?", menu=help_menu)
    
    # Configure the window to display the menu bar
    root.config(menu=menu_bar)

    # Create a frame for organizing widgets in a grid
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # PLM File Selection (Left Side)
    btn_open_plm = tk.Button(frame, text="Select PLM Database", 
                             command=lambda: open_file(label_plm, text_area_plm, "PLM"))
    btn_open_plm.grid(row=0, column=0, padx=10, pady=10)  # Place in grid

    label_plm = tk.Label(frame, text="No file selected", fg="blue")
    label_plm.grid(row=1, column=0, padx=10, pady=5)

    text_area_plm = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=15)
    text_area_plm.grid(row=2, column=0, padx=10, pady=10)

    # Jira File Selection (Right Side)
    btn_open_jira = tk.Button(frame, text="Select Jira Database", 
                              command=lambda: open_file(label_jira, text_area_jira, "Jira"))
    btn_open_jira.grid(row=0, column=1, padx=10, pady=10)  # Place in grid

    label_jira = tk.Label(frame, text="No file selected", fg="blue")
    label_jira.grid(row=1, column=1, padx=10, pady=5)

    text_area_jira = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=15)
    text_area_jira.grid(row=2, column=1, padx=10, pady=10)

    # ** Comparison Section (Below PLM & Jira) **
    label_compare = tk.Label(frame, text="Comparison Results:", fg="green")
    label_compare.grid(row=3, column=0, columnspan=1, pady=10)

    text_area_compare = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
    text_area_compare.grid(row=4, column=0, columnspan=2, pady=10)

    btn_compare = tk.Button(frame, text="Compare 2 Databases", command=compare_databases)
    btn_compare.grid(row=3, column=1,padx=10,pady=10)

    # Export Button
    btn_export = tk.Button(frame, text="Export Results", command=export_to_excel,state="disabled")
    btn_export.grid(row=9, column=0, columnspan=2, pady=30)

    # Create a checkbox for overwriting PLM or Jira
    overwrite_var = tk.IntVar(value=1)

    overwrite_plm_radio = tk.Radiobutton(frame, text="Overwrite PLM Data", variable=overwrite_var, value=1)
    overwrite_plm_radio.grid(row=6, column=0, padx=10, pady=2)

    overwrite_jira_radio = tk.Radiobutton(frame, text="Overwrite Jira Data", variable=overwrite_var, value=2)
    overwrite_jira_radio.grid(row=7, column=0, padx=10, pady=2)

    btn_column_select = tk.Button(frame, text="Select Columns to Overwrite", command=open_column_selection_dialog, state="disabled")
    btn_column_select.grid(row=7, column=1, padx=10, pady=10)

def get_selected_option():
    selection = overwrite_var.get()
    if selection == 1:
        print("Overwrite PLM Data selected")
    elif selection == 2:
        print("Overwrite Jira Data selected")

def compare_databases():
    """ Compare PLM and Jira DataFrames and show differences """
    global df_plm, df_jira,df_combined,column_combobox

    if df_plm is None or df_jira is None:
        messagebox.showwarning("Warning", "Please load both databases before comparing!")
        return

    try:
        # Column name mappings between PLM and Jira (you can extend this as needed)
        column_mapping = {
            "id": "CRID",  
            "headline": "Title", 
            "priority": "Priority", 
            "substate": "State", 
            "product_version": "PRODUCT VERSION NAME",
        }

        # Merge the two DataFrames on the 'id' and 'CRID' columns
        df_combined = pd.merge(df_plm, df_jira, left_on="id", right_on="CRID", suffixes=('_plm', '_jira'), how='outer', indicator=True)

        print("Merged DataFrame columns:", df_combined.columns)

        df_combined.rename(columns={"id": "id_plm", "CRID": "id_jira"}, inplace=True)
        df_combined = df_combined.drop(columns=["_merge"])

        print("Renamed DataFrame columns:", df_combined.columns)
        # Add 'mismatch' column to check if other columns are the same
        mismatch_column = []

        # Loop through the rows to compare non-ID columns
        for index, row in df_combined.iterrows():
            mismatch = "No"  # Assume no mismatch by default
            
            # Compare the columns based on the column mapping
            for plm_col, jira_col in column_mapping.items():
                # Skip the ID column comparison
                if plm_col != "id":
                    plm_value = row[f"{plm_col}"]
                    jira_value = row[f"{jira_col}"]
                    
                    # If values do not match, mark as mismatch
                    if plm_value != jira_value:
                        mismatch = "Yes"
                        break  # Stop at the first mismatch

            mismatch_column.append(mismatch)

        # Add the mismatch column to the DataFrame
        df_combined['mismatch'] = mismatch_column

        # Show the combined result (with mismatch info) in the comparison text area
        text_area_compare.delete("1.0", tk.END)
        text_area_compare.insert(tk.END, df_combined.to_string(index=False))  # Display the DataFrame without index
        
       
        btn_column_select.config(state="normal", bg="green")

    except Exception as e:
        messagebox.showerror("Error", f"Could not compare databases: {e}")





def open_column_selection_dialog():
    """Open a dialog with checkboxes to select columns for overwrite based on selection"""
    global df_combined,selected_columns

    if df_combined is None:
        messagebox.showwarning("Warning", "No comparison has been made yet!")
        return

    # Determine selection (PLM or Jira)
    selected_option = overwrite_var.get()  # 1 = PLM, 2 = Jira

    # Select columns based on user choice
    if selected_option == 1:
        columns_to_display = df_combined.columns[1:5]  # PLM columns
    else:
        columns_to_display = df_combined.columns[6:10]  # Jira columns

    # Create Dialog Window
    dialog = tk.Toplevel(root)
    dialog.title("Select Columns to Overwrite")

    selected_columns = []

    def toggle_selection(column, var):
        if var.get() == 1:
            selected_columns.append(column)
        else:
            if column in selected_columns:
                selected_columns.remove(column)

    row = 0
    checkbox_vars = {}

    for column in columns_to_display:
        var = tk.IntVar()
        checkbox_vars[column] = var
        checkbox = tk.Checkbutton(dialog, text=column, variable=var, 
                                  command=lambda col=column, v=var: toggle_selection(col, v))
        checkbox.grid(row=row, column=0, sticky="w", padx=10, pady=2)
        row += 1

    def on_ok():
        messagebox.showinfo("Selected Columns", f"You selected: {', '.join(selected_columns)}")
        dialog.destroy()

    ok_button = tk.Button(dialog, text="OK", command=on_ok)
    ok_button.grid(row=row, column=0, pady=10)
    btn_export.config(state="normal",bg="green")
    dialog.mainloop()
    
def export_to_excel():
    """Export the result to an Excel file with selected overwrite columns"""
    global df_combined, selected_columns

    if df_combined is None or not selected_columns:
        messagebox.showwarning("Warning", "No comparison has been made yet or no columns selected!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls")])
    
    if file_path:
        try:
            if overwrite_var.get() == 1:  # Overwrite PLM with Jira
                df_export = df_combined.iloc[:, :5].copy()  # Copy PLM Data (Columns 1-5)
                
                for col in selected_columns:
                    plm_col_index = df_combined.columns.get_loc(col)  # Get PLM column index
                    jira_col_index = plm_col_index + 5  # Find corresponding Jira column index

                    if 0 <= plm_col_index < 5 and 5 <= jira_col_index < 10:
                        df_export.iloc[:, plm_col_index] = df_combined.iloc[:, jira_col_index]  # Overwrite PLM

            elif overwrite_var.get() == 2:  # Overwrite Jira with PLM
                df_export = df_combined.iloc[:, 5:10].copy()  # Copy Jira Data (Columns 6-10)

                for col in selected_columns:
                    jira_col_index = df_combined.columns.get_loc(col)  # Get Jira column index
                    plm_col_index = jira_col_index - 5  # Find corresponding PLM column index

                    if 5 <= jira_col_index < 10 and 0 <= plm_col_index < 5:
                        df_export.iloc[:, jira_col_index - 5] = df_combined.iloc[:, plm_col_index]  # Overwrite Jira

            # Save to Excel
            df_export.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data exported successfully to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not export data: {e}")
tk.Label(root, text="First Server Link:").pack()
server1_entry = tk.Entry(root, width=40)
server1_entry.pack()
add_placeholder(server1_entry, "https://plm.com")
server1_error = tk.Label(root, text="", fg="black")
server1_error.pack()
server1_entry.bind("<FocusOut>", lambda event: validate_url(event, server1_entry, server1_error, "https://plm.com"))

tk.Label(root, text="Second Server Link:").pack()
server2_entry = tk.Entry(root, width=40)
server2_entry.pack()
add_placeholder(server2_entry, "https://jira.com")
server2_error = tk.Label(root, text="", fg="black")
server2_error.pack()
server2_entry.bind("<FocusOut>", lambda event: validate_url(event, server2_entry, server2_error, "https://jira.com"))

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()
add_placeholder(email_entry, "user@example.com")
email_error = tk.Label(root, text="", fg="black")
email_error.pack()
email_entry.bind("<FocusOut>", validate_email)

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=validate_inputs).pack(pady=10)

root.mainloop()
