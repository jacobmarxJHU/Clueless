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
  const [status, setGameStatus] = useState("");
  
  useEffect(() => {
    if (socket) {
      socket.on('notify_current', () => {
        alert("It's your turn!");
        setGameStatus("It's your turn!");
      });

      // Clean up the listener when the component unmounts
      return () => {
        socket.off('start_turn');
      };
    }
  }, [socket]);

  const handleStartGame = () => {
    // Emit the start_game event to the server when the button is clicked
    if (socket) {
      socket.emit('start_game', { gameCode: gameCode });
      setGameStatus("Game started!");
    }
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
