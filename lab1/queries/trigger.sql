use lab1;

drop trigger if exists after_borrow;
drop trigger if exists after_return;

delimiter //
create trigger after_borrow after insert on Borrow for each row
begin
    if new.return_date is null then
        update Book set status = 1, times = times + 1 where id = new.book_id;
    end if;
end //
delimiter;

delimiter //
create trigger after_return after update on Borrow for each row
begin
    if new.return_date is not null then
        update Book set status = 0 where id = new.book_id;
    end if;
end //
delimiter;

select status, times from Book where id = 'b9';
insert into Borrow value('b9', 'r19', '2023-4-25', null);
select status, times from Book where id = 'b9';
update Borrow set return_date = '2024-4-25' where book_id = 'b9' and reader_id = 'r19';
select status, times from Book where id = 'b9';
