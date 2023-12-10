import React, { useState } from 'react';
import {
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Checkbox,
  makeStyles,
  Typography,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  // header: {
  //   textAlign: 'center',
  //   padding: theme.spacing(2),
  // },
  tableCell: {
    borderBottom: 'none',
    fontWeight: 'bold',
  },
  header: {
    textAlign: 'center',
    padding: theme.spacing(2),
  },
  table: {
    minWidth: 650,
  },
  notebookHeader: {
    padding: theme.spacing(2),
    backgroundColor: theme.palette.background.paper,
    textAlign: 'center',
  },
  strikethrough: {
    textDecoration: 'line-through',
    color: 'grey',
  },
  columnHeader: {
    fontWeight: 'bold',
  },
}));

const PlayerNotebook = ({  characters, weapons, rooms }) => {
  const classes = useStyles();

  // States for checkboxes
  const [checkedCharacters, setCheckedCharacters] = useState({});
  const [checkedWeapons, setCheckedWeapons] = useState({});
  const [checkedLocations, setCheckedLocations] = useState({});

  // Handlers to toggle the checkbox
  const handleToggle = (category, item) => {
    const toggle = (checkedItems) => ({
      ...checkedItems,
      [item]: !checkedItems[item],
    });

    if (category === 'character') {
      setCheckedCharacters((current) => toggle(current));
    } else if (category === 'weapon') {
      setCheckedWeapons((current) => toggle(current));
    } else if (category === 'location') {
      setCheckedLocations((current) => toggle(current));
    }
  };

  return (
    <TableContainer component={Paper}>
      <Typography variant="h6" className={classes.header}>
        My Detective Notebook
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell className={classes.tableCell}>Character</TableCell>
            <TableCell className={classes.tableCell}>Weapon</TableCell>
            <TableCell className={classes.tableCell}>Location</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {[...Array(Math.max(characters.length, weapons.length, rooms.length))].map((_, index) => (
            <TableRow key={index}>
              <TableCell style={{ borderBottom:'none' }}>
                {characters[index] && (
                  <div>
                    <Checkbox
                      checked={!!checkedCharacters[characters[index]]}
                      onChange={() => handleToggle('character', characters[index])}
                      defaultChecked color="default"
                    />
                    <span className={checkedCharacters[characters[index]] ? classes.strikethrough : null}>
                      {characters[index]}
                    </span>
                  </div>
                )}
              </TableCell>
              <TableCell style={{ borderBottom:'none' }}>
                {weapons[index] && (
                  <div>
                    <Checkbox
                      checked={!!checkedWeapons[weapons[index]]}
                      onChange={() => handleToggle('weapon', weapons[index])}
                      defaultChecked color="default" 
                    />
                    <span className={checkedWeapons[weapons[index]] ? classes.strikethrough : null}>
                      {weapons[index]}
                    </span>
                  </div>
                )}
              </TableCell>
              <TableCell style={{ borderBottom:'none' }}>
                {rooms[index] && (
                  <div>
                    <Checkbox
                      checked={!!checkedLocations[rooms[index]]}
                      onChange={() => handleToggle('location', rooms[index])}
                      defaultChecked color="default"
                    />
                    <span className={checkedLocations[rooms[index]] ? classes.strikethrough : null}>
                      {rooms[index]}
                    </span>
                  </div>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PlayerNotebook;

