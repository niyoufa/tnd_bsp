
-- Table: mails
CREATE TABLE mails ( 
    mail_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    user_ip   VARCHAR( 39 ),
    user_name VARCHAR( 64 )  COLLATE 'NOCASE',
    user_mail VARCHAR( 64 )  NOT NULL
                             COLLATE 'NOCASE',
    mail_text TEXT,
    mail_stat INT( 1 )       DEFAULT ( 0 ),
    mail_ctms INT( 10 )      NOT NULL,
    mail_utms INT( 10 )      NOT NULL 
);


-- Index: idx_mailStat_mailId
CREATE INDEX idx_mailStat_mailId ON mails ( 
    mail_stat,
    mail_id 
);

