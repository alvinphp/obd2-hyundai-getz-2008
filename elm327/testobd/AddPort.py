import tkinter as tk

root = tk.Tk()
root.title("Mi primera ventana")
root.geometry("300x200")

label = tk.Label(root, text="Hola mundo", font=("Arial", 16))
label.pack(expand=True)

root.mainloop()