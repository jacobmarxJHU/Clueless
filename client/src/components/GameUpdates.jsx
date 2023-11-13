import React, { useState, useEffect } from 'react';
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
    minHeight: 395,
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

const GameUpdates = ({ socket }) => {
  const classes = useStyles();
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Setup the `message_chat` event listener
    const handleNewMessage = (data) => {
      setMessages((prevMessages) => [...prevMessages, data.message]);
    };

    socket.on('message_chat', handleNewMessage);

    // Clean up the event listener
    return () => {
      socket.off('message_chat', handleNewMessage);
    };
  }, [socket]);

  return (
    <Paper className={classes.updatesBox}>
      <Typography variant="h6">Status Updates</Typography>
      <List>
        {messages.map((message, index) => (
          <ListItem key={index} className={classes.updateMessage}>
            <ListItemIcon className={classes.icon}>
              <ChatIcon color="primary" />
            </ListItemIcon>
            <Typography variant="body1">{message}</Typography>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default GameUpdates;
