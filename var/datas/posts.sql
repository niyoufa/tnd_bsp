
-- Table: post_terms
CREATE TABLE post_terms ( 
    post_id INTEGER,
    term_id INTEGER 
);


-- Table: posts
CREATE TABLE posts ( 
    post_id      INTEGER          PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER          DEFAULT ( 0 ),
    post_title   VARCHAR( 128 ),
    post_descp   VARCHAR( 256 ),
    post_author  VARCHAR( 128 ),
    post_source  VARCHAR( 1024 ),
    post_summary TEXT,
    post_content TEXT,
    post_type    INT( 10 )        DEFAULT ( 0 ),
    post_ctms    INT( 10 )        NOT NULL,
    post_utms    INT( 10 )        NOT NULL,
    post_ptms    INT( 10 )        NOT NULL,
    post_refc    INT( 10 )        DEFAULT ( 0 ),
    post_rank    INT( 10 )        DEFAULT ( 99 ),
    post_plus    INT( 10 )        DEFAULT ( 0 ),
    post_mins    INT( 10 )        DEFAULT ( 0 ),
    post_stat    INT( 3 )         NOT NULL
                                  DEFAULT ( 0 ) 
);


-- Index: idx_postId_termId
CREATE UNIQUE INDEX idx_postId_termId ON post_terms ( 
    post_id,
    term_id 
);


-- Index: idx_userId_postPtms_postStat
CREATE INDEX idx_userId_postPtms_postStat ON posts ( 
    user_id,
    post_ptms,
    post_stat 
);


-- Index: idx_postId_postPtms_postStat
CREATE INDEX idx_postId_postPtms_postStat ON posts ( 
    post_id,
    post_ptms,
    post_stat 
);


-- Index: idx_postPtms_postStat
CREATE INDEX idx_postPtms_postStat ON posts ( 
    post_ptms,
    post_stat 
);


-- Index: idx_postPtms_postStat_postRank
CREATE INDEX idx_postPtms_postStat_postRank ON posts ( 
    post_ptms,
    post_stat,
    post_rank 
);


-- Index: idx_postPtms_postStat_postRefc
CREATE INDEX idx_postPtms_postStat_postRefc ON posts ( 
    post_ptms,
    post_stat,
    post_refc 
);

