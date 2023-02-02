DELIMITER $$
create function calc_distance (lat1 float,long1 float, lat2 float, long2 float)
returns float
BEGIN
declare rad_lat1 float;
declare rad_long1 float;
/*declare rad_long1,rad_lat2,rad_long2,lat_diff,long_diff, alpha,c,distance float(7,2);*/
declare rad_lat2 float;
declare rad_long2 float;
declare lat_diff float;
declare long_diff float;
declare alpha float;
declare c float;
declare distance float;
set rad_lat1 = radians(lat1);
set rad_long1 = radians(long1);
set rad_lat2 = radians(lat2);
set rad_long2 = radians(long2);
set lat_diff = rad_lat2 - rad_lat1;
set long_diff = rad_long2 - rad_long1;
set alpha = pow(sin(lat_diff/2),2)  * pow(cos(rad_lat2/2),2) * pow(sin(long_diff/2),2);
set c = 2 * atan2(sqrt(alpha),sqrt(1-alpha));
set distance = 3958.75 * c;
RETURN distance ;
END$$
select calc_distance(22,12.3,81.1,31)