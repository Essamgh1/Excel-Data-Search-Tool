import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import webbrowser

# Function to load Excel data from all sheets
def load_data(file_path):
    try:
        sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        df = pd.concat(sheets.values(), ignore_index=True)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return None

# Function to search data
def search_data():
    query = search_entry.get()
    if query == "":
        messagebox.showwarning("Input Error", "Please enter a search term")
        return
    
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    
    for row in tree.get_children():
        tree.delete(row)
    
    for index, row in results.iterrows():
        tree.insert("", tk.END, values=list(row))

    if results.empty:
        messagebox.showinfo("No results", "No matching records found")

# Function to clear results
def clear_results():
    for row in tree.get_children():
        tree.delete(row)

# Function to select file
def select_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        df = load_data(file_path)
        if df is not None:
            tree["columns"] = list(df.columns)
            tree["show"] = "headings"
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            clear_results()
            
            file_name_label.config(text=os.path.basename(file_path))
            status_label.config(text="✔️ File Loaded", fg="green")
            
            search_frame.pack(pady=10)
            results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Function to open LinkedIn profile
def open_linkedin(event):
    webbrowser.open_new("https://www.linkedin.com/in/essam-alghamdii/")

# Setting up the main application window
root = tk.Tk()
root.title("Integrated Data and Automation")

# Setting the application icon
logo_path = 'F:\مشاريع\EmailSender\excel_search\logo green.png'  # Update the path to your logo image
logo_image = tk.PhotoImage(file=logo_path)
root.iconphoto(False, logo_image)

root.geometry("800x600")

# Frame for file selection
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

select_file_button = tk.Button(file_frame, text="Select Excel File", command=select_file)
select_file_button.pack(side=tk.LEFT, padx=10)

file_name_label = tk.Label(file_frame, text="")
file_name_label.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(file_frame, text="")
status_label.pack(side=tk.LEFT, padx=10)

# Frame for search
search_frame = tk.Frame(root)

tk.Label(search_frame, text="Enter search term:").pack(side=tk.LEFT, padx=10)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Search", command=search_data)
search_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(search_frame, text="Clear Results", command=clear_results)
clear_button.pack(side=tk.LEFT, padx=10)

# Frame for results
results_frame = tk.Frame(root)
tree = ttk.Treeview(results_frame)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Label for signature with hyperlink
signature_label = tk.Label(root, text="by Essam Alghamdi", fg="blue", cursor="hand2")
signature_label.pack(side=tk.BOTTOM, pady=10)
signature_label.bind("<Button-1>", open_linkedin)

root.mainloop()
























