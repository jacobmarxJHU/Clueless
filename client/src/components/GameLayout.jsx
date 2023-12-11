import React, { useState, useEffect, createContext } from 'react';
import { Divider, makeStyles, Container, Grid } from '@material-ui/core';
import Navbar from './Navbar';
import GameStatusBanner from './GameStatusBanner';
import CharacterAndWeaponLocation from './CharacterAndWeaponLocation';
import GameBoard from './GameBoard';
import GameUpdates from './GameUpdates';
import PlayerPanel from './PlayerPanel';
import { io } from "socket.io-client";

// Create a context for the socket
export const SocketContext = createContext(null);

const useStyles = makeStyles((theme) => ({
  container: {
    padding: 0,
    maxWidth: '100%',
  },
  statusBanner: {
    width: '100%',
    backgroundColor: theme.palette.info.main,
    padding: theme.spacing(1),
    marginBottom: theme.spacing(2),
  },
  gameSection: {
    // Instead of marginBottom, you might want to set a specific height or max-height
    height: 'auto', // Or you can use a specific value, for example '500px'
    // If the content is dynamically sized, you might want to use max-height instead
    maxHeight: '500px', // Adjust the max-height as needed
    overflow: 'hidden', // Use 'auto' if you want to allow scrolling
    marginBottom: theme.spacing(2),
  },
  // Make sure this style exists and it's not causing any overflow issues
  equalColumn: {
    width: '100%', // Ensures each Grid item takes full width of its container
    padding: theme.spacing(1),
    [theme.breakpoints.down('sm')]: {
      width: '100%',
      maxWidth: '100%',
      flexBasis: '100%',
    },
  },
  scrollableColumn: {
    maxHeight: '600px', // Set a fixed height for the GameUpdates column
    overflowY: 'auto',
  },
  playerSection: {
    marginBottom: theme.spacing(2),
  },
  playerHandColumn: {
    maxWidth: '33%',
  },
  playerActionsColumn: {
    maxWidth: '67%',
  },
  divider: {
    width: '100%',
    margin: `${theme.spacing(3)}px 0`, // Space above and below the divider
  },
  gameBoardGridItem: {
    padding: theme.spacing(0), // Ensure no extra padding
  },
}));

const GameLayout = ({ username, gameCode, isLeader }) => {
  const classes = useStyles();
  const [socketInstance, setSocket] = useState(null);

  useEffect(() => {
    // Initialize the socket connection
    const gameSocket = io("http://localhost:5000", {
      transports: ["websocket"],
      upgrade: false,
    });
    setSocket(gameSocket);

    // Restore the user session
    gameSocket.emit("game_join", { username, gameCode });

    // Event listeners for socket connection
    gameSocket.on("connect", () => {
      console.log("Connected to socket.io server from GameLayout");
    });

    // Clean up the socket when the component unmounts 
    return () => {
      gameSocket.disconnect();
      console.log('Disconnected from socket.io server');
    };
  }, []);

  return (
    <Container className={classes.container}>
      <Navbar username={username} /> 
      <GameStatusBanner socket={socketInstance} isLeader={isLeader} gameCode={gameCode} className={classes.statusBanner} />
      {/* Grid for the game board and character locations */}
      <Grid container spacing={2} className={classes.gameSection}>
        <Grid item xs={12} sm={4} className={classes.equalColumn}>
          <CharacterAndWeaponLocation socket={socketInstance} />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.gameBoardGridItem}>
          <GameBoard socket={socketInstance} />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.equalColumn}>
          <GameUpdates socket={socketInstance} />
        </Grid>
      </Grid>
      <Divider className={classes.divider} />


      {/* Grid for the player section */}
      <Grid container className={classes.playerSection} justifyContent="center">
        {/* The PlayerPanel now takes up the full width of the row */}
        <Grid item xs={12}>
          <PlayerPanel username={username} gameCode={gameCode} socket={socketInstance} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default GameLayout;
