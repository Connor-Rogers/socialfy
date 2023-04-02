import React from 'react';
import styled from 'styled-components';

const data = [
  {
    username: 'john_doe',
    image: 'https://via.placeholder.com/640x480',
    likes: 123,
  },
  {
    username: 'jane_doe',
    image: 'https://via.placeholder.com/640x480',
    likes: 456,
  },
  // Add more posts here
];

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
`;

const Post = styled.div`
  background-color: white;
  border-radius: 4px;
  width: 100%;
  max-width: 640px;
  margin-bottom: 20px;
`;

const PostHeader = styled.div`
  display: flex;
  align-items: center;
  padding: 16px;
`;

const ProfileImage = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
`;

const Username = styled.span`
  font-weight: bold;
`;

const PostImage = styled.img`
  width: 100%;
  height: auto;
`;

const PostFooter = styled.div`
  padding: 16px;
`;

const Likes = styled.p`
  margin: 0;
  font-weight: bold;
`;

function App() {
  return (
    <Container>
      {data.map((post, index) => (
        <Post key={index}>
          <PostHeader>
            <ProfileImage src="https://via.placeholder.com/40" alt="profile" />
            <Username>{post.username}</Username>
          </PostHeader>
          <PostImage src={post.image} alt="post" />
          <PostFooter>
            <Likes>{post.likes} likes</Likes>
          </PostFooter>
        </Post>
      ))}
    </Container>
  );
}

export default App;