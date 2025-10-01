create database if not exists lab1;
use lab1;

# create all tables
drop table if exists Book, Reader, Borrow;
create table Book (
    id char(8) primary key,
    name varchar(10) not null,
    author varchar(10),
    price float,
    status int default 0,
    times int default 0
);

create table Reader (
    id char(8) primary key,
    name varchar(10),
    age int,
    address varchar(20)
);

create table Borrow (
    book_id char(8),
    reader_id char(8),
    borrow_date date,
    return_date date,
    constraint FK_bb foreign key (book_id) references Book(id),
    constraint FK_rr foreign key (reader_id) references Reader(id),
    primary key (book_id, reader_id)
);
