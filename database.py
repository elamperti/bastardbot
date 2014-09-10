import sqlite3

class BastardSQL():
    def __init__(self, filename='bastard.db'):
        self.messages_per_page = 20
        self.changed = False
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.changed:
            self._commit()
        self.conn.close()

    def _populate(self):
        """Populates bastard.db using bastard.sql"""
        f = open('bastard.sql', 'r')
        sql = f.read()
        self.cursor.executescript(sql)
        f.close()

    def _commit(self):
        """Write last operations in the database"""
        self.conn.commit()
        self.changed = False

    def get_conversations(self):
        """Returns an iterable list of conversations"""
        return self.cursor.execute("SELECT * FROM [Conversations]")

    def get_conversation(self, conv_id):
        """Returns a single conversation if found"""
        query = "SELECT * FROM [Conversations] WHERE [conv_id] = ?"
        result = self.cursor.execute(query, (conv_id,))
        return result.fetchone()

    def put_conversation(self, conv_id, conv_name, participants):
        """Inserts a conversation in the Conversations table, returns the conv_id"""
        query = "INSERT INTO [Conversations] ([conv_id], [conv_name], [participants]) VALUES (?, ?, ?)"
        self.cursor.execute(query, (conv_id, conv_name, participants))
        row_id = self.cursor.lastrowid
        self.changed = True
        return row_id

    def get_messages(self, conv_id=0, msg_type=0, page=0):
        """Returns an iterable list of messages"""
        
        # FIXME: this should be sanitized.
        conditions = []
        if conv_id > 0:
            conditions.append("msg_conv_id = {}".format(conv_id))
        if msg_type > 0:
            conditions.append("msg_type = {}".format(msg_type))

        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        if page > 0:
            page_lbound = page * self.messages_per_page
            page_ubound = page_lbound + self.messages_per_page
            limit = " LIMIT {},{}".format(page_lbound, page_ubound)
        else:
            limit = ""

        query = "SELECT * FROM [Messages]" + where + " ORDER BY [msg_timestamp] DESC" + limit
        return self.cursor.execute(query)

    def put_message(self, conv_id, message, author, timestamp, msg_type=1):
        """Inserts a message in the Messages table, returns the row ID"""
        query = "INSERT INTO [Messages] ([msg_conv_id], [msg_content], [msg_author_id], [msg_timestamp], [msg_type]) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (conv_id, message, author, timestamp, msg_type))
        self.changed = True
        return self.cursor.lastrowid

    def get_authors(self):
        """Returns all the authors"""
        query = "SELECT * FROM [Authors]"
        return  self.cursor.execute(query)

    def get_author(self, author_gaia_id):
        """Returns a single author"""
        query = "SELECT * FROM [Authors] WHERE [author_id] = ?"
        result = self.cursor.execute(query, (author_gaia_id,))
        return result.fetchone()

    def put_author(self, author_gaia_id, author_name):
        """Adds an author to the Authors table"""
        # FIXME: check if it exists before inserting it blindly.
        query = "INSERT INTO [Authors] ([author_id], [author_name]) VALUES (?, ?)"
        self.cursor.execute(query, (author_gaia_id, author_name))
        self.changed = True 
        return self.cursor.lastrowid

    def add_tags(self, msg_id, author, tags):
        """Adds tags to a message"""
        added_tags_count = 0
        for tag in tags:
            tag_id = self._get_tag_id(tag)
            print ("TAG_ID {}".format(tag_id))
            if tag_id is None:
                self.cursor.execute("INSERT INTO [Tags] (tag_name) VALUES (?)", (tag,))
                tag_id = self.cursor.lastrowid
                added_tags_count += 1
                self.changed = True

            query = "INSERT INTO [Messages_have_Tags] (msg_id, tag_id, author_id) VALUES (?, ?, ?)"
            self.cursor.execute(query, (msg_id, tag_id, author))

        return added_tags_count

    def get_tags(self, msg_id, author=0):
        """Returns all the tags for a given message"""
        # FIXME: this is far from being pythonic.
        # FIXME: return author(id|name) column too
        query = "SELECT DISTINCT [tag_id], [tag_name] FROM [Tags] WHERE tag_id IN (SELECT [tag_id] FROM [Messages_have_Tags] WHERE msg_id=?);"
        if author == 0:
            result = self.cursor.execute(query, (msg_id,))
        else:
            query = query[:-2] + " AND author_id=?);"
            result = self.cursor.execute(query, (msg_id, author_id))
        return result

    def _get_tag_id(self, tag_name):
        """Returns the id of a tag, given its name"""
        query = "SELECT [tag_id] FROM [Tags] WHERE tag_name = ? LIMIT 1;"
        result = self.cursor.execute(query, (tag_name,))
        tag_id = result.fetchone()
        return tag_id

    def _get_tag_name(self, tag_id):
        """Returns the name of a tag, given its id"""
        query = "SELECT [tag_name] FROM [Tags] WHERE tag_id = ? LIMIT 1;"
        result = self.cursor.execute(query, (tag_id,))
        try:
            tag_name = result.fetchone()
        except:
            tag_name = 0
        return tag_name

    def dict_factory(self, row):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d


if __name__ == '__main__':
    print("Populating database...")
    db = BastardSQL()
    db._populate()