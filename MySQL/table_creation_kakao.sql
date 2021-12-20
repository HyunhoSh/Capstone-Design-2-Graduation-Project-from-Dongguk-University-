-- drop database userdb;

CREATE DATABASE userdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;

create database userdb;
use userdb;

create table User(
   user_id varchar(20) not null unique primary key,
   user_name varchar(20) not null,
   user_pw varchar(20) not null,
   is_patient int not null,
   age int not null,
   weight float not null,
   height float not null,
   birth_date varchar(30) not null,
   gender varchar(7) not null,
   illness varchar(100),
   medicine varchar(100),
   phone_number varchar(40),
   doctor_in_charge varchar(20)
);

insert into User values ('hhshin98','신현호','123',1,24,80,176,'1998-11-25','male','X','X','01048807780','doctor');
insert into User values ('doctor','현호신','123',0,42,85,174,'1998-11-25','male','X','X','01048807780',null);
insert into User values ('hhsh8787','홍길동','123',1,24,80,176,'1992-11-25','male','X','X','01048807780','doctor');
select * from User;
create table Solution(
   solution_id int not null unique,
   solution varchar(300),
   solution_mealtime varchar(20),
   solution_date varchar(20),
   user_id varchar(20),
   primary key(solution_id)
);
insert into Solution values (1234,'염분 줄이기','점심','2021-11-14','hhshin98');



create table Diet(
    diet_id int(11) primary key,
    foods varchar(255),
    image varchar(1500),
    date varchar(50),
    mealtime varchar(10),
    user_id varchar(20),
    solution_id int(11)
);
-- insert into Diet values (1234, '쌀밥, 제육볶음','https://www.google.com/imgres?imgurl=https%3A%2F%2Fnews.kbs.co.kr%2Fdata%2Fnews%2F2017%2F01%2F04%2F3405677_bH6.jpg&imgrefurl=https%3A%2F%2Fnews.kbs.co.kr%2Fnews%2Fview.do%3Fncd%3D3405677&tbnid=o-NvJWR3wUZo9M&vet=12ahUKEwjj3JyHrIv0AhWtQPUHHZqUCPcQMygAegUIARCqAQ..i&docid=Suc0OJSJnld1AM&w=596&h=335&q=%EC%9D%8C%EC%8B%9D%20%EC%82%AC%EC%A7%84&ved=2ahUKEwjj3JyHrIv0AhWtQPUHHZqUCPcQMygAegUIARCqAQ','20200908','점심','12',53);
-- alter table Save_diet modify image varchar(255);  -- image 링크 받는 것으로 바꿈
-- alter table Save_diet modify photo_time varchar(25);
-- -- alter table Save_diet
insert into Diet values (1234, '쌀밥, 제육볶음', 'https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA5MjJfNjUg%2FMDAxNjMyMzIxMTExNjc5.S2DRWaGbM9blMfXTC-5px7TqOZKiok64NuO5WNf_jBEg.CeVTljFBYUUhAfuEvOy-eGOucV6VWeY1uJSkuYRUDmwg.JPEG.f6341138%2F9%25BF%25F916%25C0%25CF_%25C1%25A1%25BD%25C9.jpg&type=a340','2021-11-15','아침','hhshin98',1323);
insert into Diet values (1232, '가지나물, 감', 'https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMTA3MDFfMjMy%2FMDAxNjI1MTM1MzkwNDA2.KCkC4OhbNW92h9_07dNGKGO7vKPOM_LE9umbMTD1BTcg.iDMvaVfS5Biu25c-wCyk-MY_tm8jwqATWeua8OI0DqAg.JPEG%2FexternalFile.jpg&type=a340','2021-11-15','점심','hhshin98',1322);
insert into Diet values (1231, '고등어조림, 곰탕', 'https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMTEwMjFfMTQ4%2FMDAxNjM0ODA2MzU4NzE2.6y8_daoxmZ-MOeg2e6v1-3WB4Fm1DcOZuWZHSXSLKi0g.rRu-dZZBRswa8oYthb14ZopO8fc-XMXFAugg7YrX55Mg.JPEG%2FexternalFile.jpg&type=a340','2021-11-15','저녁','hhshin98',1320);
 
create table Nutrient(
   food_name varchar(40) primary key,
   calories float,
   carbohydrate float,
   protein float,
   fat float,
   sodium float,
   calcium float,
   vitamin_c float,
   saturated_fat float
);

-- select * from Nutrient;

-- 질문이 5개라 가정
create table Query(
   query_id varchar(20) not null unique primary key,
   user_id varchar(20) not null unique,
   answer_01 varchar(100) not null,
   answer_02 varchar(100) not null,
   answer_03 varchar(100) not null,
   answer_04 varchar(100) not null,
   answer_05 varchar(100) not null,
   foreign key(user_id) references User(user_id)
);
insert into Query values (23455, '12','2','2','3','4','6');
-- insert into Query_patient values ('qr1024000','12','1','3','4','2','2');
-- select * from Query_patient;
create table Food(
   food_type varchar(40) primary key,
   choice_01 varchar(10),
   choice_02 varchar(10),
   choice_03 varchar(10),
   unit varchar(50)
);

select * from Diet;
select * from Food;
select * from Nutrient;

alter table Diet add calories float;
alter table Diet add carbohydrate float;
alter table Diet add protein float;
alter table Diet add fat float;
alter table Diet add sodium float;
alter table Diet add calcium float;
alter table Diet add vitamin_c float;
alter table Diet add saturated_fat float;



