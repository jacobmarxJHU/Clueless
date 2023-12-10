import React from 'react';
import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  gameBoardContainer: {
    textAlign: 'center', // Centers the image horizontally
    lineHeight: 0, // Removes extra line height
    padding: theme.spacing(0), // Removes padding
  },
  gameBoardImage: {
    maxWidth: '100%', // Ensures the image is not wider than its container
    maxHeight: '100%', // Ensures the image is not taller than its container
    height: '490px', // Maintains the aspect ratio of the image
    display: 'block', // Removes any inline spacing
    margin: '0 auto', // Centers the image if it's not as wide as its container
  },
  gameBoardGridItem: {
    // If you've set a fixed height for the GameBoard, use the same value here
    height: '500px', // Example fixed height
  },
  gameUpdatesGridItem: {
    height: '500px', // Match the GameBoard height
    overflowY: 'auto', // Allow scrolling for overflow content
  },
}));

const GameBoard = ({}) => {
  const classes = useStyles();

  const imageUrl = '/gameBoard.png'; 

  return (
    <div className={classes.gameBoardContainer}>
      <img src={imageUrl} alt="Game Board" className={classes.gameBoardImage} />
    </div>
  );
};

export default GameBoard;
