import sqlite3

class db:
    def __init__(self, db):
        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone VARCHAR(20), client VARCHAR(3), choice TEXT, pack TEXT, send TEXT, sendDate TEXT, wishes TEXT, status TEXT);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS phoneNumbers (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, username VARCHAR(50), phoneNumber VARCHAR(20), status TEXT)')
        self.connection.commit()

    def phoneBook(self, userID, username, phoneNumber, status):
        cursor = self.cursor.execute('SELECT * FROM phoneNumbers WHERE (userID=? AND username=? AND phoneNumber=? AND status=?)', (userID, username, phoneNumber, status))
        entry = cursor.fetchone()
        if entry is None:
            self.cursor.execute("INSERT INTO phoneNumbers (userID, username, phoneNumber, status) VALUES (?, ?, ?, ?)", (userID, username, phoneNumber, status))
            self.connection.commit()
        self.cursor.execute('SELECT * FROM phoneNumbers ORDER BY id DESC LIMIT 1;')
        print(self.cursor.fetchone())

    def requestDb(self, name, email, phone, client, choice, pack, send, sendDate, wishes, status):
        cursor = self.connection.execute('SELECT * FROM Users WHERE (name=? AND email=? AND phone=? AND client=? AND choice=? AND pack=? AND send=? AND sendDate=? AND wishes=? AND status=?)', (name, email, phone, client, choice, pack, send, sendDate, wishes, status))
        entry = cursor.fetchone()
        if entry is None:
            self.cursor.execute('INSERT INTO Users (name, email, phone, client, choice, pack, send, sendDate, wishes, status) VALUES (?,?,?,?,?,?,?,?,?,?)', (name, email, phone, client, choice, pack, send, sendDate, wishes, status))
            self.connection.commit()

        self.cursor.execute('SELECT * FROM Users ORDER BY id DESC LIMIT 1;')
        print(self.cursor.fetchone())         

        #self.connection.commit()

    def getNpRequests(self):
        cursor = self.connection.execute('SELECT id, name, email, phone, choice, status FROM Users WHERE status = "не обработана" OR status LIKE "в обработке%" ORDER BY id;')
        return list(cursor.fetchall())

    def getNpCalls(self):
        cursor = self.connection.execute('SELECT id, username, phoneNumber, status FROM phoneNumbers WHERE status = "не обработан" OR status LIKE "в обработке%" ORDER BY id;')
        return list(cursor.fetchall())

    def setProcessRequest(self, id, empId):
        status = "В обработке; " + str(empId)
        cursor = self.connection.execute('UPDATE Users SET status = "' + status + '" WHERE id = "' + str(id) + '"')
        self.connection.commit()

    def setProcessCall(self, id, empId):
        status = "В обработке; " + str(empId)
        cursor = self.connection.execute('UPDATE phoneNumbers SET status = "' + status + '" WHERE id = "' + str(id) + '"')
        self.connection.commit()

    def cancelProcessRequest(self, id):
        cursor = self.connection.execute('UPDATE Users SET status = "не обработана" WHERE id = "' + str(id) + '"')
        self.connection.commit()

    def cancelProcessCall(self, id):
        cursor = self.connection.execute('UPDATE phoneNumbers SET status = "не обработан" WHERE id = "' + str(id) + '"')
        self.connection.commit()

    def setFinishedRequest(self, id):
        cursor = self.connection.execute('UPDATE Users SET status = "обработана" WHERE id = "' + str(id) + '"')
        self.connection.commit()

    def setFinishedCall(self, id):
        cursor = self.connection.execute('UPDATE phoneNumbers SET status = "обработан" WHERE id = "' + str(id) + '"')
        self.connection.commit()
    
    def __del__(self):
        self.connection.close()
