SELECT
	posts.posts_id, 
	users.user_id, 
    users.username, 
    users.profile_img_url,
    posts.posts_created_timestamp,
    posts.post_title,
    posts.post_description,
  
    
    (SELECT group_concat(emots_sub.emoticons_url SEPARATOR ' ; ')  FROM 
		(
			SELECT 
				emoticons_url
			FROM emoticons e
			RIGHT JOIN posts_emoticons p_e ON p_e.emoticons_id_FK = e.emoticons_id
			WHERE p_e.post_id_FK = posts.posts_id
			GROUP BY e.emoticons_id
			ORDER BY COUNT(e.emoticons_id) DESC
			LIMIT 3
		) AS emots_sub
	) AS emoticons_list,
    

	(SELECT GROUP_CONCAT(tag_name SEPARATOR ' ; ') FROM posts_tags p_t
		LEFT JOIN tags t on p_t.tag_id_FK = t.tags_id
		WHERE p_t.post_id_FK = posts.posts_id
	) AS tags_list,
    
    (SELECT COUNT(comments.comment_id) as comments_count FROM comments
		WHERE comments.posts_id_FK = posts.posts_id
	) AS comments_count
    
    
FROM posts 
INNER JOIN users ON posts.creator_id_FK = users.user_id










