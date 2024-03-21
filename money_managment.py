import json
import tkinter as tk
from tkinter import messagebox, filedialog

selected_file_path = None
is_first_save = True

# Initialize the transactions list at the top
transactions = []

# Define the function to add transactions
def add_transaction(description, amount, date, transaction_type):
    global transactions
    transaction = {'description': description, 'amount': amount, 'date': date, 'type': transaction_type}
    transactions.append(transaction)
    save_transactions()

# Define the function to calculate the balance
def calculate_balance():
    balance = 0
    for transaction in transactions:
        if transaction['type'] == 'income':
            balance += transaction['amount']
        elif transaction['type'] == 'expense':
            balance -= transaction['amount']
    return balance

# Define the function to save transactions to a file
def save_transactions(default_filename='transactions.json'):
    global selected_file_path, is_first_save  # Refer to the global variable
    
    # If the file path hasn't been chosen before, ask the user to select it
    if not selected_file_path:
        selected_file_path = filedialog.asksaveasfilename(
            defaultextension=".json", 
            initialfile=default_filename, 
            filetypes=[("JSON files", "*.json")], 
            title="Save Transactions"
        )
        
        if not selected_file_path:  # If the user cancels the dialog
            messagebox.showwarning("Save Cancelled", "Save operation was cancelled. Your transactions were not saved.")
            return  # Exit the function without saving

    try:
        with open(selected_file_path, 'w') as file:
            json.dump(transactions, file)
        if is_first_save:
            messagebox.showinfo("Transactions Saved", f"Your transactions have been saved to: {selected_file_path}")
            is_first_save = False
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving transactions: {e}")
        selected_file_path = None  # Reset if there was an error, prompting the user to choose again next time


# Define the function to load transactions from a file
def load_transactions(filename='transactions.json'):
    global transactions
    try:
        with open(filename, 'r') as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []

# Define the function to remove transactions
def remove_transaction(description):
    global transactions
    transactions = [transaction for transaction in transactions if transaction['description'] != description]
    save_transactions()

# GUI Code
def add_transaction_gui():
    description = entry_description.get()
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the amount.")
        return
    date = entry_date.get()
    transaction_type = entry_type.get()
    add_transaction(description, amount, date, transaction_type)
    display_transactions()

def display_transactions():
    transactions_text = "\n".join([f"{t['date']}: {t['description']} ({t['type']}) - ${t['amount']}" for t in transactions])
    label_transactions.config(text=f'Transactions:\n{transactions_text}')
    label_balance.config(text=f'Balance: ${calculate_balance()}')

# Main window setup
root = tk.Tk()
root.title("Personal Budget Tracker")
root.geometry('400x400')

# GUI setup for input fields and buttons
label_description = tk.Label(root, text='Description:')
label_description.pack()
entry_description = tk.Entry(root)
entry_description.pack()

label_amount = tk.Label(root, text="Amount:")
label_amount.pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

label_date = tk.Label(root, text='Date (YYYY-MM-DD)')
label_date.pack()
entry_date = tk.Entry(root)
entry_date.pack()

label_type = tk.Label(root, text="Type (income/expense):")
label_type.pack()
entry_type = tk.Entry(root)
entry_type.pack()

button_add = tk.Button(root, text="Add Transaction", command=add_transaction_gui)
button_add.pack()

label_transactions = tk.Label(root, text="Transactions will be listed here.")
label_transactions.pack()
label_balance = tk.Label(root, text="Balance will be displayed here.")
label_balance.pack()

# Load transactions from file and display them
load_transactions()
display_transactions()

# Start the GUI event loop
if __name__ == "__main__":
    root.mainloop()
