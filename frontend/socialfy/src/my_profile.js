import React, { useState, useEffect } from 'react';
import AddFriend from './add_friend';
import './my_profile.css'

const MyProfile = ({ onClose }) => {
  const [user, setUser] = useState(null);
  const [friends, setFriends] = useState([]);

  useEffect(() => {
    fetchUser();
    fetchFriends();
  }, []);

  const fetchUser = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/secure/user/self');
      
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }

      const userData = await response.json();
      setUser(userData);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchFriends = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/secure/user/friends');

      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }

      const friendsData = await response.json();
      setFriends(friendsData.friends);
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  };

  const removeFriend = async (friendId) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/secure/user/friends/remove',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"friend_id":friendId}),
      });

      if (!response.ok) {
        throw new Error('Failed to remove friend');
      }

      // Refresh the friends list
      fetchFriends();
    } catch (error) {
      console.error('Error removing friend:', error);
    }
  };

  const handleAddFriend = () => {
    fetchFriends();
  };

  return (
    <div className="my-profile">
      <button onClick={onClose}>Close</button>
      {user && (
        <div href={user.spotify_url}>
          <img src={user.profile_photo} alt="Profile" />
          <p>{user.username}</p>
        </div>
      )}
      <AddFriend onAddFriend={handleAddFriend} />
      <ul>
        {friends.map((friend) => (
          <li key={friend.id}>
            <img src={friend.profile_photo} alt="Friend" />
            <p href={friend.spotify_url}>{friend.display_name}</p>
            <button onClick={() => removeFriend(friend.id)}>Remove Friend</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MyProfile;