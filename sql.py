import mysql.connector
from datetime import date, datetime, timedelta
import random
import string

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_passowrd",
    database="BOOKAIR"
)


# Function to check for an available user ID
def check_user_id(data):
    # Recursive function to check for an available user ID
    new = data
    cursor = mydb.cursor()
    query = "SELECT * FROM PASSENGERINFO WHERE U_ID = %s"
    value = (data,)
    cursor.execute(query, value)
    result = cursor.fetchall()
    if len(result) != 0:
        new += 1
        return check_user_id(new)
    return new

# Function to check for available username
def check_username():
    # Check for available username and prevent duplicates
    data = input("ENTER USERNAME: ")
    cursor = mydb.cursor()
    query = "SELECT * FROM PASSENGERINFO WHERE USER = %s"
    value = (data,)
    cursor.execute(query, value)
    result = cursor.fetchall()
    if len(result) != 0:
        print("USERNAME ALREADY EXISTS")
        return check_username()
    return data

# Function to register a new user
def query_register(data):
    # Register a new user and insert into database
    user_id = check_user_id(data[0])
    cursor = mydb.cursor()
    value = (user_id, data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    cursor.execute("""
           INSERT INTO BOOKAIR.PASSENGERINFO 
           (U_ID,FULLNAME,USER,PASSWORD,GENDER,NATIONALITY,DOB,PHONE)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", value)
    mydb.commit()
    cursor.close()
    print("REGISTRATION SUCCESSFUL")

# Function to log in a user
def query_login(data):
    # Login a user and retrieve user information
    cursor = mydb.cursor()
    cursor.execute("""
                SELECT 
                    * 
                FROM BOOKAIR.PASSENGERINFO
                WHERE 
                     USER = %s AND PASSWORD = %s""", data)
    result = cursor.fetchall()
    if len(result) == 0:
        print('ACCOUNT DOES NOT EXIST')
    else:
        print('\n\n')
        for x in result:
            print("WELCOME:", str(x[1]) +
                  "\nUSER ID: " + str(x[0]) +
                  "\n|USER: " + str(x[2]) +
                  "\n|PASSWORD: " + str(x[3]) +
                  "\n|GENDER: " + str(x[4]) +
                  "\n|NATIONALITY: " + str(x[5]) +
                  "\nDOB: " + str(x[6]) +
                  "\nPHONE: " + str(x[7]))
            print('\n')
        print('\n\n')
    table_name = "User_" + str(result[0][1]) + "_" + str(result[0][0])  # Correctly format table name
    table_name_escaped = '`' + table_name + '`'  # Escape table name
    create_table_query = """
        CREATE TABLE IF NOT EXISTS %s (
            FLIGHT_NO INTEGER,
            DATE_BOOKED DATE,
            PASSENGER_NAME VARCHAR(30),
            PASSENGER_AGE INTEGER,
            PASSENGER_GENDER VARCHAR(200)
        )
    """ % table_name_escaped
    cursor.execute(create_table_query)
    mydb.commit()
    cursor.close()
    return result[0][0]

# Function to search for available flights
def query_search_flight(data, data2):
    # Search for available flights based on departure and arrival cities
    cursor = mydb.cursor()
    cursor.execute("""
                   SELECT 
                       * 
                   FROM BOOKAIR.SEARCHFLIGHTS
                   WHERE 
                       DEPARTURE = %s AND ARRIVAL = %s""", data)
    result = cursor.fetchall()
    if len(result) == 0:
        print('NO FLIGHTS AVAILABLE')
    else:
        print('\n\n')
        for x in result:
            print("FLIGHT_NO", str(x[0]) +
                  "\nDATE " + str(x[1]) +
                  "\nDEPARTURE " + str(x[2]) +
                  "\n|ARRIVAL " + str(x[3]) +
                  "\nSEATS AVAILABLE " + str(x[4]) +
                  "\nFARE " + str(x[5]))
            print('\n')
        print('\n\n')
        mydb.commit()
        cursor.close()

    if data2 == 0:
        book = input("DO YOU WANT TO BOOK (Y/N): ")
        if book == "Y":
            flight_id = int(input("ENTER THE FLIGHT NO TO BOOK: "))
        else:
            print("THANK YOU>>>VISIT AGAIN")
            flight_id = 0
    else:
        flight_id = 0
    return flight_id

# Function to book a flight
def query_book_flight(book_data, no_tick):
    # Book a flight for the user and update database
    cursor = mydb.cursor()
    user_id = int(book_data[0])
    flight_id = int(book_data[1])
    cursor.execute("SELECT FULLNAME FROM BOOKAIR.PASSENGERINFO WHERE U_ID = %s" % user_id)
    result = cursor.fetchone()
    dat1 = result[0]
    cursor.execute("SELECT FARE FROM BOOKAIR.SEARCHFLIGHTS WHERE FLIGHT_NO = %s" % flight_id)
    result = cursor.fetchone()
    dat2 = int(result[0])
    total_fare = 0
    today = str(date.today())
    table_name = dat1 + str(user_id)
    for k in range(no_tick):
        total_fare += dat2
        pass_name = input('ENTER THE PASSENGER NAME: ')
        pass_age = int(input('ENTER THE PASSENGER AGE: '))
        pass_gender = input('ENTER PASSENGER GENDER (F,M): ')
        t = (flight_id, today, pass_name, pass_age, pass_gender)
        query = "INSERT INTO BOOKAIR.`%s`" % table_name + "(FLIGHT_NO, DATE_BOOKED, PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, t)
        query = "UPDATE BOOKAIR.SEARCHFLIGHTS SET SEATS_AVAIL = SEATS_AVAIL - 1 WHERE FLIGHT_NO = %s"
        s = (flight_id,)
        cursor.execute(query, s)
    mydb.commit()
    cursor.close()
    return total_fare

# Function to process payment
def query_payment(ticket_no, user_id, total_fare):
    # Process payment for booked tickets and update database
    card = int(input("ENTER YOUR CARD NUMBER: "))
    expiry_date = datetime.strptime(input("ENTER EXPIRY DATE (MM/DD/YYYY): "), '%m/%d/%Y').date()
    cursor = mydb.cursor()
    query = "INSERT INTO BOOKAIR.PAYMENT VALUES(%s, %s, %s, %s, %s)"
    values = (ticket_no, user_id, card, expiry_date, total_fare)
    cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    print("PAYMENT SUCCESSFUL")

# Function to check booking history
def check_history(data):
    # Check booking history for a user
    cursor = mydb.cursor()
    query = "SELECT FULLNAME, U_ID FROM PASSENGERINFO WHERE USER = %s"
    value = (data,)
    cursor.execute(query, value)
    result = cursor.fetchall()
    table_name = str(result[0][0]) + str(result[0][1])
    try:
        query = "SELECT * FROM %s" % table_name
        cursor.execute(query)
        result = cursor.fetchall()
        for x in result:
            print("PASSENGER NAME:", x[2])
            print("DATE BOOKED:", x[1])
            print("FLIGHT_NO:", x[0])
    except mysql.connector.Error as err:
        print("No booking history found.")
    finally:
        cursor.close()
