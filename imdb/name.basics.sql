begin;
drop table if exists name_basics;

create table name_basics (
    nconst text not null,
    primaryName text not null,
    birthYear text,
    deathYear text,
    primaryProfession text,
    knownForTitles text
);

\copy name_basics from 'imdb/name.basics.tsv' delimiter e'\t' quote e'\b' null as '\N' csv header;

alter table name_basics alter column nconst type int using substring(nconst, 3)::int;
alter table name_basics rename column nconst to id;
alter table name_basics add primary key (id);
alter table name_basics alter column birthYear type int using birthYear::int;
alter table name_basics alter column deathYear type int using deathYear::int;
alter table name_basics alter column primaryProfession type text[] using string_to_array(primaryProfession, ',');
alter table name_basics alter column knownForTitles type text[] using string_to_array(knownForTitles, ',');

commit;

select * from name_basics limit 10;
