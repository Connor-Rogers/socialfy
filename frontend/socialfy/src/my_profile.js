import React, { useState, useEffect } from 'react';
import AddFriend from './add_friend';
import './my_profile.css'

const MyProfile = ({ onClose }) => {
  const [user, setUser] = useState(null);
  const [friends, setFriends] = useState([]);
  const [friendProfiles, setFriendProfiles] = useState([]);

  useEffect(() => {
    fetchUser();
    fetchFriends();
  }, []);

  const fetchUser = async () => {
    try {
      const response = await fetch('http://socialfy.rogersconnor.com/secure/user/self');
      
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
      const response = await fetch('http://socialfy.rogersconnor.com/secure/user/friends');

      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }

      const friendsData = await response.json();
      setFriends(friendsData.friends);
      console.log(friendsData)
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  };
  const fetchOtherUser = async (friendId) => {
    try {
      const response = await fetch("http://socialfy.rogersconnor.com/secure/user/other", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: friendId }),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch posts");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching posts:", error);
      return;
    }
  };
  useEffect(() => {
    const fetchAllFriendProfiles = async () => {
      const profiles = await Promise.all(friends.map((friend) => fetchOtherUser(friend)));
      setFriendProfiles(profiles);
    };

    if (friends.length > 0) {
      fetchAllFriendProfiles();
    }
  }, [friends]);

  const removeFriend = async (friendId) => {
    try {
      const response = await fetch('http://socialfy.rogersconnor.com/secure/user/friends/remove',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"user_id":friendId}),
      });

      if (!response.ok) {
        throw new Error('Failed to remove friend');
      }

      // Refresh the friends list
      setFriendProfiles((prevFriendProfiles) => prevFriendProfiles.filter((profile) => profile.user_id !== friendId));
    } catch (error) {
      console.error('Error removing friend:', error);
      fetchFriends();
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
      {friendProfiles.map((friendProfile) => (
          <li key={friendProfile.display_name}>
            <img src={friendProfile.profile_photo} alt="Friend" />
            <p href={friendProfile.spotify_url}>{friendProfile.display_name}</p>
            <button onClick={() => removeFriend(friendProfile.user_id)}>Remove Friend</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MyProfile;