import tkinter as tk
import mysql.connector
import random
import seatClass
import studentClass

#changes what class seating chart is shown from the drop down menu, erases labels from previous class display
#and pulls the new set of students from the database
def change_class(event):
    if students:
        for student in students:
            if student.seat != "NULL":
                student.seat.student = "NULL"
            student.label.destroy()
        studentClass.student.no_seat_location = 100
        students.clear()

    if clicked.get() == "First hour":
        hour = "first_hour"
        sql = "SELECT * FROM first_hour ORDER BY seat_number DESC"
    elif clicked.get() == "Second hour":
        hour = "second_hour"
        sql = "SELECT * FROM second_hour ORDER BY seat_number DESC"
    elif clicked.get() == "Third hour":
        hour = "third_hour"
        sql = "SELECT * FROM third_hour ORDER BY seat_number DESC"
    elif clicked.get() == "Sixth hour":
        hour = "sixth_hour"
        sql = "SELECT * FROM sixth_hour ORDER BY seat_number DESC"
    elif clicked.get() == "Seventh hour":
        hour = "seventh_hour"
        sql = "SELECT * FROM seventh_hour ORDER BY seat_number DESC"

    cursor.execute(sql)
    results = cursor.fetchall()
    

    i = 0
    for seat in seats:
        if results[i][3] == seat.seat_number:
          students.append(studentClass.student(results[i][0], results[i][1], results[i][2], seat, canvas, hour, save_button_window, seats, drop_label, cursor))
          seat.student = students[i]  
          i+=1
          if i >= len(results):
              break
    for result in results:
        if result[3] == (None):
            students.append(studentClass.student(result[0], result[1], result[2], "NULL", canvas, hour, save_button_window, seats, drop_label, cursor))

    for student in students:
        student.check_name(students)
        student.create_label()

    canvas.itemconfigure(add_button_window, state = 'normal')


#arranges the list of students alphabetically and puts them in the corresponding seat

def alphabetize(event):
    i = len(seats) - 1
    students.sort(key= lambda x: x.last_name)
    for student in students:
        student.seat = seats[i]
        seats[i].student = student
        i-=1
        student.update_position()
    canvas.itemconfigure(save_button_window, state = 'normal')


#arranges the list of students randomly and puts them in the corresponding seat
def randomize(event):
    i = len(seats) - 1
    random.shuffle(students)
    for student in students:
        student.seat = seats[i]
        seats[i].student = student
        i-=1
        student.update_position()
    canvas.itemconfigure(save_button_window, state = 'normal')


#takes all of the students and sets their seat to null
#THIS DOES NOT WORK YET BECAUSE IT DOES NOT LIKE NULL SEATS
def clear_seats(event):
    studentClass.student.no_seat_location = 100
    for student in students:
        student.seat.student = "NULL"
        student.seat = "NULL"
        student.update_position()
    canvas.itemconfigure(save_button_window, state = 'normal')


#this allows you to drag and drop the locations of the seat on the image. If there is already a class listed you will need to clear it first so you can see the seats
def edit_seat_locations(event):
    seatClass.seat.edit = True
    canvas.itemconfigure(save_button_window, state = 'normal')


#pushes all of the changes of the seats and students to the database
def save(event):
    seatClass.seat.edit = False
    for seat in seats:
        sql = "UPDATE seats SET x_pos = %s, y_pos = %s WHERE seat_number = %s"
        val = (seat.x, seat.y, seat.seat_number)
        cursor.execute(sql, val)

        

    for student in students:
        if(student.seat != "NULL"):
            sql = "UPDATE " + student.hour + " SET seat_number = %s WHERE id = %s"
            val = (student.seat.seat_number, student.id)
            cursor.execute(sql, val)
        else:
            #THIS NEEDS TO BE FIXED. DOES NOT LIKE SETTING VALUE TO NULL
            sql = "UPDATE " + student.hour + " SET seat_number = %s WHERE id = %s"
            val = ("NULL", student.id)
            cursor.execute(sql, val)
    studentdb.commit()

    canvas.itemconfigure(save_button_window, state = 'hidden')

def toggleAddStudentOff(event):
    addStudent(int(idTextBox.get()), firstNameTextBox.get(), lastNameTextBox.get())
    canvas.itemconfigure(submitButton_window, state = "hidden")
    tk.Place.forget(idTextBox)
    tk.Place.forget(firstNameTextBox)
    tk.Place.forget(lastNameTextBox)


def toggleAddStudentOn(event):
    idTextBox.place(x = 1050, y = 10)
    idTextBox.insert(0, "id")
    firstNameTextBox.place(x = 1150, y = 10)
    firstNameTextBox.insert(0, "First Name")
    lastNameTextBox.place(x = 1300, y = 10)
    lastNameTextBox.insert(0, "Last Name")
    canvas.itemconfigure(submitButton_window, state = "normal")

def addStudent(id, firstName, lastName):
    if clicked.get() == "First hour":
        hour = "first_hour"
    elif clicked.get() == "Second hour":
        hour = "second_hour"
    elif clicked.get() == "Third hour":
        hour = "third_hour"
    elif clicked.get() == "Sixth hour":
        hour = "sixth_hour"
    elif clicked.get() == "Seventh hour":
        hour = "seventh_hour"
    
    sql = "INSERT INTO " + hour + " (id, first_name, last_name) VALUES (%s, %s, %s)"
    val = (id, firstName, lastName)
    cursor.execute(sql, val)
    studentdb.commit()
    newStudent = studentClass.student(id, firstName, lastName, "NULL", canvas, hour, save_button, seats, drop_label, cursor)
    newStudent.check_name(students)
    newStudent.create_label()
    newStudent.seat = "NULL"
    students.append(newStudent)


#database info
studentdb = mysql.connector.connect(
    host = "localhost",
    user = "josh",
    password = "password",
    database="students"
)

cursor = studentdb.cursor()

#tkinter setup
root = tk.Tk()
root.title('Seating chart')
root.geometry('1920x1080')

#background image setup
bg = tk.PhotoImage(file = "ClassroomSetup.png")
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image = bg, anchor = "nw")

#Creating labels for seats
sql = "SELECT * FROM seats ORDER BY seat_number DESC"
cursor.execute(sql)
results = cursor.fetchall()

seats = []
students = []
for seat in results:
    seats.append(seatClass.seat(seat[0], seat[1], seat[2], canvas, "NULL"))

#setup buttons and class dropdown menu
clicked = tk.StringVar()
clicked.set("Select a class")

drop = tk.OptionMenu(
    canvas, 
    clicked,
    "First hour", "Second hour", "Third hour", "Sixth hour", "Seventh hour",
    command = change_class
)
drop.place(x = 10, y = 10)

save_button = tk.Button(root, text = "save")
save_button_window = canvas.create_window(759, 10, anchor = "nw", window = save_button)
save_button.bind("<Button-1>", save)
canvas.itemconfigure(save_button_window, state = 'hidden')

drop_label = tk.Label(canvas, bg = "white", text = "drop student", font = 20, anchor = "center")
drop_label.place(x = 830, y = 10)

add_button = tk.Button(root, text = "add student")
add_button_window = canvas.create_window(950, 10, anchor = "nw", window = add_button)
add_button.bind("<Button-1>", toggleAddStudentOn)
canvas.itemconfigure(add_button_window, state = 'hidden')


idTextBox = tk.Entry(root, bd=4, width = 10)
firstNameTextBox = tk.Entry(root, bd=4, width = 15)
lastNameTextBox = tk.Entry(root, bd=4, width = 15)


submitButton = tk.Button(root, text = "submit")
submitButton_window = canvas.create_window(1450, 10, anchor = "nw", window = submitButton)
submitButton.bind("<Button-1>", toggleAddStudentOff)
canvas.itemconfigure(submitButton_window, state = "hidden")

alphabetize_button = tk.Button(root, text = "alphabetical")
randomize_button = tk.Button(root, text = "randomize")
edit_seats_button = tk.Button(root, text = "edit seats")
clear_seating_chart_button = tk.Button(root, text = "clear seating chart")
edit_seats_location_button = tk.Button(root, text = "edit seat location")

alphabetize_button_window = canvas.create_window(200, 10, anchor = "nw", window = alphabetize_button)
randomize_button_window = canvas.create_window(300, 10, anchor = "nw", window = randomize_button)
edit_seats_button_window = canvas.create_window(390, 10, anchor = "nw", window = edit_seats_button)
clear_seating_chart_button_window = canvas.create_window(478, 10, anchor = "nw", window = clear_seating_chart_button)
edit_seats_location_button_window = canvas.create_window(617, 10, anchor = "nw", window = edit_seats_location_button)


alphabetize_button.bind("<Button-1>", alphabetize)
randomize_button.bind("<Button-1>", randomize)
edit_seats_location_button.bind("<Button-1>", edit_seat_locations)
clear_seating_chart_button.bind("<Button-1>", clear_seats)

root.mainloop()



