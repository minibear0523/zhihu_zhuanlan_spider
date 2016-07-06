# Author Table
CREATE TABLE zhihu_author (
    id serial PRIMARY KEY, 
    hash character(32) UNIQUE, 
    bio text, 
    name text, 
    slug text UNIQUE, 
    description text
);
  
# Post Table
CREATE TABLE zhihu_post (
    id serial PRIMARY KEY,
    source_url text,
    url text unique,
    title text,
    title_image text,
    summary text,
    content text,
    href text,
    slug integer unique,
    likes_count integer,
    comments_count integer,
    published_time date,
    author character(32) REFERENCES zhihu_author (hash),
    db_create_time timestamp
);