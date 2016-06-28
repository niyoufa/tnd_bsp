
-- Table: files
CREATE TABLE files ( 
    file_id   INTEGER         PRIMARY KEY AUTOINCREMENT,
    file_hash CHAR( 32 ),
    file_base VARCHAR( 128 ),
    file_path VARCHAR( 512 ),
    file_type VARCHAR( 128 ),
    file_memo VARCHAR( 512 ),
    file_ctms INT( 10 )       NOT NULL 
);
