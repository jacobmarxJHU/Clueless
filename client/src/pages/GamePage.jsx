import React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import GameLayout from '../components/GameLayout';

const GamePage = () => {
  const { gameCode } = useParams(); // This will get the gameCode from the URL
  const location = useLocation(); // This will allow you to access the routing state

  console.log("Game Code:", gameCode); // Should log the game code from the URL

  // Extract the username and isLeader from the location state (fallback to an empty string if not provided)
  const username = location.state?.username || '';
  const isLeader = location.state?.isLeader;

  return (
    <div>
      <GameLayout
        gameCode={gameCode} // Pass the gameCode from the URL
        username={username} // Pass the username from the routing state
        isLeader={isLeader} // Pass the isLeader sstatus from the routing state
      />
    </div>
  );
};

export default GamePage;
