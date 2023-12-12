import React, {useState, useEffect} from 'react';
import { makeStyles } from '@material-ui/core';
import Row from './Row';

const useStyles = makeStyles((theme) => ({
    gameBoardContainer: {
      textAlign: 'center', // Centers the image horizontally
      lineHeight: 0, // Removes extra line height
      padding: theme.spacing(0), // Removes padding
      height: '490px',
      maxWidth: '100%', // Ensures the image is not wider than its container
      maxHeight: '100%', // Ensures the image is not taller than its container
      display: 'block', // Removes any inline spacing
      margin: '0 auto', // Centers the image if it's not as wide as its container,
      background: 'red',
      backgroundImage: 'url(/gameBoard.png)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }
}));

export default function GameGrid({socket}) {

    const classes = useStyles();
/*
    const [colors, setColors] = useState({
        row0: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row1: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row2: ['', '', '', '', '', '', '', '', '', 'purple', 'blue', '', '', '', '', '', '', '', '', ''],
        row3: ['', '', 'yellow', 'red', 'purple', '', '', 'yellow', '', 'purple', 'blue', '', '', 'red', '', 'blue', 'green', 'yellow', '', ''],
        row4: ['', '', 'yellow', 'red', 'purple', '', '', '', '', 'purple', 'blue', '', '', '', '', 'blue', 'green', 'yellow', '', ''],
        row5: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row6: ['', '', '', '', 'purple', '', '', '', '', '', 'blue', '', '', '', '', '', 'green', '', '', ''],
        row7: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row8: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row9: ['', '', 'yellow', 'red', 'purple', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row10: ['', '', 'yellow', 'red', 'purple', '', 'blue', '', 'red', 'purple', 'blue', 'green', 'yellow', '', 'purple', '', 'green', 'yellow', '', ''],
        row11: ['', '', 'yellow', 'red', 'purple', '', '', '', '', '', '', '', '', '', '', '', 'green', 'yellow', '', ''],
        row12: ['', '', '', '', '', '', '', '', '', '', 'blue', '', '', '', '', '', '', '', '', ''],
        row13: ['', '', '', '', 'purple', '', '', '', '', '', '', '', '', '', '', '', 'green', '', '', ''],
        row14: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row15: ['', '', '', '', '', '', '', '', '', 'purple', 'blue', 'green', '', '', '', '', '', '', '', ''],
        row16: ['', '', '', '', '', '', '', 'yellow', '', '', '', '', '', '', '', '', '', '', '', ''],
        row17: ['', '', 'yellow', 'red', 'purple', '', '', '', '', '', '', '', '', 'red', '', 'blue', 'green', 'yellow', '', ''],
        row18: ['', '', 'yellow', 'red', 'purple', '', '', '', '', 'purple', 'blue', 'green', '', '', '', 'blue', 'green', 'yellow', '', ''],
        row19: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    });
*/
    const [colors, setColors] = useState({
        row0: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row1: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row2: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row3: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row4: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row5 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row6 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row7 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row8 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row9 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row10 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row11 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row12 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row13 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row14 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row15 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row16 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row17 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row18 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        row19 : ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}
    );

    useEffect(() => {
        if (socket) {
            socket.on('popMapLocations', (data) => {
                setColors(colors => data.colors);
            });
        }
    })
    
    return (
        <>
            <div className={classes.gameBoardContainer}>
                <Row colors={colors.row0}/>
                <Row colors={colors.row1}/>
                <Row colors={colors.row2}/>
                <Row colors={colors.row3}/>
                <Row colors={colors.row4}/>
                <Row colors={colors.row5}/>
                <Row colors={colors.row6}/>
                <Row colors={colors.row7}/>
                <Row colors={colors.row8}/>
                <Row colors={colors.row9}/>
                <Row colors={colors.row10}/>
                <Row colors={colors.row11}/>
                <Row colors={colors.row12}/>
                <Row colors={colors.row13}/>
                <Row colors={colors.row14}/>
                <Row colors={colors.row15}/>
                <Row colors={colors.row16}/>
                <Row colors={colors.row17}/>
                <Row colors={colors.row18}/>
                <Row colors={colors.row19}/>
            </div>
        </>
    );
}