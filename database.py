import mysql.connector

# def resetDatabase():

#     for i, file in enumerate(files):
#         fileRead = open(file, "r")
#         period = periods[i]
#         data = fileRead.read()
#         totalStudents = data.split("\n")
#         students = []

#         cursor.execute("TRUNCATE " + period)
#         for place in totalStudents:
#             if place.split("\t")[0] == "Perm ID":
#                 continue
#             students.append(place.split("\t"))

#         for student in students:
#             id = student[0]
#             firstName = student[9]
#             lastName = student[10]
            
        
#             sql = "INSERT INTO " + period + " (id, first_name, last_name) VALUES (%s, %s, %s)"
#             val = (id, firstName, lastName)
#             cursor.execute(sql, val)
#             studentdb.commit()

#         cursor.execute("SELECT * FROM " + period)
#         result = cursor.fetchall()
#         for x in result:
#             print(x)

def addStudent(id, firstName, lastname, period, cursor):
    sql = "INSERT INTO " + period + " (id, first_name, last_name) VALUES (%s, %s, %s)"
    val = (id, firstName, lastname)
    cursor.execute(sql, val)
    studentdb.commit()

def dropStudent(id, period, cursor):
    sql = "DELETE FROM " + period + " WHERE id = " + "'" + str(id) + "'"
    cursor.execute(sql)
    studentdb.commit()
    
def initSeats():
    seats = ['1A', '1B', '1C', '1D',
         '2A', '2B', '2C', '2D',
         '3A', '3B', '3C', '3D',
         '4A', '4B', '4C', '4D',
         '5A', '5B', '5C', '5D',
         '6A', '6B', '6C', '6D',
         '7A', '7B', '7C', '7D',
         '8A', '8B', '8C', '8D',
         '9A', '9B', '9C', '9D']

    for seat in seats:
        sql = "INSERT INTO seats (seat_number) VALUES (%s)"
        val = (seat,)
        cursor.execute(sql, val)
        studentdb.commit()

def sampleStudents():
    files = ["1st hour.txt", "2nd hour.txt", "3rd hour.txt", "6th hour.txt", "7th hour.txt"]
    periods = ["first_hour", "second_hour", "third_hour", "sixth_hour", "seventh_hour"]
    
    for i, file in enumerate(files):
        fileRead = open(file, "r")
        period = periods[i]
        data = fileRead.read()
        totalStudents = data.split("\n")
        students = []
        
        cursor.execute("TRUNCATE " + period)
        for place in totalStudents:
            if place != '':
                students.append(place.split("\t"))

        for student in students:
            id = student[0]
            firstName = student[1]
            lastName = student[2]
            addStudent(id, firstName, lastName, period, cursor)

#database info
studentdb = mysql.connector.connect(
    host = "localhost",
    user = "seating_chart",
    password = "48UhdZH8AmGBCc",
    database="students"
)

cursor = studentdb.cursor()


# sampleStudents()


# cursor.execute("SELECT * FROM " + "first_hour")
# result = cursor.fetchall()
# for x in result:
#     print(x)


    
    