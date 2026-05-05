from tkinter import *
app = Tk()
app.geometry("400x250")
app.configure(bg="#F1F5F9")
Label(
 app,
 text="Interface Moderne",
 bg="#0F172A",
 fg="white",
 font=("Arial", 18, "bold"), pady=15 ).pack(fill=X)
Button(
 app,
 text="Valider",
 bg="#2563EB",
 fg="white",
 font=("Arial", 12, "bold")
).pack(pady=40)
app.mainloop()