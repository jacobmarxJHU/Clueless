import React from 'react';
import {
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Typography,
  makeStyles,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  tableContainer: {
    maxHeight: 300, // Set a fixed maximum height for scrollable content
    maxWidth: 550, // Adjust the width as necessary
    overflowY: 'auto', // Add vertical scroll
    minHeight: 380,
  },
  table: {
    minWidth: 300, // Adjust the width as necessary
  },
  headerCell: {
    backgroundColor: theme.palette.primary.light, // Use theme colors for consistency
    color: theme.palette.common.white,
    fontWeight: 'bold', // Make the header text bold
  },
  header: {
    padding: theme.spacing(2), // Example padding
    backgroundColor: theme.palette.background.default, // Sets the background color
    color: theme.palette.text.primary, // Sets the text color
    // Add any other styles you wish to apply to the header
  },
}));

const CharacterAndWeaponLocation = ({ rooms }) => {
  const classes = useStyles();

  return (
    <div>
      <Typography variant="h6" component="h2" className={classes.header}>
        Board State
      </Typography>
      <TableContainer component={Paper} className={classes.tableContainer}>
        <Table stickyHeader className={classes.table} size="small" aria-label="character and weapon locations">
          <TableHead>
            <TableRow>
              <TableCell className={classes.headerCell}>Room</TableCell>
              <TableCell className={classes.headerCell}>Character</TableCell>
              <TableCell className={classes.headerCell}>Weapon</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rooms.map((room) => (
              <TableRow key={room.id}>
                <TableCell>{room.room}</TableCell>
                <TableCell>{room.character}</TableCell>
                <TableCell>{room.weapon}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default CharacterAndWeaponLocation;