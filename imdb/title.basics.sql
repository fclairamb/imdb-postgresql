begin;

drop table if exists title_basics;

create table title_basics (
    tconst text not null,
    titleType text not null,
    primaryTitle text not null,
    originalTitle text not null,
    isAdult text not null,
    startYear text,
    endYear text,
    runtimeMinutes text,
    genres text
);

\copy title_basics from 'imdb/title.basics.tsv' delimiter e'\t' quote e'\b' null as '\N' csv header;

alter table title_basics alter column tconst type int using substring(tconst, 3)::int;
alter table title_basics rename column tconst to id;
alter table title_basics add primary key (id);
alter table title_basics alter column isAdult type boolean using isAdult::boolean;
alter table title_basics alter column startYear type int using startYear::int;
alter table title_basics alter column endYear type int using endYear::int;
alter table title_basics alter column runtimeMinutes type int using runtimeMinutes::int;
alter table title_basics alter column genres type text[] using string_to_array(genres, ',');

select * from title_basics;

commit;
