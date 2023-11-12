import React from 'react';
import { Paper, Divider, makeStyles, Typography } from '@material-ui/core';
import PlayerHand from './PlayerHand';
import PlayerActions from './PlayerActions';

const useStyles = makeStyles((theme) => ({
  root: {
    paddingTop: '10px',
    border: '1px solid black',
    borderRadius: theme.shape.borderRadius,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    maxWidth: '60%', // Adjust the width as needed
    margin: '0 auto', // Center the section
  },
  divider: {
    width: '100%',
    margin: `${theme.spacing(1)}px 0`, // Space above and below the divider
  },
  // You might need to adjust the PlayerHand and PlayerActions styles if they are not aligned properly
}));

const PlayerPanel = ({ userHand, gameCode }) => {
  const classes = useStyles();

  return (
    <Paper className={classes.root} elevation={2}>
      <PlayerActions />
      <Divider className={classes.divider} />
      <PlayerHand userHand={userHand} />
      <Typography variant="body2">Game Code: {gameCode}</Typography>
    </Paper>
  );
};

export default PlayerPanel;