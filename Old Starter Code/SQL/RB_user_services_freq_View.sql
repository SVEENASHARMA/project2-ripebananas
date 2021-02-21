CREATE VIEW `users_services_frequency` AS
Select *
FROM user_profile up
INNER JOIN user_profile_services ups
ON up.User_ID = usp.User_ID
LEFT JOIN streamingservices ss
on ss.Service_ID = ups.Service_ID
LEFT JOIN user_frequency uf
ON uf.Frequency_ID = up.Frequency_ID
ORDER BY user_profile.User_Name;