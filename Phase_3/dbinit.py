from db import init_db
import mysql.connector as mysql

db1 = mysql.connect(host="127.0.0.1", user="root", passwd="12341234", database="swapGame_team024_spr22_schema")
cursor = db1.cursor()

cursor.execute(
	        '''
	DROP DATABASE IF EXISTS	swapGame_team024_spr22_schema;
	CREATE DATABASE swapGame_team024_spr22_schema;
	USE swapGame_team024_spr22_schema;
	CREATE TABLE address (
		postal_code varchar(5) NOT NULL, 
		city varchar(60) NOT NULL, 
		state varchar(60) NOT NULL, 
		longitude decimal(11,8) NOT NULL, 
		latitude decimal(10,8) NOT NULL, 
		PRIMARY KEY (postal_code)
	);
	insert into address values('10001', 'manhattan', 'ny',34.831242,38.831242);
	insert into address values('20001', 'dc', 'md',45.831242,48.831242);
	insert into address values('30001', 'frankfort', 'ky',56.831242,59.831242);
	insert into address values('40001', 'salt lake city', 'ut',67.831242,70.831242);
	insert into address values('40002', 'ugden', 'ut',68.831242,98.831242);
	CREATE TABLE user (
		email varchar(250) NOT NULL,
		password varchar(60) NOT NULL,
		nickname varchar(100) NOT NULL,
		first_name varchar(100) NOT NULL,
		last_name varchar(100) NOT NULL,
		postal_code varchar(5) NOT NULL, 
		PRIMARY KEY (email),
		KEY (postal_code),
	    CONSTRAINT user_postal_code FOREIGN KEY (postal_code) REFERENCES address (postal_code) ON UPDATE CASCADE
	);
	insert into user values('ebad@gmail.com', '1234', 'eh','Ebad','Honarvar','10001');
	insert into user values('kyle@gmail.com', '1234', 'kl','Kyle','Lee','20001');
	insert into user values('rick@gmail.com', '1234', 'rc','Rick','Chen','30001');
	insert into user values('willie@gmail.com', '1234', 'wt','Willie','Townes','40001');
	insert into user values('chris@gmail.com', '1234', 'ca','Chris','Anthony','10001');
	CREATE TABLE phone (
		phone_number char(12)  NOT NULL,
	    email varchar(250) NOT NULL, 
		phone_type varchar(100) NULL,
		is_shared boolean NOT NULL, 
		PRIMARY KEY (phone_number),  
		KEY (email),  
	    constraint phone_user_email foreign key (email) references user (email) on update cascade
	);
	insert into phone values('646-222-1111','ebad@gmail.com','mobile', 1);
	insert into phone values('720-666-0022','kyle@gmail.com', null, 0);
	insert into phone values('512-999-0123', 'rick@gmail.com','home', 1);
	insert into phone values('858-555-0058','willie@gmail.com', 'work', 1);
	insert into phone values('999-333-8888','chris@gmail.com', 'work', 0);
	CREATE TABLE item (
		item_number int(16)  NOT NULL AUTO_INCREMENT,
		email varchar(250) NOT NULL,
		title varchar(250) NOT NULL,
		item_condition varchar(250) NOT NULL,
		item_description varchar(1000) NULL,
		PRIMARY KEY (item_number),
		KEY item_user_email_idx (email),
	    constraint item_user_email foreign key (email) references user (email) ON UPDATE CASCADE
	);
	insert into item values (1,'ebad@gmail.com','fifa 2022','good','best game ever');
	insert into item values (2,'ebad@gmail.com','fifa 2020','very good',null);
	insert into item values (3,'kyle@gmail.com','call of duty','bad',null);
	insert into item values (4,'rick@gmail.com','total war','good',null);
	insert into item values (5,'rick@gmail.com','total war_2','good',null);
	insert into item values (6,'willie@gmail.com','sonic the hedgehog','very good',null);
	insert into item values (7,'willie@gmail.com','mouse trap','bad',null);
	insert into item values (8,'kyle@gmail.com','puzzle','very bad','such a fun game');
	insert into item values (9,'rick@gmail.com','total war_3',' bad','such a fun game');
	insert into item values (10,'willie@gmail.com','sonic the hedgehog_2','very good',null);
	insert into item values (11,'willie@gmail.com','sonic the hedgehog_3','very good',null);
	insert into item values (12,'kyle@gmail.com','sonic the hedgehog_4','very good',null);
	insert into item values (13,'ebad@gmail.com','fifa 2018','very good',null);
	insert into item values (14,'ebad@gmail.com','NBA','good',null);
	insert into item values (15,'chris@gmail.com','battle field','good',null);
	insert into item values (16,'rick@gmail.com','battle field_2','good',null);
	insert into item values (17,'kyle@gmail.com','mortal combat','good',null);
	insert into item values (18,'willie@gmail.com','mario','very good',null);
	insert into item values (19,'ebad@gmail.com','fifa 2022','good','best game ever');
	insert into item values (20,'kyle@gmail.com','fifa 2018','very good','best game ever');
	insert into item values (21,'willie@gmail.com','fifa 2019','good','best game ever');
	insert into item values (22,'rick@gmail.com','fifa 2012','very good','very fun');
	insert into item values (23,'ebad@gmail.com','fifa 2013','bad','too fun');
	insert into item values (24,'chris@gmail.com','puzzle 1000','bad','too fun');
	insert into item values (25,'rick@gmail.com','total war_2','good','so amusing');
	CREATE TABLE board_game (
		item_number int(16) not null, 
	    KEY (item_number), 
	    constraint board_game_item_number foreign key (item_number) references item (item_number) on update cascade
	);
	insert into board_game values (21);
	insert into board_game values (15);
	CREATE TABLE card_game (
		item_number int(16) not null, 
	    KEY (item_number), 
	    constraint card_game_item_number foreign key (item_number) references item (item_number) on update cascade
	);
	insert into card_game values (19);
	CREATE TABLE computer_game (
		item_number int(16) NOT NULL, 
		os varchar(60) NOT NULL,
		KEY computer_item_number_idx (item_number), 
	    constraint computer_item_number foreign key (item_number) references item (item_number) on update cascade
	);
	insert into computer_game values (1,'mac');
	insert into computer_game values (22,'linux');
	CREATE TABLE video_platform (
	    type varchar(60) NOT NULL,
	    primary key (type)
		);
	insert into video_platform values ('Xbox');
	insert into video_platform values ('PlayStation');
	insert into video_platform values ('Nintendo');
	CREATE TABLE video_game (
		item_number int(16) NOT NULL, 
	    platform_type varchar(60) NOT NULL,
	    media varchar(60) NOT NULL,
	    KEY (platform_type), 
	    constraint video_game_platform foreign key (platform_type) references video_platform (type) on update cascade,
		KEY (item_number), 
	    constraint video_game_item_number foreign key (item_number) references item (item_number) on update cascade
	);
	insert into video_game values (6,'PlayStation','optical disk');
	insert into video_game values (23,'Xbox','optical disk');
	insert into video_game values (20,'Nintendo','optical disk');
	CREATE TABLE jigsaw (
		item_number int(16) NOT NULL,
	    piece_count int(16) NOT NULL,
		KEY (item_number), 
	    constraint jigsaw_item_number foreign key (item_number) references item (item_number) on update cascade
	);
	insert into jigsaw values (8,600);
	insert into jigsaw values (24,1000);
	CREATE TABLE swap (
	    item_number_pro int(16) NOT NULL,
	    item_number_counter int(16) NOT NULL,
		swap_status varchar(60) NOT NULL,
	    propose_date date NOT NULL,
		KEY (item_number_pro), 
	    KEY (item_number_counter), 
	    constraint swap_item_number_pro foreign key (item_number_pro) references item (item_number) on update cascade,
		constraint swap_item_number_counter foreign key (item_number_counter) references item (item_number) on update cascade
	);
	insert into swap values(12,11,'pending','2012-11-25');
	insert into swap values(13,17,'pending','2013-11-25');
	insert into swap values(1,3,'pending','2022-03-01');
	insert into swap values(4,2,'accepted','2022-03-05');
	insert into swap values(7,8,'accepted','2012-11-25');
	insert into swap values(9,10,'accepted','2022-02-05');
	insert into swap values(15,14,'accepted','2015-11-25');
	insert into swap values(16,18,'accepted','2015-12-25');
	insert into swap values(5,6,'rejected','2022-03-05');
	CREATE TABLE accepted_swap (
		item_number_pro int(16) NOT NULL,
		item_number_counter int(16) NOT NULL,
	    accepted_date date NOT NULL,
		proposer_rating int NULL, 
		counterparty_rating int  NULL, 
		KEY accepted_swap_item_number_pro_idx (item_number_pro), 
		KEY accepted_swap_item_number_counter_idx (item_number_counter), 
	    constraint accepted_swap_item_number_pro foreign key (item_number_pro) references item (item_number) on update cascade,
		constraint accepted_swap_item_number_counter foreign key (item_number_counter) references item (item_number) on update cascade
	);
	insert into accepted_swap values(4,2,'2022-03-12',null,null);
	insert into accepted_swap values(7,8,'2022-02-15',4,null);
	insert into accepted_swap values(9,10,'2012-11-28', null, 5);
	insert into accepted_swap values(15,14,'2015-11-29', 5, null);
	insert into accepted_swap values(16,18,'2016-01-25', null, null);
	CREATE TABLE rejected_swap (
		item_number_pro int(16) NOT NULL,
		item_number_counter int(16) NOT NULL,
		rejected_date date NOT NULL,
		KEY rejected_swap_item_number_pro_idx (item_number_pro), 
		KEY rejectaed_swap_item_number_counter_idx (item_number_counter), 
	    constraint rejected_swap_item_number_pro foreign key (item_number_pro) references item (item_number) on update cascade,
		constraint rejected_swap_item_number_counter foreign key (item_number_counter) references item (item_number) on update cascade
	);
	insert into rejected_swap values(5,6,'2022-03-18'); 
	        '''

	    )