import React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import GameLayout from '../components/GameLayout';

// Mock data for the player's hand
const mockPlayerHand = ['Candlestick', 'Kitchen', 'Mrs. White'];

// Mock data for chat messages
const mockChatMessages = [
  'Miss Scarlet has joined the game.',
  'Prof. Plum moved to the Study.',
  'Miss Scarlet suggested it was Col. Mustard, with the Rope, in the Library.',
  'Prof. Plum was unable to disprove the suggestion.',
  // ... other updates
];

const GamePage = () => {
  const { gameCode } = useParams(); // This will get the gameCode from the URL
  const location = useLocation(); // This will allow you to access the routing state

  console.log("Game Code:", gameCode); // Should log the game code from the URL

  // Extract the username from the location state (fallback to an empty string if not provided)
  const username = location.state?.username || '';

  return (
    <div>
      <GameLayout
        gameCode={gameCode} // Pass the gameCode from the URL
        username={username} // Pass the username from the routing state
        chatMessages={mockChatMessages}
        userHand={mockPlayerHand}
      />
    </div>
  );
};

export default GamePage;
