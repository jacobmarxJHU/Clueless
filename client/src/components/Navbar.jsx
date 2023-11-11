import React from 'react';
import { AppBar, Toolbar, Typography, makeStyles } from '@material-ui/core';
import { Link } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  appBar: {
    backgroundColor: theme.palette.primary.dark,
    height: '60px',
    verticalAlign: 'center'
  },
  title: {
    flexGrow: 1,
    fontWeight: 'bold',
    color: theme.palette.common.white,
    textDecoration: 'none',
  },
}));

const Navbar = ({ username }) => {
  const classes = useStyles();

  return (
    <AppBar position="static" className={classes.appBar}>
      <Toolbar>
        <Link to="/" className={classes.title}>
          <Typography variant="h6"><strong>Clue-Less</strong></Typography>
        </Link>
        <Typography variant="subtitle1">{username}</Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
