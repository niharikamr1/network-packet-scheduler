import tkinter as tk
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    # Apply a modern theme if available, otherwise default
    try:
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
        
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
