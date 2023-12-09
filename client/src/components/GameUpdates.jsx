import React, { useState, useEffect } from 'react';
import { Paper, List, ListItem, ListItemIcon, Typography, makeStyles } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';

const useStyles = makeStyles((theme) => ({
  header: {
    backgroundColor: '#303f9f',
    color: '#fff',
    padding: theme.spacing(1),
    textAlign: 'center',
    fontWeight: 'bold',
  },
  updatesBox: {
    height: '140px',
    overflow: 'hidden',
    marginBottom: theme.spacing(2),
  },
  updates: {
    height: 'calc(100% - 48px)', // Adjust height to subtract the header height
    overflowY: 'auto',
    backgroundColor: theme.palette.background.paper,
  },
  icon: {
    marginRight: theme.spacing(1),
  },
}));

const GameUpdates = ({ socket }) => {
  const classes = useStyles();
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    console.log('Received socket in GameUpdates.jsx:', socket);
    // Set up the listener if the socket instance is not null
    if (socket) {
      const handleNewMessage = (data) => {
        setMessages((prevMessages) => [...prevMessages, data.message]);
      };

      socket.on('message_chat', handleNewMessage);

      // Clean up the event listener when the component unmounts
      // or if the socket instance changes
      return () => {
        socket.off('message_chat', handleNewMessage);
      };
    }
  }, [socket]); // Only re-run the effect if the socket instance changes

  return (
    
    <Paper className={classes.updatesBox}>
      <Typography variant="subtitle1" className={classes.header}>
        Status Updates
      </Typography>
      <List className={classes.updates}>
        {messages.map((message, index) => (
          <ListItem key={index} className={classes.messageItem}>
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
