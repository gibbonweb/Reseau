drop table if exists sites;
create table sites (
    id integer primary key autoincrement,
    shortname string not null,
    title string not null,
    url string not null
);

drop table if exists sources;
create table sources (
    id integer primary key autoincrement,
    site_id integer not null,
    medium string not null,
    url string not null,
    last_update timestamp
);

drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    source_id integer not null,
    title string not null,
    content string not null,
    url string not null,
    score integer not null
);
