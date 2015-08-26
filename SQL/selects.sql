select * from `scout_camp`.`user`;
select user_name, facebook_id from `scout_camp`.`user` where facebook_id <>'null';
select user_name, tier_name from `scout_camp`.`tier`, `scout_camp`.`user`; 