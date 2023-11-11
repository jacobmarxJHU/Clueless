import React from 'react';
import { Paper, Typography, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  banner: {
    padding: theme.spacing(1),
    backgroundColor: '#F3F6F9',
    textAlign: 'center',
    width: '10%',
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    marginLeft: 'auto',
    marginRight: 'auto', 
  },
}));

const GameStatusBanner = ({ status }) => {
  const classes = useStyles();

  return (
    <Paper elevation={4} className={classes.banner}>
      <Typography variant="subtitle1"><strong>{status}</strong></Typography>
    </Paper>
  );
};

export default GameStatusBanner;
