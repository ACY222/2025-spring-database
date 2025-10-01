use lab1;

drop procedure if exists UpdateBookID;
delimiter //

create procedure UpdateBookID (
    in old_id char(8),
    in new_id char(8),
    out status int
)
begin
    if left(old_id, 2) = '00' then
        set status = 1;      # old id is super id
    elseif left(new_id, 2) = '00' then
        set status = 2;      # new id is super id
    elseif exists (select 1 from Book where id = new_id) then
        set status = 3;      # cannot use same id
    elseif not exists (select 1 from Book where id = old_id) then
        set status = 4;      # cannot find the book with old id
    else 
        set status = 0;
        alter table Borrow drop constraint FK_bb;
        update Book set id = new_id where id = old_id;
        update Borrow set book_id = new_id where book_id = old_id;
        alter table borrow add constraint FK_bb foreign key (book_id) references Book(id);
    end if;
end //
delimiter;

set @output = 0;
call UpdateBookID('00000000', '11111111', @output);
select @output;     # 1

set @output = 0;
call UpdateBookID('11111111', '00000000', @output);
select @output;     # 2

set @output = 0;
call UpdateBookID('b1', 'b2', @output);
select @output;     # 3

set @output = 0;
call UpdateBookID('11111111', '12345678', @output);
select @output;     # 4

set @output = 0;
call UpdateBookID('b1', '11111111', @output);
select @output;     # 0