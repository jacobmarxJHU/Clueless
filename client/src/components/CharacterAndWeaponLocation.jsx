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
    maxHeight: '400px', // Set a fixed height
    overflow: 'auto', // Enable scrolling
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

  /* Socket.io listener setup */
  const [characterData, setUserState] = useState([]);
  const [weaponData, setWeaponState] = useState([]);
  
  useEffect(() => {
    console.log('Received socket in CharacterAndWeaponLocation.jsx:', socket);
    // Set up socket event listener for pop_locations
    if (socket) {
      socket.on('pop_locations', (data) => {
        const newUserState = data.userState;
        const newWeaponState = data.weaponState;
  
        // Update your local state with the new data
        setUserState(newUserState);
        setWeaponState(newWeaponState);
      });

      // Clean up the event listener when the component unmounts
      // or if the socket instance changes
      return () => {
        socket.off('pop_locations');
      };
    }
  }, [socket]); // Only re-run the effect if the socket instance changes

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
            {characterRows.map((row, index) => (
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
            {weaponRows.map((row, index) => (
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
