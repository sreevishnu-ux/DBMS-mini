import mysql.connector as mysql


def init_db():
    mydb = mysql.connect(host="localhost" , user="root" , passwd="Hanx@1" , database="antivenom",auth_plugin="mysql_native_password")
    cursor = mydb.cursor()
    cursor.execute("Use antivenom;")


    cursor.execute("""
        CREATE Table Person(
            Pid int primary key unique,
            Name varchar(20),
            Age int,
            City varchar(20),  
            District varchar(20),
            State varchar(20),
            Snake_type varchar(30),
            Snake_colour varchar(20)
        );
    """)
    mydb.commit()
   

init_db()
    
