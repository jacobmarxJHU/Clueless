import React from 'react';
import { Paper, List, ListItem, ListItemIcon, Typography, makeStyles } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';

const useStyles = makeStyles((theme) => ({
  updatesBox: {
    marginTop: theme.spacing(2),
    maxHeight: '300px', // Set a max-height for scrolling
    overflow: 'auto',
    padding: theme.spacing(2),
    backgroundColor: '#F3F6F9',
    border: '1px solid black',
  },
  updateMessage: {
    listStyleType: 'none', // Removes list style
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(1),
    borderRadius: theme.shape.borderRadius,
    marginBottom: theme.spacing(1),
    display: 'flex',
    alignItems: 'center',
  },
  icon: {
    marginRight: theme.spacing(1),
  },
}));

const GameUpdates = ({ updates }) => {
  const classes = useStyles();

  return (
    <Paper className={classes.updatesBox}>
      <Typography variant="h6">Status Updates</Typography>
      <List>
        {updates.map((update, index) => (
          <ListItem key={index} className={classes.updateMessage}>
            <ListItemIcon className={classes.icon}>
              <ChatIcon color="primary" />
            </ListItemIcon>
            <Typography variant="body1">{update}</Typography>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default GameUpdates;
