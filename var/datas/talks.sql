
-- Table: talks
CREATE TABLE talks ( 
    talk_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    post_id   INTEGER,
    user_id   INTEGER        NOT NULL
                             DEFAULT ( 0 ),
    user_ip   VARCHAR( 39 ),
    talk_ptid INTEGER        NOT NULL
                             DEFAULT ( 0 ),
    user_name VARCHAR( 64 )  COLLATE 'NOCASE',
    user_mail VARCHAR( 64 )  COLLATE 'NOCASE',
    talk_text TEXT,
    talk_rank INT( 10 )      NOT NULL
                             DEFAULT ( 100 ),
    talk_plus INT( 10 )      NOT NULL
                             DEFAULT ( 0 ),
    talk_mins INT( 10 )      NOT NULL
                             DEFAULT ( 0 ),
    talk_ctms INT( 10 )      NOT NULL,
    talk_utms INT( 10 )      NOT NULL 
);


-- Index: idx_talkRank_talkId
CREATE INDEX idx_talkRank_talkId ON talks ( 
    talk_rank,
    talk_id 
);


-- Index: idx_postId_talkRank_talkId
CREATE INDEX idx_postId_talkRank_talkId ON talks ( 
    post_id,
    talk_rank,
    talk_id 
);

