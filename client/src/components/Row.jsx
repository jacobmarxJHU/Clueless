import React from "react";
import Square from "./Square";
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    row: {
        display: 'flex',
        flexDirection: 'row',
        flexDirection: 'row',
        height: '5%',
        width:'100%',
    },
  }));

export default function Row({colors}) {
    const classes = useStyles();

    if (colors === undefined) {
        colors = ['', '', '', '', '','', '', '', '', '','', '', '', '', '','', '', '', '', '']
    }
    
    return (
        <div className={classes.row}>
            <Square value={colors[0]} />
            <Square value={colors[1]} />
            <Square value={colors[2]} />
            <Square value={colors[3]} />
            <Square value={colors[4]} />
            <Square value={colors[5]} />
            <Square value={colors[6]} />
            <Square value={colors[7]} />
            <Square value={colors[8]} />
            <Square value={colors[9]} />
            <Square value={colors[10]} />
            <Square value={colors[11]} />
            <Square value={colors[12]} />
            <Square value={colors[13]} />
            <Square value={colors[14]} />
            <Square value={colors[15]} />
            <Square value={colors[16]} />
            <Square value={colors[17]} />
            <Square value={colors[18]} />
            <Square value={colors[19]} />
        </ div>
    )
}