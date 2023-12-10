import React, { useState, useEffect } from 'react';
import { Paper, List, ListItem, ListItemIcon, Typography, makeStyles, Divider, TextField, Button } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';

const useStyles = makeStyles((theme) => ({
  container: {
    height: '480px', // Adjusted for both sections
    marginBottom: theme.spacing(2),
  },
  header: {
    backgroundColor: '#303f9f',
    color: '#fff',
    padding: theme.spacing(1),
    textAlign: 'center',
  },
  updatesArea: {
    height: '140px', // Half height for updates
    overflowY: 'auto',
    backgroundColor: theme.palette.background.paper,
  },
  chatArea: {
    height: 'calc(190px - 48px)', // Half height minus input section
    overflowY: 'auto',
    backgroundColor: theme.palette.background.paper,
    marginTop: theme.spacing(2),
  },
  inputSection: {
    display: 'flex',
    padding: theme.spacing(1),
  },
  input: {
    flexGrow: 1,
    marginRight: theme.spacing(1),
  },
  icon: {
    marginRight: theme.spacing(1),
  },
}));

const GameUpdates = ({ socket }) => {
  const classes = useStyles();
  const [gameUpdates, setGameUpdates] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");

  useEffect(() => {
    console.log('Received socket in GameUpdates.jsx:', socket);
    // Set up the listener if the socket instance is not null
    if (socket) {
      socket.on('message_chat', (data) => {
        setGameUpdates(prevUpdates => [...prevUpdates, data.message]);
      });

      socket.on('game_chat', (data) => {
        setChatMessages(prevMessages => [...prevMessages, data.message]);
      });

      // Clean up the event listener when the component unmounts
      // or if the socket instance changes
      return () => {
        socket.off('message_chat');
        socket.off('game_chat');
      };
    }
  }, [socket]); // Only re-run the effect if the socket instance changes

  const handleSendMessage = () => {
    if (socket && currentMessage.trim()) {
      socket.emit('send_chat', currentMessage);
      setCurrentMessage('');
    }
  };

  return (
    
    <Paper className={classes.container}>
      <Typography variant="subtitle1" className={classes.header}>
        Status Updates
      </Typography>
      <List className={classes.updatesArea}>
        {gameUpdates.map((message, index) => (
          <ListItem key={index} className={classes.messageItem}>
            <ListItemIcon className={classes.icon}>
              <ChatIcon color="primary" />
            </ListItemIcon>
            <Typography variant="body1">{message}</Typography>
          </ListItem>
        ))}
      </List>

      <Typography variant="subtitle1" className={classes.header}>
        Chat
      </Typography>
      <List className={classes.chatArea}>
        {chatMessages.map((message, index) => (
          <ListItem key={index} className={classes.messageItem}>
            <ListItemIcon className={classes.icon}>
              <ChatIcon color="primary" />
            </ListItemIcon>
            <Typography variant="body1">{message}</Typography>
          </ListItem>
        ))}
      </List>
      <div className={classes.inputSection}>
        <TextField 
          className={classes.input} 
          value={currentMessage} 
          onChange={(e) => setCurrentMessage(e.target.value)} 
          placeholder="Type a message..." 
          variant="outlined" 
          size="small"
        />
        <Button variant="contained" color="primary" onClick={handleSendMessage}>
          Send
        </Button>
      </div>
    </Paper>
  );
};

export default GameUpdates;
