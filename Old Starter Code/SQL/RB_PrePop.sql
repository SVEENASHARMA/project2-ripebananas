use ripe_bananas;
DELETE FROM user_frequency;
INSERT INTO user_frequency(Frequency_ID, Frequency_Name, Frequency_Description)
VALUES(1, 'Daily', 'Streams VOD at least once a day'),
	(2, 'Weekly', 'Streams a least 2 times a week'),
    (3, 'Monthly', 'Streams fewer than 3 times a month');

