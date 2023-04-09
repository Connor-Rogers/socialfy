import Post from './post';
import React, { useEffect, useRef, useCallback } from 'react';

const Feed = ({ posts, fetchPosts }) => {
  const onDelete = () => {
    fetchPosts();
  };

  const observer = useRef();
  const lastPostElementRef = useCallback(
    (node) => {
      if (observer.current) observer.current.disconnect();
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          fetchPosts();
        }
      });
      if (node) observer.current.observe(node);
    },
    [fetchPosts]
  );

  return (
    <div className="feed">
      {posts.map((post, index) => (
        <Post
          key={post.id}
          post={post}
          onDelete={onDelete}
          innerRef={index === posts.length - 1 ? lastPostElementRef : null}
        />
      ))}
    </div>
  );
};

export default Feed;
