
-- Table: alogs
CREATE TABLE IF NOT EXISTS alogs ( 
    alog_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER        DEFAULT ( 0 ),
    user_ip   VARCHAR( 39 ),
    user_name VARCHAR( 64 )  COLLATE 'NOCASE',
    alog_text TEXT,
    alog_data TEXT,
    alog_ctms INT( 10 )      NOT NULL 
);
