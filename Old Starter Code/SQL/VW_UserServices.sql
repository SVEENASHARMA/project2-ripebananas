Select *
FROM user_profile 
LEFT JOIN user_profile_services
ON user_profile.User_ID = user_profile_services.User_ID
LEFT JOIN streamingservices ss
on ss.Service_ID = user_profile_services.Service_ID
ORDER BY user_profile.User_Name;