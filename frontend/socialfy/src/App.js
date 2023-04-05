import React, { useState, useEffect } from 'react';
import './App.css';
import Feed from './feed';


function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Replace this URL with the actual API endpoint or JSON file path
    const url = 'http://127.0.0.1:5000/secure/feed/0';

    fetch(url)
      .then((response) => response.json())
      .then((data) => setPosts(data))
      .catch((error) => console.error('Error fetching posts:', error));
      
      
  }, []);
  console.log(posts)

  return (
    <div className="App">
      <header className="App-header">
        <h1>Socially</h1>
      </header>
      <main>
        <Feed posts={posts} />
      </main>
    </div>
  );
}

export default App;