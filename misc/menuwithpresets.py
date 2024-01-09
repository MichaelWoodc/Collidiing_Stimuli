import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Widget Updater")

        # Variables to store widget values
        self.scroll_var = tk.StringVar()
        self.slider_var = tk.DoubleVar()
        self.check_var = tk.BooleanVar()
        self.radio_var = tk.StringVar()

        # Create a drop-down menu for presets
        preset_options = ["Default", "Preset 1", "Preset 2", "Preset 3", "Custom"]
        self.preset_var = tk.StringVar(value="Default")
        preset_menu = ttk.Combobox(root, textvariable=self.preset_var, values=preset_options)
        preset_menu.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        preset_menu.bind("<<ComboboxSelected>>", self.update_widgets)

        # Scrollbox
        self.scrollbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False)
        self.scrollbox.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        # Slider
        self.slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.slider_var)
        self.slider.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")

        # Checkbutton
        self.checkbutton = tk.Checkbutton(root, text="Check me", variable=self.check_var)
        self.checkbutton.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        # Radiobuttons
        radio_frame = ttk.Frame(root)
        radio_frame.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")

        radio1 = tk.Radiobutton(radio_frame, text="Option 1", variable=self.radio_var, value="Option 1")
        radio1.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        radio2 = tk.Radiobutton(radio_frame, text="Option 2", variable=self.radio_var, value="Option 2")
        radio2.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        radio3 = tk.Radiobutton(radio_frame, text="Option 3", variable=self.radio_var, value="Option 3")
        radio3.grid(row=2, column=0, pady=5, padx=5, sticky="w")

        # Set initial values
        self.update_widgets()

    def update_widgets(self, event=None):
        # Get the current preset
        current_preset = self.preset_var.get()

        # Update widget values based on the preset
        if current_preset == "Default":
            self.scroll_var.set("Option 1")
            self.slider_var.set(50)
            self.check_var.set(True)
            self.radio_var.set("Option 1")
        elif current_preset == "Preset 1":
            self.scroll_var.set("Option 2")
            self.slider_var.set(30)
            self.check_var.set(False)
            self.radio_var.set("Option 2")
        elif current_preset == "Preset 2":
            self.scroll_var.set("Option 3")
            self.slider_var.set(70)
            self.check_var.set(True)
            self.radio_var.set("Option 3")
        elif current_preset == "Preset 3":
            self.scroll_var.set("Option 1")
            self.slider_var.set(80)
            self.check_var.set(False)
            self.radio_var.set("Option 1")
        elif current_preset == "Custom":
            # Handle custom values here
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
