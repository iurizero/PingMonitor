import tkinter as tk
from interface import PingApp

def main():
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
