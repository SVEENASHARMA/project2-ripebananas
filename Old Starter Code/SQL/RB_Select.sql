use ripe_bananas;
SELECT *
FROM user_frequency;

SELECT *
FROM streamingservices
ORDER BY Service_Name asc;
 

SELECT *
FROM user_profile_services;

Select *
FROM user_profile 
INNER JOIN user_profile_services
ON user_profile.User_ID = user_profile_services.User_ID
LEFT JOIN streamingservices ss
on ss.Service_ID = user_profile_services.Service_ID
ORDER BY user_profile.User_Name;