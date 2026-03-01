import sqlite3
from datetime import datetime
def login(username, password):
    try:
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT PasswordHash FROM Staff WHERE UserName = ?", (username,))
        results = cursor.fetchone()
        password = hash(password)
        if results[0] == password:
            cursor.execute(f"SELECT Name FROM Staff WHERE UserName = ?", (username,))
            results = cursor.fetchone()
            print('welcome' , results[0])

        return results[0]
    except:
        print('login error. Wrong username or password')
        return False

class accounter():
    def __init__(self, accountName):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        self._Name = accountName
        
        cursor.execute(f"SELECT * FROM Staff WHERE UserName = ?", (username,))
        results = cursor.fetchone()
        print(results)
        self._StaffID = results[0]
        self._speciality = results[2]
        self._AccessRights = results[3]
        self._RFIDTagID = results[4]

    def returnSP(self):
        return self._speciality
    def returnAS(self):
        return self._AccessRights
    def returnRFID(self):
        return self._RFIDTagID

    def searchPatients(self, patientName):

        if int(self.returnAS()) >= 2:
            conn = sqlite3.connect("hospital.db")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT FirstName, LastName, Diagnosis, Stage
                FROM Patients
                WHERE LastName = ?
            """, (patientName,))
            
            results = cursor.fetchone()

            if results is None:
                print("Patient not found.")
                conn.close()
                return

            first, last, diagnosis, stage = results

            print(first, last, "has a diagnosis of", diagnosis, "at cancer stage", stage)

            action_text = f"Searched patient record: {first} {last}"
            timestamp = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO AccessLogs (StaffID, Action, Timestamp)
                VALUES (?, ?, ?)
            """, (self._StaffID, action_text, timestamp))

            conn.commit()
            conn.close()
 #           except:
  #              print('patient records cannot be accessed')
        else: print('Cannot access due to lack of access rights')
            



class doctor():
    
while True:
    username = input('username: ')
    password = input('password: ')
    accountName = login(username, password)
    if accountName != False:
        account = accounter(accountName)
        patientName = input('enter patient last name: ')
        account.searchPatients(patientName)
