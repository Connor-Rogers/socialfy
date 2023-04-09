import React, { useState } from 'react';

const CreatePost = ({ onPostSubmit }) => {
  const [songSearch, setSongSearch] = useState('');
  const [selectedSong, setSelectedSong] = useState(null);
  const [description, setDescription] = useState('');

  const handleSongSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/secure/song/search`,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"query":songSearch}),
      });
      
      if (!response.ok) {
        throw new Error('Failed to search for songs');
      }
  
      const song = await response.json();
      // Select the first song from the results as an example
      console.log(song)
      setSelectedSong(song);
    } catch (error) {
      console.error('Error searching for songs:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newPostData = {
      song_id : selectedSong.song_uri,
      text_blurb : description
    };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/secure/post/make', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newPostData),
      });
  
      if (!response.ok) {
        throw new Error('Failed to create a new post');
      }
      setSongSearch('')
      setSelectedSong(null);
      setDescription('');
      onPostSubmit();
     
    } catch (error) {
      console.error('Error creating a new post:', error);
    }
  };

  return (
    <div className="create-post">
      {!selectedSong ? (
        <form onSubmit={handleSongSearch}>
          <input
            type="text"
            placeholder="Search for a song"
            value={songSearch}
            onChange={(e) => setSongSearch(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      ) : (
        <div>
        <button onClick={() => setSelectedSong(null)}>X</button>
        <form onSubmit={handleSubmit}>
          <p>
            <strong>Song:</strong> {selectedSong.song_name} <br />
            <strong>Artist:</strong> {selectedSong.song_artist}
          </p>
          <textarea
            placeholder="Add a description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <button type="submit">Create Post</button>
        </form>
        </div>
      )}
    </div>
  );
};

export default CreatePost;
