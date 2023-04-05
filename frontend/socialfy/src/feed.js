import React from 'react';
import Post from './post';

const Feed = ({ posts }) => {
  return (
    <div className="feed">
      {posts.map((post, index) => (
        <Post key={index} post={post} />
      ))}
    </div>
  );
};

export default Feed;