DROP TABLE IF EXISTS [Conversations];
CREATE TABLE [Conversations]
(
    [conv_id] VARCHAR(26) NOT NULL,
    [conv_name] NVARCHAR(140),
    [participants] TEXT,
    CONSTRAINT [PK_conv] PRIMARY KEY ([conv_id])
);

DROP TABLE IF EXISTS [Messages];
CREATE TABLE [Messages]
(
    [msg_id] INTEGER NOT NULL,
    [msg_conv_id] VARCHAR(26) NOT NULL,
    [msg_content] TEXT,
    [msg_author_id] INTEGER,
    [msg_timestamp] DATETIME,
    [msg_type] INTEGER DEFAULT 1,
    CONSTRAINT [PK_msg] PRIMARY KEY ([msg_id]),
    FOREIGN KEY ([msg_conv_id]) REFERENCES [Conversations] ([conv_id]),
    FOREIGN KEY ([msg_author_id]) REFERENCES [Authors] ([author_id]),
    FOREIGN KEY ([msg_type]) REFERENCES [Message_Types] ([type_id])
);

DROP TABLE IF EXISTS [Message_Types];
CREATE TABLE [Message_Types]
(
    [type_id] INTEGER DEFAULT 1,
    [type_name] TEXT,
    CONSTRAINT [PK_type] PRIMARY KEY ([type_id])
);

DROP TABLE IF EXISTS [Tags];
CREATE TABLE [Tags]
(
    [tag_id] INTEGER NOT NULL,
    [tag_name] TEXT,
    [tag_author_id] INTEGER,
    CONSTRAINT [PK_tags] PRIMARY KEY ([tag_id])
);

DROP TABLE IF EXISTS [Messages_have_Tags];
CREATE TABLE [Messages_have_Tags]
(
    [id] INTEGER NOT NULL,
    [msg_id] INTEGER,
    [tag_id] INTEGER,
    [author_id] INTEGER,
    CONSTRAINT [PK_messages_have_tags] PRIMARY KEY ([id]),
    FOREIGN KEY ([msg_id]) REFERENCES [Messages] ([msg_id]),
    FOREIGN KEY ([tag_id]) REFERENCES [Tags] ([tag_id]),
    FOREIGN KEY ([author_id]) REFERENCES [Authors] ([author_id])
);

DROP TABLE IF EXISTS [Authors];
CREATE TABLE [Authors]
(
    [author_id] INTEGER,
    [author_name] TEXT,
    CONSTRAINT [PK_author] PRIMARY KEY ([author_id])
);

CREATE UNIQUE INDEX [IPK_conv] ON [Conversations]([conv_id]);

CREATE UNIQUE INDEX [IPK_msg] ON [Messages]([msg_id]);

CREATE UNIQUE INDEX [IPK_type] ON [Message_Types]([type_id]);

CREATE UNIQUE INDEX [PPK_tag] ON [Tags]([tag_id]);

CREATE UNIQUE INDEX [PPK_messages_have_tags] ON [Messages_have_Tags]([id]);

CREATE UNIQUE INDEX [PPK_author] ON [Authors]([author_id]);

CREATE INDEX [IFK_msg_conv_id] ON [Messages]([msg_conv_id]);


INSERT INTO [Message_Types]([type_id], [type_name]) VALUES (1, 'Text');
INSERT INTO [Message_Types]([type_id], [type_name]) VALUES (2, 'Link');