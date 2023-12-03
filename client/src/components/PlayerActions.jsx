import React, { useState, useEffect } from 'react';
import { 
  Button, 
  Modal, 
  Backdrop, 
  Fade, 
  makeStyles, 
  MenuItem, 
  FormControl, 
  Select, 
  InputLabel,
  Grid,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
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

const PlayerActions = ({ gameCode, socket, username }) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [actionType, setActionType] = useState('');
  const [character, setCharacter] = useState('');
  const [weapon, setWeapon] = useState('');
  const [room, setRoom] = useState('');
  const [paths, setPaths] = useState([]);
  const [selectedPath, setSelectedPath] = useState('');


  // Character and Weapon dropdown data
  const characters = ['Miss Scarlet', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Professor Plum'];
  const weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench'];
  const rooms = ['Ballroom', 'Billiard Room', 'Conservatory', 'Dining Room', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study'];

  useEffect(() => {
    if (socket) {
      socket.on('start_turn', (data) => {
        console.log(data);
        let user = data[username];
        if (user !== undefined){
          setPaths(user.locations); // Populate the paths with data from the server
        }
        //setPaths(user.locations); // Populate the paths with data from the server
      });

      return () => socket.off('start_turn');
    }
  }, [socket]);

  const handlePathChange = (event) => {
    setSelectedPath(event.target.value);
  };

  const handleOpen = (action) => {
    setActionType(action);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    // Reset states
    setCharacter('');
    setWeapon('');
    setRoom('');
  };

  const handleActionSubmit = () => {
    if (!socket) {
      console.error('Socket instance is not available');
      return;
    }

    let emitData = {};

    // For testing until pulling user's location works
    // let room = 'Hall';

    switch (actionType) {
      case 'move':
        emitData = {
          username: username,
          new_loc: selectedPath,
        };
        socket.emit('action_move', emitData);
        break;
      case 'suggestion':
        emitData = {
          username: username,
          character: character,
          weapon: weapon,
          room: room
        };
        socket.emit('action_suggestion', emitData);
        break;
      case 'accusation':
        emitData = {
          username: username,
          character: character,
          weapon: weapon,
          room: room
        };
        console.log(emitData);
        socket.emit('action_accuse', emitData);
        break;
      case 'endTurn':
        // End turn might not need any additional data
        socket.emit('action_turnEnd', { gamecode: gameCode });
        break;
      default:
        console.error('Invalid action type');
    }

    handleClose();
  };

  const handleMove = () => {
    handleOpen('move');
  };

  const handleSuggestion = () => {
    handleOpen('suggestion');
  };

  const handleAccusation = () => {
    handleOpen('accusation');
  };

  const handleEndTurn = () => {
    setActionType('endTurn');
    handleActionSubmit();
  };

  const renderModalContent = () => {
    switch (actionType) {
      case 'move':
        return (
          <div className={classes.paper}>
            <h2 id="transition-modal-title">Move</h2>
            <FormControl className={classes.formControl}>
              <InputLabel htmlFor="path-select">Path</InputLabel>
              <Select
                labelId="path-select"
                id="path-select"
                value={selectedPath}
                onChange={handlePathChange}
              >
                 {paths.map((path) => (
                    <MenuItem key={path} value={path}>{path}</MenuItem>
                  ))}
              </Select>
            </FormControl>
            <Button onClick={handleActionSubmit}>Submit</Button>
          </div>
        );
      case 'suggestion':
        return (
          <div className={classes.paper}>
            <h2 id="transition-modal-title">Select Options</h2>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="character-select-label">Character</InputLabel>
                  <Select
                    labelId="character-select-label"
                    id="character-select"
                    value={character}
                    onChange={(e) => setCharacter(e.target.value)}
                  >
                     {characters.map((character, index) => (
                      <MenuItem key={index} value={character}>
                        {character}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="weapon-select-label">Weapon</InputLabel>
                  <Select
                    labelId="weapon-select-label"
                    id="weapon-select"
                    value={weapon}
                    onChange={(e) => setWeapon(e.target.value)}
                  >
                    {weapons.map((weapon, index) => (
                      <MenuItem key={index} value={weapon}>
                        {weapon}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Button onClick={handleActionSubmit} color="primary">
              Submit
            </Button>
          </div>
        );
      case 'accusation':
        return (
          <div className={classes.paper}>
            <h2 id="transition-modal-title">Select Options</h2>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="character-select-label">Character</InputLabel>
                  <Select
                    labelId="character-select-label"
                    id="character-select"
                    value={character}
                    onChange={(e) => setCharacter(e.target.value)}
                  >
                     {characters.map((character, index) => (
                      <MenuItem key={index} value={character}>
                        {character}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={4}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="weapon-select-label">Weapon</InputLabel>
                  <Select
                    labelId="weapon-select-label"
                    id="weapon-select"
                    value={weapon}
                    onChange={(e) => setWeapon(e.target.value)}
                  >
                    {weapons.map((weapon, index) => (
                      <MenuItem key={index} value={weapon}>
                        {weapon}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={4}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="room-select-label">Room</InputLabel>
                  <Select
                      labelId="room-select-label"
                      id="room-select"
                      value={room}
                      onChange={(e) => setRoom(e.target.value)}
                  >
                      {rooms.map((room, index) => (
                          <MenuItem key={index} value={room}>
                              {room}
                          </MenuItem>
                      ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Button onClick={handleActionSubmit} color="primary">
              Submit
            </Button>
          </div>
        );
    }
    
  };

  return (
    <div>
      <Button variant="contained" color="primary" className={classes.button} onClick={handleMove}>Move</Button>
      <Button variant="contained" color="primary" className={classes.button} onClick={handleSuggestion}>Make a Suggestion</Button>
      <Button variant="contained" color="secondary" className={classes.button} onClick={handleAccusation}>Make an Accusation</Button>
      <Button variant="contained" color="default" className={classes.button} onClick={handleEndTurn}>End Turn</Button>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        className={classes.modal}
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          {renderModalContent()}
        </Fade>
      </Modal>
    </div>
  );
};

export default PlayerActions;
