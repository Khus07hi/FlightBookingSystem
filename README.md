# Airline Booking System

This project is an airline booking system developed in Python with MySQL database integration. 
This project was created for understanding basic MySQL queries.

## Features
- Search for flights
- Book tickets
- User registration and login
- View booking history

## Tables
### Predefined Tables
- **passengerinfo**: Stores user registration details.
    - *Structure*:
        - `U_ID` INT (Primary Key)
        - `FULLNAME` VARCHAR(255)
        - `USER` VARCHAR(255)
        - `PASSWORD` VARCHAR(255)
        - `GENDER` VARCHAR(1)
        - `NATIONALITY` VARCHAR(255)
        - `DOB` DATE
        - `PHONE` BIGINT
- **payment**: Stores payment information for booked tickets.
    - *Structure*:
        - `TICKET_NO` BIGINT (Primary Key)
        - `USER_ID` INT
        - `CARD_NUMBER` BIGINT
        - `EXPIRY_DATE` DATE
        - `TOTAL_FARE` DECIMAL(10, 2)
- **searchflights**: Stores information about available flights.
    - *Structure*:
        - `FLIGHT_NO` INT (Primary Key)
        - `DATE` DATE
        - `DEPARTURE` VARCHAR(255)
        - `ARRIVAL` VARCHAR(255)
        - `SEATS_AVAIL` INT
        - `FARE` DECIMAL(10, 2)

### Dynamically Created Tables
- Tables for each user dynamically created to store their booking history.
    - *Structure*:
        - Table name: `{FULLNAME}_{U_ID}`
        - Columns:
            - `FLIGHT_NO` INT
            - `DATE_BOOKED` DATE
            - `PASSENGER_NAME` VARCHAR(255)
            - `PASSENGER_AGE` INT
            - `PASSENGER_GENDER` VARCHAR(1)


### SQL Queries

1. **check_user_id(data)**:
   - *Description*: Checks if a user ID already exists in the database.
   - *SQL Query*: `SELECT * FROM PASSENGERINFO WHERE U_ID = %s`

2. **check_username()**:
   - *Description*: Checks if a username already exists in the database.
   - *SQL Query*: `SELECT * FROM PASSENGERINFO WHERE USER = %s`

3. **query_register(data)**:
   - *Description*: Registers a new user by inserting their details into the database.
   - *SQL Query*: `INSERT INTO BOOKAIR.PASSENGERINFO (U_ID,FULLNAME,USER,PASSWORD,GENDER,NATIONALITY,DOB,PHONE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)`

4. **query_login(data)**:
   - *Description*: Logs in a user by checking their username and password in the database.
   - *SQL Query*: `SELECT * FROM BOOKAIR.PASSENGERINFO WHERE USER = %s AND PASSWORD = %s`

5. **query_search_flight(data, data2)**:
   - *Description*: Searches for available flights based on the departure and arrival cities.
   - *SQL Query*: `SELECT * FROM BOOKAIR.SEARCHFLIGHTS WHERE DEPARTURE = %s AND ARRIVAL = %s`

6. **query_book_flight(book_data, no_tick)**:
   - *Description*: Books a flight for the user and updates the database with booking details.
   - *SQL Queries*:
     - `SELECT FULLNAME FROM BOOKAIR.PASSENGERINFO WHERE U_ID = %s`
     - `SELECT FARE FROM BOOKAIR.SEARCHFLIGHTS WHERE FLIGHT_NO = %s`
     - `INSERT INTO BOOKAIR.\`%s\` (FLIGHT_NO, DATE_BOOKED, PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER) VALUES (%s, %s, %s, %s, %s)`
     - `UPDATE BOOKAIR.SEARCHFLIGHTS SET SEATS_AVAIL = SEATS_AVAIL - 1 WHERE FLIGHT_NO = %s`

7. **query_payment(ticket_no, user_id, total_fare)**:
   - *Description*: Processes payment for booked tickets and updates the database.
   - *SQL Query*: `INSERT INTO BOOKAIR.PAYMENT VALUES(%s, %s, %s, %s, %s)`

8. **check_history(data)**:
   - *Description*: Checks the booking history for a user and displays it.
   - *SQL Query*: `SELECT * FROM %s` (where %s is the user's dynamically created table name)


## Usage
1. Run the `proj.py` file to start the program.
2. Follow the on-screen instructions to search for flights, book tickets, or register/login.

