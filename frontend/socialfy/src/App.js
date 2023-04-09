import React, { useState, useEffect } from 'react';
import './App.css';
import Feed from './feed';
import CreatePost from './create_post';
import MyProfile from './my_profile';

function App() {
  const [posts, setPosts] = useState([]);
  const [showProfile, setShowProfile] = useState(false);
  const [page, setPage] = useState(0);

  const fetchPosts = async (pageNumber) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/secure/feed/${pageNumber}`);

      if (!response.ok) {
        throw new Error('Failed to fetch posts');
      }

      const data = await response.json();
      setPosts((prevPosts) => [...prevPosts, ...data]);
      setPage((prevPage) => prevPage + 1);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  useEffect(() => {
    fetchPosts(page);
  }, []);

  return (
    <div className="app">
      <h1>Socialfy</h1>
      <header className="app-header">
        <CreatePost onPostSubmit={() => {
          setPosts([]);
          setPage(0);
          fetchPosts(0);
        }} />
        <button onClick={() => setShowProfile(true)}>My Profile</button>
        {showProfile && (
          <div className="overlay">
            <MyProfile onClose={() => setShowProfile(false)} />
          </div>
        )}
      </header>
      <Feed posts={posts} fetchPosts={() => fetchPosts(page)} />
    </div>
  );
};

export default App;

