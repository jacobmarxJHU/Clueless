import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Card,
  CardContent,
  makeStyles,
  Grid,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(1),
    margin: theme.spacing(2),
    backgroundColor: theme.palette.background.paper,
    display: 'flex', // Added for horizontal layout
    alignItems: 'center', // Align items vertically
    flexWrap: 'wrap', // Allow items to wrap
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'left',
    marginRight: theme.spacing(1), // Space between hand and character sections
  },
  card: {
    margin: theme.spacing(1),
  },
  cardContent: {
    padding: theme.spacing(2),
    "&:last-child": {
      paddingBottom: theme.spacing(1),
    },
  },
  header: {
    marginBottom: theme.spacing(0),
    paddingLeft: '9px',
  },
  // Added for character card to not grow
  characterCard: {
    maxWidth: 'fit-content',
  },
}));

const PlayerHand = ({ socket, username }) => {
  const classes = useStyles();
  const [userHand, setUserHand] = useState([]); // State to hold the user's hand
  const [userCharacter, setUserCharacter] = useState([]); // State to hold the user's hand

  useEffect(() => {
    // Listen for the 'pop_hand' event from the server
    if (socket) {
      socket.on('pop_hand', (data) => {
        // Update the user's hand based on the username
        const newUserHand = data.playerHands[username];
        if (newUserHand) {
          setUserHand(newUserHand);
        }
        // Update the user's character based on the username
        const newUserCharacter = data.playerCharacters[username];
        if (newUserCharacter) {
          setUserCharacter(newUserCharacter);
        }
      });

      // Clean up the listener when the component unmounts
      return () => {
        socket.off('pop_hand');
      };
    }
  }, [socket, username]); // Dependencies

  return (
    <Paper className={classes.root} elevation={3}>
      {/* Hand Section */}
      <div className={classes.section}>
        <Typography variant="h6" className={classes.header}>Hand</Typography>
        <Grid container direction="row" justifyContent="flex-start" alignItems="center">
          {userHand.map((card, index) => (
            <Card key={index} className={classes.card}>
              <CardContent className={classes.cardContent}>
                <Typography variant="body2">{card}</Typography>
              </CardContent>
            </Card>
          ))}
        </Grid>
      </div>

      {/* Character Section */}
      <div className={classes.section}>
        <Typography variant="h6" className={classes.header}>Character</Typography>
        <Card className={`${classes.card} ${classes.characterCard}`}>
          <CardContent className={classes.cardContent}>
            <Typography variant="body2">{userCharacter}</Typography>
          </CardContent>
        </Card>
      </div>
    </Paper>
  );
};

export default PlayerHand;
