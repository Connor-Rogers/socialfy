import React, { useState } from 'react';

const AddFriend = ({ onAddFriend }) => {
  const [friendUsername, setFriendUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Replace with the actual API endpoint to add a friend
      const response = await fetch('http://socialfy.rogersconnor.com/secure/user/friends/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ display_name: friendUsername }),
      });

      if (!response.ok) {
        throw new Error('Failed to add friend');
      }

      setFriendUsername('');
      onAddFriend();
    } catch (error) {
      console.error('Error adding friend:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Add friend by username"
        value={friendUsername}
        onChange={(e) => setFriendUsername(e.target.value)}
      />
      <button type="submit">Add Friend</button>
    </form>
  );
};

export default AddFriend;