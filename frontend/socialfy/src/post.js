import React, { useState } from 'react';
import '@mui/icons-material'

const Post = ({ post }) => {
  const [bookmarked, setBookmarked] = useState(false);
  const handleBookmark = async () => {
    const payload = {
      "track_id": post.id,
    };
  
    try {
      const response = await fetch('https://your-api-endpoint/bookmarks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error('Failed to bookmark the post');
      }
  
      const responseData = await response.json();
      setBookmarked(!); // Toggle the bookmark state only if the request is successful
      console.log('Bookmark response:', responseData);
    } catch (error) {
      console.error('Error bookmarking the post:', error);
    }
  };
  

  return (
    <div className="post">
      <div className="post-header">
        <span className="username">{post.friend_id}</span>
      </div>
      <img src={post.song_album_art} alt={post.text_blurb} />
      <p>{post.text_blurb}</p>
      <p>
        <strong>Song:</strong> {post.song_name} <br />
        <strong>Artist:</strong> {post.song_arist}
      </p>
      <div className="post-actions">
      {post.likes !== "null" ? (
          <button onClick={() => console.log('Liked!')}>
            Like ({post.likes}) </button> ) : null}
         <button onClick={() => handleBookmark}> Bookmark </button>
      </div>
    </div>
  );
};

export default Post;