import React, { useState } from 'react';
import '@mui/icons-material'

const Post = ({ post, onDelete, innerRef }) => {
  const [likes, setLikes] = useState(post.likes);
  const [liked, setLiked] = useState(false);
  // Bookmarking 
  const handleBookmark = async () => { 
    try {
      const response = await fetch('http://socialfy.rogersconnor.com/secure/song/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({song_uri:post.song_uri}),
      });
      if (!response.ok) {
        throw new Error('Failed to bookmark the post');
      }
  
      const responseData = await response.json();
       // Toggle the bookmark state only if the request is successful
      console.log('Bookmark response:', responseData);
    } catch (error) {
      console.error('Error bookmarking the song:', error);
    }
  };
  // Liking
  const handleLike = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/secure/post/like`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({post_id:post.id}),
      });
  
      if (!response.ok) {
        console.log(JSON.stringify({post_id:post.id}));
        throw new Error('Failed to update the like count');
      }
      
      const updatedPost = await response.json();
      console.log(response)
      setLikes(updatedPost.likes);
     
      setLiked(updatedPost.status);
    } catch (error) {
      console.error('Error updating the like count:', error);
    }
  };
  // Deleting Posts
  const handleDelete = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/secure/post/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({post_id:post.id}),
      });


      if (!response.ok) {
        throw new Error('Failed to delete the post');
      }
      onDelete(post.id);
    } catch (error) {
      console.error('Error deleting the post:', error);
    }
  };
  return (
    <div className="post" ref={innerRef}>
      <div className="post-header">
        <span className="username">{post.friend_name}</span>
         {post.friend_name === post.current_user ? (<button onClick={handleDelete} className="delete-btn">Delete</button>) : null}
        </div>
      <img src={post.song_album_art} alt={post.text_blurb} />
      <p>{post.text_blurb}</p>
      <p>
        <strong>Song:</strong> {post.song_name} <br />
        <strong>Artist:</strong> {post.song_arist}
      </p>
      <div className="post-actions">
      {post.likes !== "null" ? (
         <button onClick={handleLike} className={liked ? 'liked' : ''}>
         {likes} {likes === 1 ? 'Like' : 'Likes'}
       </button>) : null}
         <button onClick={() => handleBookmark()}> Bookmark </button>
      </div>
    </div>
  );
};

export default Post;