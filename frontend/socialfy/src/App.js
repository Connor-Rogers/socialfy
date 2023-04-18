import React, { useState, useEffect } from 'react';
import { BrowserRouter, useNavigate } from 'react-router-dom';
import './App.css';
import Feed from './feed';
import CreatePost from './create_post';
import MyProfile from './my_profile';

function App() {
  const [posts, setPosts] = useState([]);
  const [showProfile, setShowProfile] = useState(false);
  const [page, setPage] = useState(0);
  const navigate = useNavigate();

  const deletePost = (postId) => {
    setPosts(posts.filter((post) => post.id !== postId));
  };

  const fetchPosts = async (pageNumber) => {
    try {
      const response = await fetch(`http://socialfy.rogersconnor.com/secure/feed/${pageNumber}`);

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

  const handleLogout = () => {
    navigate('/secure/logout');
    window.location.reload();
  };
  return (
    <div className="app">
      <h1>Socialfy</h1>
      <header className="app-header">
        <CreatePost onPostSubmit={() => {
          setPosts([]);
          setPage(0);
          fetchPosts(0);
        }} />
        <button class="enter_profile" onClick={() => setShowProfile(true)}>My Profile</button>
        {showProfile && (
          <div className="overlay">
            <MyProfile onClose={() => setShowProfile(false)} />
          </div>
        )}
        <button className="logout" onClick={handleLogout}>Logout</button>
      </header>
      <Feed posts={posts} fetchPosts={() => fetchPosts(page)} onDeletePost={deletePost} />
    </div>
  );
};

export default App;

