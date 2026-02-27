import sqlite3

def login(username, password):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT PasswordHash FROM Staff WHERE UserName = ?", (username,))
    results = cursor.fetchone()
    if results == None:
        print('wrong username or password')
    else:
        if results[0] == password:
            cursor.execute(f"SELECT Name FROM Staff WHERE UserName = ?", (username,))
            results = cursor.fetchone()
            print('welcome' , results[0])

    return results[0]

class accounter():
    def __init__(self, accountName):
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        self._Name = accountName
        
        cursor.execute(f"SELECT * FROM Staff WHERE UserName = ?", (username,))
        results = cursor.fetchone()
        print(results)
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
        if int(self.returnAS()) < 1:
            cursor.execute(f"SELECT * FROM Patients WHERE Name = ?", (patientName,))
            results = cursor.fetchone()
            print(results)

username = input('username: ')
password = input('password: ')
accountName = login(username, password)
account = accounter(accountName)
patientName = input('enter patient name')
account.searchPatients(patientName)
