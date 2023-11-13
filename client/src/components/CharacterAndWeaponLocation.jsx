import React, { useState, useEffect } from 'react';
import {
  Box,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  makeStyles,
  Divider,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
    marginTop: theme.spacing(3),
  },
  tableContainer: {
    width: '40%',
    minHeight: '400px',
    marginRight: theme.spacing(2),
  },
  table: {
    maxWidth: 250,
  },
  column: {
    width: '25%',
    maxWidth: '25%',
    whiteSpace: 'normal', // This allows text to wrap
    wordWrap: 'break-word', // Breaks words onto the next line
  },
  headerCell: {
    backgroundColor: theme.palette.primary.dark,
    color: theme.palette.common.white,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  divider: {
    margin: `${theme.spacing(1)}px 0`, // Vertical space around the divider
  },
  cell: {
    padding: theme.spacing(1),
  },
  characterCell: {
    whiteSpace: 'normal',
    wordWrap: 'break-word',
    textAlign: 'center',
  },
}));

const CharacterAndWeaponLocation = ({ socket }) => {
  const classes = useStyles();

  /* Socket.io listener setup
  const [characterData, setUserState] = useState([]);
  const [weaponData, setWeaponState] = useState([]);
  
  useEffect(() => {
    // Set up socket event listener for pop_locations
    socket.on('pop_locations', (data) => {
      const newUserState = data.userState;
      const newWeaponState = data.weaponState;

      // Update your local state with the new data
      setUserState(newUserState);
      setWeaponState(newWeaponState);
    });

    // Clean up the listener when the component unmounts
    return () => {
      socket.off('pop_locations');
    };
  }, [socket]);

  // Map userState to table rows for characters
  const characterRows = Object.entries(characterData).map(([username, details]) => ({
    character: details.character,
    username: username,
    location: details.location,
  }));

  // Map weaponState to table rows for weapons
  const weaponRows = Object.entries(weaponData).map(([weapon, location]) => ({
    weapon,
    location,
  }));
*/

  const characterRowsFake = [
    { character: 'Miss Scarlet', username: 'Saron', location: 'Study' },
    { character: 'Prof. Plum', username: 'Jacob', location: 'Library' },
    { character: 'Col. Mustard', username: 'Nick', location: 'Billiard' },
    { character: 'Miss Scarlet', username: '', location: 'Kitchen' },
    { character: 'Prof. Plum', username: '', location: 'Ballroom' },
    { character: 'Col. Mustard', username: '', location: 'Hallway xyz' },
    // ... Add more rows as needed
  ];

  const weaponRowsFake = [
    { weapon: 'Pipe', location: 'Study' },
    { weapon: 'Knife', location: 'Hall' },
    { weapon: 'Wrench', location: 'Lounge' },
    { weapon: 'Rope', location: 'Library' },
    { weapon: 'Candelstick', location: 'Hall' },
    { weapon: 'Revolver', location: 'Ballroom' },
    // ... Add more rows as needed
  ];

  return (
    <Box className={classes.root}>
      
      {/* Character Location Table */}
      <TableContainer component={Paper} className={classes.tableContainer}>
        <Table className={classes.table} aria-label="character table" size="small">
          <TableHead>
            <TableRow>
              <TableCell csize="small" className={classes.headerCell} >Character</TableCell>
              <TableCell size="small" className={classes.headerCell}>Location</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {characterRowsFake.map((row, index) => (
              <TableRow key={index}>
                <TableCell size="small" className={classes.characterCell}>
                  {row.character}
                  <Divider className={classes.divider} />
                  {row.username}
                </TableCell>
                <TableCell size="small" className={[classes.cell, classes.characterCell]}>{row.location}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      {/* Weapon Location Table */}
      <TableContainer component={Paper} className={classes.tableContainer}>
        <Table className={classes.table} aria-label="weapon table" size="small">
          <TableHead>
            <TableRow>
              <TableCell className={[classes.headerCell, classes.characterCell]}>Weapon</TableCell>
              <TableCell className={[classes.headerCell, classes.characterCell]}>Location</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {weaponRowsFake.map((row, index) => (
              <TableRow key={index}>
                <TableCell className={[classes.cell,classes.characterCell]}>{row.weapon}</TableCell>
                <TableCell className={[classes.cell,classes.characterCell]}>{row.location}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default CharacterAndWeaponLocation;
