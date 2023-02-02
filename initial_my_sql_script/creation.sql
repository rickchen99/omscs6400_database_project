DROP DATABASE IF EXISTS	swapGame_team024_spr22;
CREATE DATABASE swapGame_team024_spr22;
USE swapGame_team024_spr22;

CREATE TABLE address (
	postal_code varchar(5) NOT NULL, 
	city varchar(60) NOT NULL, 
	state varchar(60) NOT NULL, 
	longitude decimal(11,8) NOT NULL, 
	latitude decimal(10,8) NOT NULL, 
	PRIMARY KEY (postal_code)
);

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

CREATE TABLE phone (
	phone_number char(12)  NOT NULL,
        email varchar(250) NOT NULL, 
	phone_type varchar(100) NULL,
	is_shared boolean NOT NULL, 
	PRIMARY KEY (phone_number),  
	KEY (email),  
        constraint phone_user_email foreign key (email) references user (email) on update cascade
);

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

CREATE TABLE board_game (
	item_number int(16) not null, 
    KEY (item_number), 
    constraint board_game_item_number foreign key (item_number) references item (item_number) on update cascade
);

CREATE TABLE card_game (
	item_number int(16) not null, 
        KEY (item_number), 
        constraint card_game_item_number foreign key (item_number) references item (item_number) on update cascade
);

CREATE TABLE computer_game (
	item_number int(16) NOT NULL, 
	os varchar(60) NOT NULL,
	KEY computer_item_number_idx (item_number), 
        constraint computer_item_number foreign key (item_number) references item (item_number) on update cascade
);

CREATE TABLE video_platform (
    type varchar(60) NOT NULL,
    primary key (type)
	);

CREATE TABLE video_game (
	item_number int(16) NOT NULL, 
    	platform_type varchar(60) NOT NULL,
   	 media varchar(60) NOT NULL,
   	 KEY (platform_type), 
    	constraint video_game_platform foreign key (platform_type) references video_platform (type) on update cascade,
	KEY (item_number), 
    	constraint video_game_item_number foreign key (item_number) references item (item_number) on update cascade
);

CREATE TABLE jigsaw (
	item_number int(16) NOT NULL,
    	piece_count int(16) NOT NULL,
	KEY (item_number), 
    	constraint jigsaw_item_number foreign key (item_number) references item (item_number) on update cascade
);

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

CREATE TABLE rejected_swap (
	item_number_pro int(16) NOT NULL,
	item_number_counter int(16) NOT NULL,
	rejected_date date NOT NULL,
	KEY rejected_swap_item_number_pro_idx (item_number_pro), 
	KEY rejectaed_swap_item_number_counter_idx (item_number_counter), 
   	constraint rejected_swap_item_number_pro foreign key (item_number_pro) references item (item_number) on update cascade,
	constraint rejected_swap_item_number_counter foreign key (item_number_counter) references item (item_number) on update cascade
);