import tkinter as tk

class seat():
    edit = False
    def __init__(self, seat_number, x, y, canvas, student):
        self.seat_number = seat_number
        self.x = x
        self.y = y
        self.label = tk.Label(canvas, bg = "white", text = seat_number, anchor="center")
        self.label.place(x = self.x, y = self.y)
        self.label.bind("<Button-1>", self.drag_start)
        self.label.bind("<B1-Motion>", self.drag_motion)
        self.student = student
        

    #drag and drop setup for the seats. Only works if the edit seat button is pressed
    def drag_start(self, event):
        self.label.startX = event.x
        self.label.startY = event.y
    
    def drag_motion(self, event):
        if self.edit == True:
            self.x = self.label.winfo_x() - self.label.startX + event.x
            self.y = self.label.winfo_y() - self.label.startY + event.y
            self.label.place(x=self.x, y=self.y)