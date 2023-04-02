import './App.css';
import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';


const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #191414;
`;

const Title = styled.h1`
  font-size: 32px;
  font-family: 'proxima-nova', sans-serif;
  font-weight: bold;
  color: #FFFFFF;
  margin-bottom: 24px;
`;

const LoginButton = styled.button`
  background-color: #1DB954;
  border: none;
  color: white;
  padding: 12px 24px;
  text-align: center;
  text-decoration: none;
  font-family: 'proxima-nova', sans-serif;
  display: inline-block;
  font-size: 16px;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
`;

function App() {
  const navigate = useNavigate();
  const handleLoginClick = () => {
    navigate('/login'); 
    window.location.reload();
  };
  return (
    <Container>
      <Title>Socialfy</Title>
      <LoginButton onClick={handleLoginClick}>Login</LoginButton>
    </Container>
  );
}

export default App;