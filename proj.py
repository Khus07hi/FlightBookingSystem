import datetime
import random
import string
import sql

U_ID = 100
TICKET_NO = 300

# Function to display the main menu
def menu():
    print("******************************************")
    print("* WELCOME TO BOOKAIR AIRLINES           *")
    print("******************************************")
    print("* PLEASE MAKE A SELECTION:              *")
    print("*(1) SEARCH FLIGHTS                     *")
    print("*(2) BOOK A FLIGHT                      *")
    print("*(3) LOGIN/REGISTER                     *")
    print("******************************************")
    select_menu = int(input())
    return select_menu

# Function to select an option from the main menu
def selected(i):
    if i == 1:
        return search_flight(i)
    elif i == 2:
        return book_flight()
    elif i == 3:
        return log_reg(i)
    elif i == 4:
        print("THANK YOU FOR VISITING")
    else:
        print("INVALID SELECTION")

# Function to search for available flights
def search_flight(x):
    from_city = input("DEPARTURE CITY: ")
    to_city = input("ARRIVAL CITY: ")
    search_data = (from_city, to_city)
    flight_id = sql.query_search_flight(search_data, x)
    if x == 1:
        main()
    return flight_id

# Function to book a flight
def book_flight():
    global TICKET_NO
    TICKET_NO = TICKET_NO * random.randint(1, 9) + random.randint(1, 9) * random.randint(1, 9) 
    n = 0
    user_id = log_reg(n)
    flight_id = search_flight(n)
    no_tick = int(input('ENTER THE NO OF TICKETS YOU DESIRE TO BOOK: '))
    book_data = (user_id, flight_id)
    total_fare = sql.query_book_flight(book_data, no_tick)
    print("PROCEEDING TO PAYMENT>>>>")
    sql.query_payment(TICKET_NO, user_id, total_fare)
    print(total_fare)

# Function for user login or registration
def log_reg(data):
    print("1. LOGIN")
    print("2. REGISTER")
    selected = int(input())
    if selected == 1:
        return login(data)
    elif selected == 2:
        return register(data)
    else:
        print("INVALID SELECTION")

# Function to display the main menu after login/registration
def main_menu():
    print("******************************************")
    print("* PLEASE MAKE A SELECTION:              *")
    print("*(1) SEARCH FLIGHTS                     *")
    print("*(2) BOOK A FLIGHT                      *")
    print("******************************************")
    select_menu = int(input())
    selected(select_menu)

# Function for user login
def login(data):
    user = input("ENTER USERNAME: ")
    password = input("ENTER YOUR PASSWORD: ")
    log_data = (user, password)
    user_id = sql.query_login(log_data)
    if data == 3:
        history = input("DO YOU WANT TO VIEW YOUR PREVIOUS BOOKINGS (Y/N): ")
        if history == "Y":
            sql.check_history(user)
        else:
            print("THANK YOU FOR VISITING BOOKAIR AIRLINES")
            main_menu()  # Return to the main menu if the user doesn't want to view booking history
    return user_id

# Function to check gender input
def check_gender():
    gender = input("ENTER GENDER (M,F,T): ")
    if gender not in ("M", "F", "T"):
        print("ENTER VALID GENDER")
        return check_gender()
    return gender 

# Function to check phone number input
def check_phone():
    ph_no = input("PHONE NUMBER: ")
    if len(ph_no) != 10:
        print("ENTER VALID PHONE NUMBER")
        return check_phone()
    return int(ph_no)

# Function for user registration
def register(data):
    global U_ID
    U_ID += 1
    full_name = input("ENTER FULLNAME: ")
    user = sql.check_username()
    password = input("ENTER YOUR PASSWORD: ")
    gender = check_gender()
    nat = input("NATIONALITY: ")
    dob = datetime.datetime.strptime(input("ENTER YOUR DOB (MM/DD/YYYY): "), '%m/%d/%Y').date()
    ph = check_phone()
    reg_data = (U_ID, full_name, user, password, gender, nat, dob, ph)
    sql.query_register(reg_data)
    if data == 0:
        login(data)
    else:
        main()
        
# Function to display the main menu
def main():
    select_menu = menu()
    selected(select_menu)


if __name__ == "__main__":
    main()
