
-- Table: terms
CREATE TABLE terms ( 
    term_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    term_name VARCHAR( 64 )  NOT NULL
                             UNIQUE
                             COLLATE 'NOCASE',
    term_refc INT( 10 )      DEFAULT ( 0 ),
    term_ctms INT( 10 ) 
);
