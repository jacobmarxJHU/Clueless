import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, TextField, Typography, Paper, makeStyles } from '@material-ui/core';
import { io } from "socket.io-client"

const useStyles = makeStyles((theme) => ({
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        padding: 20
    },
    input: {
        marginBottom: 20
    },
    title: {
        marginBottom: 30,
        fontWeight: 'bold'
    },
    header: {
        marginBottom: 20
    },
    appBar: {
        marginBottom: 50
    },
    appName: {
        fontFamily: 'Arial, sans-serif', 
        fontSize: '24px', 
        fontWeight: 'bold',
        cursor: 'pointer',
        flexGrow: 1
    },
    loggedInUsername: {
        marginLeft: 'auto',
        marginRight: 10
    },
}));

const Login = () => {
    const classes = useStyles();
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [gameCode, setGameCode] = useState('');
    const [validationError, setValidationError] = useState('');
    const [message, setMessage] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [socketInstance, setSocketInstance] = useState(null);

    useEffect(() => {
        // Initialize the socket connection here
        const socket = io("http://localhost:5000", {
            transports: ["websocket"],
            upgrade: false,
        });

        setSocketInstance(socket);

        // Event listeners for socket connection
        socket.on("connect", () => {
            console.log("Connected to socket.io server");
            setSocketInstance(socket);
        });

        socket.on("disconnect", () => {
            console.log("Disconnected from socket.io server");
        });

        // Clean up the socket when the component unmounts
        return () => {
            socket.close();
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Input validation
        if (!username.trim()) {
            setValidationError('Username cannot be empty!');
            return;
        } else {
            setValidationError('');
            setIsSubmitted(true);

            // First, check if the user exists using a GET request
            try {
                let data = JSON.stringify({username:username, gameCode:gameCode});
                let dataDict = {username, gameCode};
                const userInfoResponse = await fetch(`/user/${data}`);
                const userInfoData = await userInfoResponse.json();
                
                if (userInfoData && userInfoData.id) {
                    // If user exists
                    socketInstance.emit("user_join", dataDict);
                } else {
                    // If user doesn't exist, register them using a POST request
                    const registerResponse = await fetch('/user', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username })
                    });
                    const registerData = await registerResponse.json();
                    if (registerData && registerData.id) {
                        socketInstance.emit("user_join", dataDict);
                    } else {
                        setMessage('An error occurred. Please try again.');
                    }
                }
            } catch (error) {
                console.error('Failed to fetch user info:', error);
                setValidationError('An error occurred. Please try again.');
            }
        }
    };

    // Listen for the "user_join" event emitted by the server with the gameCode and username
    useEffect(() => {
        if (socketInstance) {
            socketInstance.on("pass_game", (updatedData) => {
                console.log(updatedData);
                navigate(`/game/${updatedData.gameCode}`, {
                    state: { 
                        username: updatedData.username, 
                        isLeader: updatedData.isLeader
                    }
                  });
            });
        }
    }, [socketInstance, navigate]);

    return (
        <Paper className={classes.container}>
            <Typography variant="h4" className={classes.title}>Clue-Less</Typography>
            <Typography variant="h5" className={classes.header}>Login</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    className={classes.input}
                    label="Username"
                    variant="outlined"
                    fullWidth
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    className={classes.input}
                    label="Game Code"
                    variant="outlined"
                    fullWidth
                    value={gameCode}
                    onChange={(e) => setGameCode(e.target.value)}
                />
                {validationError && (
                    <Typography color="error">{validationError}</Typography>
                )}
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Login/Register
                </Button>
            </form>
        </Paper>
    );
};

export default Login;
