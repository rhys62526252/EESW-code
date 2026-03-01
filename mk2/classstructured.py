import sqlite3
from datetime import datetime

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




class doctor(User):
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
class Nurse(User):
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

class Admin(User):
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
    
staff = doctor(1, 'ecarter')
staff.remove_patient()