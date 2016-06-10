# Author Table
CREATE TABLE author (
    id serial PRIMARY KEY, 
    hash character(32) UNIQUE, 
    bio text, 
    name text, 
    slug text UNIQUE, 
    desc text
);
  
# Post Table
CREATE TABLE post (
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
    author character(32) REFERENCES author (hash)
);