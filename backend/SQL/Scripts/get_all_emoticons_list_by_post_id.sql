SELECT 
	emoticons_url,
    emoticons_name,
	profile_img_url,
	username,
    u.user_id,
    reaction_date
FROM posts_emoticons p_e

RIGHT JOIN emoticons e ON e.emoticons_id = p_e.emoticons_id_FK
RIGHT JOIN users u ON u.user_id = p_e.user_id
WHERE post_id_FK = 9
ORDER BY reaction_date DESC
