import sqlite3


class BastardSQL():
    def __init__(self):
        self.conn = sqlite3.connect('bastard.db')
        self.cursor = self.conn.cursor()

    def _populate(self):
        """Populates bastard.db using bastard.sql"""
        f = open('bastard.sql', 'r')
        sql = f.read()
        self.cursor.executescript(sql)
        pass

    def getConversations(self):
        """Returns an iterable list of conversations"""
        return self.cursor.execute("SELECT * FROM [Conversations]")

    def getConversation(self, conv_id):
        """Returns a single conversation if found"""
        return self.cursor.execute("SELECT * FROM [Conversations] WHERE [conv_id] = ?", conv_id)

    def putConversation(self, conv_id, conv_name, participants):
        """Inserts a conversation in the Conversations table, returns the conv_id"""
        self.cursor.execute("INSERT INTO [Conversations] ([conv_id], [conv_name], [participants]) VALUES (?, ?, ?)", (
                conv_id,
                conv_name,
                participants
            ))
        return self.cursor.lastrowid

    def getMessages(self, conv_id=0):
        """Returns an iterable list of all messages (or the messages on a conversation if conv_id is defined)"""
        if conv_id > 0:
            return self.cursor.execute("SELECT * FROM [Messages] WHERE msg_conv_id = {} ORDER BY [msg_timestamp] DESC".format(conv_id))
        else:
            return self.cursor.execute("SELECT * FROM [Messages] ORDER BY [msg_timestamp] DESC".format(conv_id))

    def putMessage(self, conv_id, message, author, timestamp):
        """Inserts a message in the Messages table, returns the row ID"""
        self.cursor.execute("INSERT INTO [Messages] ([msg_conv_id], [msg_content], [msg_author_id], [msg_timestamp]) VALUES (?, ?, ?, ?)", (
                conv_id,
                message,
                author,
                timestamp
            ))
        return self.cursor.lastrowid

if __name__ == '__main__':
    print("Populating database...")
    db = BastardSQL()
    db._populate()
