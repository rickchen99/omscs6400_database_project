DELIMITER $$
create function calc_distance1 ( zip1 varchar(5) ,  zip2 varchar(5) )
returns float
BEGIN
declare rad_lat1 float;
declare rad_long1 float;
declare rad_lat2 float;
declare rad_long2 float;
declare lat_diff float;
declare long_diff float;
declare alpha float;
declare c float;
declare distance float;

select radians(latitude) into rad_lat1 from address where postal_code like zip1;
select radians(longitude) into rad_long1 from address where postal_code like zip1;
select radians(latitude) into rad_lat2 from address where postal_code like zip2;
select radians(longitude) into rad_long2 from address where postal_code like zip2;

set lat_diff = rad_lat2 - rad_lat1;
set long_diff = rad_long2 - rad_long1;
set alpha = pow(sin(lat_diff/2),2)  * pow(cos(rad_lat2/2),2) * pow(sin(long_diff/2),2);
set c = 2 * atan2(sqrt(alpha),sqrt(1-alpha));
set distance = 3958.75 * c;
RETURN distance ;
END$$
calc_distance1('10001','40002')