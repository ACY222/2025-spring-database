use lab1;

# (1) 查询读者 Rose 的读者号和地址
select id, address 
from Reader 
where name = 'Rose';

# (2) 查询读者 Rose 所借阅图书的图书名和借期
select Book.name, Borrow.borrow_date
from Borrow
join Book on Borrow.book_id = Book.id
join Reader on Borrow.reader_id = Reader.id
where Reader.name = 'Rose'

# (3) 查询未借阅图书的读者姓名
select name from Reader
where id not in (select distinct reader_id from Borrow)

# (4) 查询 Ullman 所写的书的书名和单价
select name, price from Book where author = 'Ullman'

# (5) 查阅读者"李林"借阅未还的图书的图书号和书名
select Book.ID, Book.name
from Borrow
join Book on Borrow.book_id = Book.id
join Reader on Borrow.reader_id = Reader.id
where Reader.name = '李林' and borrow.return_date is NULL;

# (6) 查询借阅图书数目超过 3 本的读者姓名
select distinct Reader.name 
from Reader
join Borrow on Borrow.reader_id = Reader.id
group by reader.id having count(*) > 3;

# I am not sure
# (7) 查询没有借阅读者"李林"所借的任何一本书的读者姓名和读者号
select Reader.name, Reader.id
from Reader
where Reader.id not in (
    select distinct Borrow.Reader_id
    from Borrow
    where book_id in(
        select distinct Borrow.book_id 
        from Borrow
        join Reader on Borrow.reader_id = Reader.id
        where Reader.name = '李林'
    )
)

# (8) 查询书名中包含了 "MySQL" 的图书书名及图书号
select name, id from Book where name LIKE '%MySQL%'

# I am not sure
# (9) 查询 2021 年借阅图书数目排名前 10 名的读者号, 姓名, 年龄以及借阅图书数
select Reader.id, Reader.name, Reader.age, COUNT(*) as borrow_count
from Borrow
join Reader on Borrow.reader_id = Reader.id
where year(Borrow.borrow_date) = 2021
group by Reader.id
order by borrow_count DESC
limit 10;

# (10) 创建读者借书信息的视图, 并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数
drop view if exists ReaderBorrowInfo;
create view ReaderBorrowInfo (reader_id, reader_name, book_id, book_name, borrow_date) as
select Reader.id, Reader.name, Book.id, Book.name, Borrow.borrow_date
from Borrow
join Book on Borrow.book_id = Book.id
join Reader on Borrow.reader_id = Reader.id

select reader_id, count(distinct book_id) as distinct_book_count
from ReaderBorrowInfo
where borrow_date >= curdate() - interval 2 year
group by reader_id;
