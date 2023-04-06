          
SELECT
	emoticons.emoticons_name,
	(
		SELECT 
			JSON_ARRAYAGG(
					JSON_OBJECT(
						'emoticons_name', emoticons_name,
						'username', username,
						'user_id', p_e.user_id,
						'profile_img_url', profile_img_url,
						'reaction_date', reaction_date
					)
			)
		FROM posts_emoticons p_e
		RIGHT JOIN emoticons e ON e.emoticons_id = p_e.emoticons_id_FK
		RIGHT JOIN users u ON u.user_id = p_e.user_id
		WHERE post_id_FK = 9 AND emoticons_name = emoticons.emoticons_name
		ORDER BY reaction_date DESC
	) as json_result
FROM posts_emoticons
RIGHT JOIN emoticons ON emoticons.emoticons_id = posts_emoticons.emoticons_id_FK
RIGHT JOIN users ON users.user_id = posts_emoticons.user_id
WHERE post_id_FK = 9
GROUP BY emoticons_id
ORDER BY reaction_date DESC    

   


