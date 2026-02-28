import sqlite3

def login(username, password):
    try:
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT PasswordHash FROM Staff WHERE UserName = ?", (username,))
        results = cursor.fetchone()

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
        if int(self.returnAS()) > 1:#
            conn = sqlite3.connect("hospital.db")
            cursor = conn.cursor()
        
            cursor.execute(f"SELECT * FROM Patients WHERE LastName = ?", (patientName,))
            results = cursor.fetchone()
            try:
                print(results[1], results[2], 'has a diagnosis of', results[6], 'at stage', results[7])
            except:
                print('patient records cannot be accessed')
            

username = input('username: ')
password = input('password: ')
accountName = login(username, password)
if accountName != False:
    account = accounter(accountName)
    patientName = input('enter patient last name: ')
    account.searchPatients(patientName)
