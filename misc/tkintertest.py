import tkinter as tk
from tkinter import ttk

def on_button_click():
    value = entry_var.get()
    print(f"Text Entry Value: {value}")

    spinbox_value = spinbox_var.get()
    print(f"Spinbox Value: {spinbox_value}")

    scale_value = scale_var.get()
    print(f"Scale Value: {scale_value}")

    selected_radio = radio_var.get()
    print(f"Selected Radio Button: {selected_radio}")

    check_value = check_var.get()
    print(f"Check Button Value: {check_value}")

    dropdown_value = dropdown_var.get()
    print(f"Dropdown Value: {dropdown_value}")

    # Update the Text widget
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Text Entry Value: {value}\n")
    result_text.insert(tk.END, f"Spinbox Value: {spinbox_value}\n")
    result_text.insert(tk.END, f"Scale Value: {scale_value}\n")
    result_text.insert(tk.END, f"Selected Radio Button: {selected_radio}\n")
    result_text.insert(tk.END, f"Check Button Value: {check_value}\n")
    result_text.insert(tk.END, f"Dropdown Value: {dropdown_value}\n")

def update_scale_label(value):
    scale_value_label.config(text=f"Current Value: {value}")

def update_scale_2_label(value):
    scale_2_value_label.config(text=f"Current Value: {value}")
# Create the main window
window = tk.Tk()
window.title("Input Options Example")

# Menu Bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)

# Text Entry
entry_var = tk.StringVar()
entry_label = ttk.Label(window, text="Text Entry:")
entry_label.grid(row=0, column=0, pady=5)
entry_entry = ttk.Entry(window, textvariable=entry_var)
entry_entry.grid(row=0, column=1, pady=5)

# Spinbox
spinbox_var = tk.IntVar()
spinbox_label = ttk.Label(window, text="Spinbox:")
spinbox_label.grid(row=1, column=0, pady=5)
spinbox_spinbox = ttk.Spinbox(window, from_=0, to=10, textvariable=spinbox_var)
spinbox_spinbox.grid(row=1, column=1, pady=5)

# Scale (Slider)
scale_label = tk.Label(window, text="Scale:")
scale_var = tk.DoubleVar()
scale = tk.Scale(window, from_=0, to=10, orient=tk.HORIZONTAL, variable=scale_var, command=lambda value: update_scale_label(value))
scale_label.grid(row=2, column=0, pady=5)
scale.grid(row=2, column=1, pady=5)
scale_value_label = ttk.Label(window, text="Current Value: 0.0")
scale_value_label.grid(row=2, column=2, pady=5)



# Radio Buttons
radio_var = tk.StringVar()
radio_label = ttk.Label(window, text="Radio Buttons:")
radio_label.grid(row=3, column=0, pady=5)
radio_frame = ttk.Frame(window)
radio_frame.grid(row=3, column=1, pady=5)
radio_button1 = ttk.Radiobutton(radio_frame, text="Option 1", variable=radio_var, value="Option 1")
radio_button1.grid(row=0, column=0)
radio_button2 = ttk.Radiobutton(radio_frame, text="Option 2", variable=radio_var, value="Option 2")
radio_button2.grid(row=0, column=1)

# Check Button
check_var = tk.BooleanVar()
check_label = ttk.Label(window, text="Check Button:")
check_label.grid(row=4, column=0, pady=5)
check_check = ttk.Checkbutton(window, variable=check_var)
check_check.grid(row=4, column=1, pady=5)

# Drop-down Select
dropdown_var = tk.StringVar()
dropdown_label = ttk.Label(window, text="Dropdown:")
dropdown_label.grid(row=5, column=0, pady=5)
dropdown_values = ["Option 1", "Option 2", "Option 3"]
dropdown_select = ttk.Combobox(window, textvariable=dropdown_var, values=dropdown_values)
dropdown_select.grid(row=5, column=1, pady=5)

# Button to trigger action
action_button = ttk.Button(window, text="Get Values", command=on_button_click)
action_button.grid(row=6, column=0, columnspan=3, pady=10)

# Scale
scale_2_var = tk.DoubleVar()
scale_2_label = ttk.Label(window, text="Scale:")
scale_2_label.grid(row=7, column=0, pady=5)
scale_2_scale = ttk.Scale(window, from_=0, to=10, orient=tk.HORIZONTAL, variable=scale_2_var, length=200,
                        command=lambda value: update_scale_2_label(value))
scale_2_scale.grid(row=7, column=1, pady=5)
scale_2_value_label = ttk.Label(window, text="Current Value: 0.0")
scale_2_value_label.grid(row=7, column=2, pady=5)

# Text widget to display results
result_text = tk.Text(window, height=10, width=40)
result_text.grid(row=8, column=0, columnspan=3, pady=10)

# Start the main loop
window.mainloop()
