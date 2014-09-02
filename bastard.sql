DROP TABLE IF EXISTS [Conversations];
CREATE TABLE [Conversations]
(
    [conv_id] INTEGER NOT NULL,
    [conv_name] NVARCHAR(140),
    [participants] TEXT,
    CONSTRAINT [PK_conv] PRIMARY KEY ([conv_id])
);

DROP TABLE IF EXISTS [Messages];
CREATE TABLE [Messages]
(
    [msg_id] INTEGER,
    [msg_conv_id] INTEGER NOT NULL,
    [msg_content] TEXT,
    [msg_author_id] INTEGER,
    [msg_timestamp] DATETIME,
    [msg_tags] TEXT,
    CONSTRAINT [PK_msg] PRIMARY KEY ([msg_id]),
    FOREIGN KEY ([msg_conv_id]) REFERENCES [Conversations] ([conv_id])
        ON DELETE NO ACTION ON UPDATE NO ACTION
);


CREATE UNIQUE INDEX [IPK_conv] ON [Conversations]([conv_id]);

CREATE UNIQUE INDEX [IPK_msg] ON [Messages]([msg_id]);

CREATE INDEX [IFK_msg_conv_id] ON [Messages]([msg_conv_id]);
