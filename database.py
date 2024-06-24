import mysql.connector

def resetDatabase():

    for i, file in enumerate(files):
        fileRead = open(file, "r")
        period = periods[i]
        data = fileRead.read()
        totalStudents = data.split("\n")
        students = []

        cursor.execute("TRUNCATE " + period)
        for place in totalStudents:
            if place.split("\t")[0] == "Perm ID":
                continue
            students.append(place.split("\t"))

        for student in students:
            id = student[0]
            #name = student[4].split(", ")
            firstName = student[9]
            lastName = student[10]
            
        
            sql = "INSERT INTO " + period + " (id, first_name, last_name) VALUES (%s, %s, %s)"
            val = (id, firstName, lastName)
            cursor.execute(sql, val)
            studentdb.commit()

        # cursor = studentdb.cursor()
        cursor.execute("SELECT * FROM " + period)
        result = cursor.fetchall()
        for x in result:
            print(x)
        #print(students)

def addStudent(id, firstName, lastname, period, cursor):
    sql = "INSERT INTO " + period + " (id, first_name, last_name) VALUES (%s, %s, %s)"
    val = (id, firstName, lastname)
    cursor.execute(sql, val)
    studentdb.commit()

def dropStudent(id, period, cursor):
    sql = "DELETE FROM " + period + " WHERE id = " + "'" + str(id) + "'"
    cursor.execute(sql)
    studentdb.commit()
    

#database info
studentdb = mysql.connector.connect(
    host = "localhost",
    user = "josh",
    password = "password",
    database="students"
)

cursor = studentdb.cursor()

files = ["1st hour.txt", "2nd hour.txt", "3rd hour.txt", "6th hour.txt", "7th hour.txt"]
periods = ["first_hour", "second_hour", "third_hour", "sixth_hour", "seventh_hour"]


# dropStudent(300469, 'second_hour', cursor)
# dropStudent(292211, 'second_hour', cursor)
#dropStudent(309767, 'seventh_hour', cursor)
#addStudent(401310, 'Ruben', 'Adorno', 'second_hour', cursor)



cursor.execute("SELECT * FROM " + "third_hour")
result = cursor.fetchall()
for x in result:
    print(x)


    
    