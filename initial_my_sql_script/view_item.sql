select count(card_game.item_number),
count(board_game.item_number),
count(computer_game.item_number),
count(video_game.item_number),
count(jigsaw.item_number)
from
user join item using(email)
left join card_game using(item_number)
left join board_game using(item_number)
left join computer_game using(item_number)
left join video_game using(item_number)
left join jigsaw using(item_number)
where email = 'ebad@gmail.com'