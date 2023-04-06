SELECT 
	emoticons_url,
    emoticons_name,
    COUNT(emoticons_id) as emoticons_count
FROM posts_emoticons p_e

RIGHT JOIN emoticons e ON e.emoticons_id = p_e.emoticons_id_FK
WHERE post_id_FK = 9
GROUP BY emoticons_id
ORDER BY COUNT(emoticons_id) DESC