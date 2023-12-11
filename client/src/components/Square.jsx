import React from "react";
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    square: {
      textAlign: 'center', // Centers the image horizontally
      lineHeight: 0, // Removes extra line height
      padding: theme.spacing(0), // Removes padding
      height: '100%',
      width: '5%',
      borderColor: 'red',
      textAlign: 'center',
    },
    dotRed: {
        height: '100%',
        width: '5%',
        backgroundColor: 'red',
        borderRadius: '50%',
        display: 'inline-block',
    },
    dotBlue: {
        height: '100%',
        width: '5%',
        backgroundColor: 'blue',
        borderRadius: '50%',
        display: 'inline-block',
    },
    dotGreen: {
        height: '100%',
        width: '5%',
        backgroundColor: 'green',
        borderRadius: '50%',
        display: 'inline-block',
    },
    dotYellow: {
        height: '100%',
        width: '5%',
        backgroundColor: 'yellow',
        borderRadius: '50%',
        display: 'inline-block',
    },
    dotPurple: {
        height: '100%',
        width: '5%',
        backgroundColor: 'purple',
        borderRadius: '50%',
        display: 'inline-block',
    },
    dotWhite: {
        height: '100%',
        width: '5%',
        backgroundColor: 'white',
        borderRadius: '50%',
        display: 'inline-block',
    }
  }));

export default function Square({value}) {
    const classes = useStyles();

    if (value === 'red') {
        return (<div className={classes.dotRed}></div>)
    } else if (value === 'blue') {
        return (<div className={classes.dotBlue}></div>)
    } else if (value === 'white') {
        return (<div className={classes.dotWhite}></div>)
    } else if (value === 'purple') {
        return (<div className={classes.dotPurple}></div>)
    } else if (value === 'yellow') {
        return (<div className={classes.dotYellow}></div>)
    } else if (value === 'green') {
        return (<div className={classes.dotGreen}></div>)
    } else {
        return (<div className={classes.square}>{value}</div>)
    }
}