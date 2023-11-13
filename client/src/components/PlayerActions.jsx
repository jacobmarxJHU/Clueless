import React from 'react';
import { Paper, Typography, Button, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(1),
  },
  header: {
    marginBottom: theme.spacing(1), // Add some space below the header
  },
  buttonsContainer: {
    display: 'flex', // Set to 'flex' to enable flexbox for button alignment
    flexDirection: 'row', // Align buttons horizontally
    alignItems: 'center', // Center buttons vertically
  },
  button: {
    margin: theme.spacing(1),
    flexGrow: 1, // Buttons will grow to fill available space
  },
}));

const PlayerActions = () => {
  const classes = useStyles();

  // Handlers for the buttons' onClick events
  const handleMove = () => {
    console.log('Move'); // Placeholder for actual logic
  };

  const handleSuggestion = () => {
    console.log('Suggestion'); // Placeholder for actual logic
  };

  const handleAccusation = () => {
    console.log('Accusation'); // Placeholder for actual logic
  };

  return (
    <Paper className={classes.root}>
      <Typography variant="h6" className={classes.header}>Actions</Typography>
      <div className={classes.buttonsContainer}>
      <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={handleMove}
        >
          Move
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={handleSuggestion}
        >
          Make a Suggestion
        </Button>
        <Button
          variant="contained"
          color="secondary"
          className={classes.button}
          onClick={handleAccusation}
        >
          Make an Accusation
        </Button>
      </div>
    </Paper>
  );
};

export default PlayerActions;
