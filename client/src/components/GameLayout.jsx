import React from 'react';
import { Divider, makeStyles, Container, Grid } from '@material-ui/core';
import Navbar from './Navbar';
import GameStatusBanner from './GameStatusBanner';
import CharacterAndWeaponLocation from './CharacterAndWeaponLocation';
import GameBoard from './GameBoard';
import GameUpdates from './GameUpdates';
import PlayerPanel from './PlayerPanel';

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

const GameLayout = ({ username, gameCode, chatMessages, userHand }) => {
  const classes = useStyles();

  // Dummy data for rooms
  const rooms = [
    { room: 'Study', character: 'Prof. Plum', weapon: 'Candlestick' },
    { room: 'Hall', character: 'Mr. Green', weapon: 'Revolver' },
    { room: 'Lounge', character: 'Mrs. Peacock', weapon: 'Rope' },
    { room: 'Dining Room', character: 'Miss Scarlet', weapon: 'Lead Pipe' },
    { room: 'Kitchen', character: 'Colonel Mustard', weapon: 'Knife' },
    { room: 'Ballroom', character: 'Mrs. White', weapon: 'Wrench' },
    { room: 'Conservatory', character: '', weapon: '' },
    { room: 'Billiard Room', character: '', weapon: '' },
    { room: 'Library', character: '', weapon: '' },
  ];

  // Example updates
  const updates = [
    'Prof. Plum moved to the Study.',
    'Mr. Green suggested it was Mrs. Peacock in the Lounge with the Rope.',
    'Miss Scarlet disproved the suggestion.',
    'It is now Colonel Mustard’s turn.',
    'Colonel Mustard made an accusation!',
    'Game over: Colonel Mustard won the game!',
  ];

  return (
    <Container className={classes.container}>
      <Navbar username="{username}" /> 
      <GameStatusBanner status="It's your turn!" className={classes.statusBanner} />
      {/* Grid for the game board and character locations */}
      <Grid container spacing={2} className={classes.gameSection}>
        <Grid item xs={12} sm={4} className={classes.equalColumn}>
          <CharacterAndWeaponLocation rooms={rooms} />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.gameBoardGridItem}>
          <GameBoard image="/path/to/gameBoard.png" />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.equalColumn}>
          <GameUpdates updates={chatMessages} />
        </Grid>
      </Grid>
      <Divider className={classes.divider} />


      {/* Grid for the player section */}
      <Grid container className={classes.playerSection} justifyContent="center">
        {/* The PlayerPanel now takes up the full width of the row */}
        <Grid item xs={12}>
          <PlayerPanel userHand={userHand} gameCode={gameCode} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default GameLayout;
