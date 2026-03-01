import sqlite3
from datetime import datetime
import hashlib
import time



class User:
    def __init__(self, staffID, username):
        self._staffID = staffID
        self._username = username

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Name, Speciality, AccessRights, RFIDTagID
            FROM Staff
            WHERE StaffID = ?
        """, (self._staffID,))

        result = cursor.fetchone()
        conn.close()

        if result is None:
            raise Exception("Staff member not found")

        self._name = result[0]
        self._speciality = result[1]
        self._accessRights = result[2]
        self._rfidTagID = result[3]

    def get_name(self):
        return self._name

    def get_access_level(self):
        return self._accessRights
    
    def search_patient(self, last_name):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT FirstName, LastName, Diagnosis, Stage
            FROM Patients
            WHERE LastName = ?
        """, (last_name,))

        result = cursor.fetchone()
        conn.close()

        if result is None:
            print("Patient not found.")
            return None

        first, last, diagnosis, stage = result

        self.log_action(f"Searched patient record: {first} {last}")

        print(first, last, "has a diagnosis of", diagnosis, "at stage", stage)
        return result
    
    def search_log(self):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT PatientID, FirstName, LastName
            FROM Patients
            WHERE NHSNumber = ?
        """, (input('enter NHS number: '),))
        result1 = cursor.fetchone()
        conn.close()
        
        if result1 is None:
            print("Patient not found.")
            conn.close()
            return None
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM TreatmentLog
            WHERE PatientID = ?
        """, (result1[0],))

        result = cursor.fetchone()
        conn.close()

        if result is None:
            print("Patient not found.")
            return None
        #TreatmentID, PatientID, StaffID, TreatmentID, Date, Notes = result

        self.log_action(f"Searched treatment patient record: {result1[1]} {result1[2]}")

        print(f'''Record Logs for {result1[1]} {result1[2]}: \n
Treatment Type: {result[3] } \n
Date: {result[4]} \n
Notes:
{result[5]}
''')





class Doctor(User):
    def __init__(self, staffID, username):
        super().__init__(staffID, username)

    
    def log_action(self, action_text):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO AccessLogs (StaffID, Action, Timestamp)
            VALUES (?, ?, ?)
        """, (self._staffID, action_text, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    
    def add_patient(self):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        firstName = input('first name: ')
        lastName = input('last name: ')
        DateOfBirth = input('date of birth: ')
        NHSNumber = input('NHS number ')
        RFIDTag = input('RFID tag ID: ')
        diagnosis = input('diganoiss: ')
        stage = input('stage: ')

        cursor.execute("""
            INSERT INTO Patients (FirstName, LastName, DateOfBirth, NHSNumber, RFIDTagID, Diagnosis, Stage)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (firstName, lastName, DateOfBirth, NHSNumber, RFIDTag, diagnosis, stage))
        

        conn.commit()
        conn.close()
        self.log_action(f"added patient record: {firstName} {lastName}")

    def remove_patient(self):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        NHSNumber = input('NHS Number: ')
        cursor.execute("""
            SELECT FirstName, LastName
            FROM Patients
            WHERE NHSNumber = ?
        """, (NHSNumber,))
        result = cursor.fetchone()
        print(result)
        cursor.execute("""  
            DELETE FROM Patients
            WHERE NHSNumber = ?""", (NHSNumber,))
        conn.commit()
        conn.close()
        self.log_action(f"Deleted patient record with name: {result[0]} {result[1]}")
        print("Patient deleted successfully.")


    def log_treatment(self):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        repeat = True
        while repeat:
            NHSNumber = input('NHS number ')
            cursor.execute("""
                SELECT FirstName, LastName, PatientID
                FROM Patients
                WHERE NHSNumber = ?
            """, (NHSNumber,))
            result = cursor.fetchone()

            if result != None:
                print(f"did you mean {result[0]} {result[1]}? ")
                if input('Y = yes, N = No: ') == 'Y':
                    repeat = False
        conn.commit()
        conn.close()
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        TreatmentType = input('treatmentType: ')
        Notes = input('Notes: ')
        cursor.execute("""
        INSERT INTO TreatmentLog (PatientID, StaffID, TreatmentType, Date, Notes)
        VALUES (?, ?, ?, ?, ?)
    """, (result[2], self._staffID, TreatmentType, datetime.now().isoformat(), Notes))
        conn.commit()
        conn.close()
        self.log_action(f"Treatment logged for {result[0]} {result[1]}")


            
class Nurse(User):
    def __init__(self, staffID, username):
        super().__init__(staffID, username)



def login(username, password):

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT PasswordHash FROM Staff WHERE UserName = ?", (username,))
    results = cursor.fetchone()
    password = hashlib.sha256(password.encode()).hexdigest()
    conn.commit()
    conn.close()
    if results[0] == password:
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT Name, StaffID, AccessRights FROM Staff WHERE UserName = ?", (username,))
        results = cursor.fetchone()
        conn.commit()
        conn.close()
        print('welcome' , results[0])
        return results[2], results[1], results[0]

        
    else:
        print('login error. Wrong username or password')
        return 'Nuhuh', 'Nuhuh', 'Nuhuh'


while True:
    access, result, username = login(input('Enter username: '), input('Enter password: '))
    time.sleep(2)
    for x in range(0,100):
        print()
    
    if access == 'Doctor':
        staff = Doctor(result, username)
    elif access == 'Nurse':
        staff = Nurse(result, username)
    else:
        staff = 'Nuhuh'
    if staff != 'Nuhuh':
       while True:
        if access == 'Nurse':
                operation = input('enter opperation: \n' \
                    'Search for a patient (S)\n' \
                    'Search for a appointment treatment (T) \n \n')
                if operation == 'S':
                    staff.search_patient()
                if operation == 'T':
                    staff.search_log()

        if access == 'Doctor':
                operation = input('enter opperation: ' \
                    'Add patient (A)\n' \
                    'Remove Patient (R)\n' \
                    'Log treatment (L)\n' \
                    'Search for a patient (S)\n' \
                    'Search for a appointment treatment (T)\n \n')
                if operation == 'A':
                    staff.add_patient()
                elif operation == 'R':
                    staff.remove_patient()
                elif operation == 'L':
                    staff.log_treatment()
                elif operation == 'S':
                    staff.search_patient()
                elif operation == 'T':
                    staff.search_log()

                
                    
            

