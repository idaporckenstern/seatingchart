import tkinter as tk
import database

class student():
    no_seat_location = 100
    def __init__(self, id, first_name, last_name, seat, canvas, hour, save_button, seats, drop_label, cursor):
        self.id = id
        self.last_name = last_name
        self.seat = seat
        self.hour = hour
        self.save_button = save_button
        self.canvas = canvas
        self.seats = seats
        self.drop_label = drop_label
        self.cursor = cursor

        #checking for any second first names
        tempName = first_name.split(" ")
        self.first_name = tempName[0]

    #drag start and motion both update where the label is according to mouse position (drag and drop)
    def drag_start(self, event):
        self.label.startX = event.x
        self.label.startY = event.y
    
    def drag_motion(self, event):
        self.xpos = self.label.winfo_x() - self.label.startX + event.x
        self.ypos = self.label.winfo_y() - self.label.startY + event.y
        self.label.place(x=self.xpos, y=self.ypos)
        self.canvas.itemconfigure(self.save_button, state = 'normal')
        
    #updates the label position based on the seat they are assigned
    def update_position(self):
        if self.seat != "NULL":
            self.label.place(x = self.seat.x, y = self.seat.y)
        else:
            self.label.place(x = 10, y = student.no_seat_location)
            student.no_seat_location += 20

    #when a student is dragged and dropped onto a seat it will switch places with that student
    #it checks what student is assigned to that seat and swaps the students for each seat and the seat for each student
    def swap_seats(self, event):
        buffer = 30
        for seat in self.seats:
            if (self.xpos > seat.x - buffer) and (self.xpos < seat.x + buffer) and (self.ypos > seat.y - buffer) and (self.ypos < seat.y + buffer):
                if seat.student != "NULL":
                    self.tempStudent = seat.student
                    self.tempStudent.seat = self.seat
                    seat.student = self
                    self.seat.student = self.tempStudent
                    self.seat = seat
                    self.tempStudent.update_position()
                else:
                    self.seat.student = "NULL"
                    self.seat = seat
                    seat.student = self
                break
        if (self.xpos > self.drop_label.winfo_x() - buffer) and (self.xpos < self.drop_label.winfo_x() + buffer) and (self.ypos > self.drop_label.winfo_y() - buffer) and (self.ypos < self.drop_label.winfo_y() + buffer):
            
            database.dropStudent(self.id, self.hour, self.cursor)
            self.label.destroy()
            return
        self.update_position()

    #checks for any kids with the same first name
    def check_name(self, students):
        for student in students:
            if student.id == self.id:
                continue
            if student.first_name == self.first_name:
                self.name = self.first_name + " " + self.last_name[0] 
                return
        self.name = self.first_name



    #creating a label for the student and placing them in their seat if they have one, and to the left if they do not
    def create_label(self):
        self.label = tk.Label(self.canvas, bg = "white", text = self.name, font = 20, anchor="center")
        self.label.bind("<Button-1>", self.drag_start)
        self.label.bind("<B1-Motion>", self.drag_motion)
        self.label.bind("<ButtonRelease-1>", self.swap_seats)

        self.tempStudent = "NULL"
        
        if self.seat != "NULL":
            self.label.place(x = self.seat.x,y =  self.seat.y)
        else:
            self.label.place(x = 10,y =  student.no_seat_location)
            student.no_seat_location += 20

