import React, { useState, useEffect } from 'react';
import { Paper, Typography, Button, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  banner: {
    padding: theme.spacing(1),
    backgroundColor: '#F3F6F9',
    textAlign: 'center',
    width: '100%', // Adjusted to 100% for full width
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  startButton: {
    marginTop: theme.spacing(1),
  },
}));

const GameStatusBanner = ({ isLeader, socket, gameCode }) => {
  const classes = useStyles();
  const [status, setStatus] = useState(""); // Initialize with empty string or any default status

  /*
  const handleStartGame = () => {
    // Emit the start_game event with the gameCode in an object
    // and include a callback for the server's acknowledgement
    console.log(gameCode);
    socket.emit('start_game', { gameCode: gameCode }, (response) => {
      console.log('Server responded with:', response);
    });
  };
  */

  useEffect(() => {
    const handleStartTurn = () => {
      setStatus("It's your turn!");
    };

    // Setup the event listener for 'start_turn' event
    socket?.on('start_turn', handleStartTurn);

    // Return a cleanup function to remove the event listener
    return () => {
      socket?.off('start_turn', handleStartTurn);
    };
  }, [socket]);

  const handleStartGame = () => {
    // Emit the 'start_game' event when the button is clicked
    socket?.emit('start_game', { gameCode: gameCode });
  };

  return (
    <Paper elevation={4} className={classes.banner}>
      <Typography variant="subtitle1"><strong>{status}</strong></Typography>
      {isLeader ? (
        <Button
          variant="contained"
          color="primary"
          className={classes.startButton} 
          onClick={handleStartGame}
        >Start Game!</Button>
      ) : (
        <Typography variant="subtitle1"><strong>{status}</strong></Typography>
      )}
    </Paper>
  );
};

export default GameStatusBanner;
