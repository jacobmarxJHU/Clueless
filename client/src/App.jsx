import React, { useState, useEffect } from 'react';
import { Button, TextField, Typography, Paper, AppBar, Toolbar, makeStyles, List, ListItem, Divider, Box, ListItemIcon, Icon } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';
import UserContext from './UserContext';  // assuming the UserContext is in the same directory
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
    chatBox: {
        marginTop: theme.spacing(2),
        maxHeight: '300px',
        overflow: 'auto',
        padding: theme.spacing(2),
        backgroundColor: '#F3F6F9'
    },
    chatMessage: {
        listStyleType: 'disc',
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(1),
        borderRadius: theme.spacing(1),
        marginBottom: theme.spacing(1),
    }
}));

function App() {
    const classes = useStyles();
    const { user, setUser } = React.useContext(UserContext);
    const [username, setUsername] = useState('');
    const [message, setMessage] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [validationError, setValidationError] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);

    const [gameCode, setGameCode] = useState('');
    const [socketInstance, setSocketInstance] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Input validation
        if (!username.trim()) {
            setValidationError('Username cannot be empty!');
            return;
        } else {
            setValidationError('');
        }
        let data = JSON.stringify({username:username, gameCode:gameCode})
        // First, check if the user exists using a GET request
        const userInfoResponse = await fetch(`/user/${data}`);
        const userInfoData = await userInfoResponse.json();
        

        if (userInfoData && userInfoData.id) {
            // If user exists
            setMessage(`Welcome back, ${userInfoData.username}! Your ID is ${userInfoData.id}`);
            setUser(userInfoData.username);
            setGameCode(userInfoData.gameCode);
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
                setMessage(`Welcome, ${registerData.username}! Your ID is ${registerData.id}`);
                setUser(registerData.username);
            } else {
                setMessage('An error occurred. Please try again.');
            }
        }

        setIsSubmitted(true);
        
        const socket = io("localhost:5000/", {
        transports: ["websocket"],
        cors: {
            origin: "http://localhost:3000/",
        },
        });
    
        setSocketInstance(socket);


        let updated_data = JSON.stringify({username:username, gameCode:gameCode})

        socket.on("connect", () => {
            socket.emit("user_join", updated_data)
            console.log(updated_data);
        });
    }

    useEffect(() => {
        if (socketInstance) {
            socketInstance.on("pass_game", function(data) {
                setChatMessages(prevMessages => [...prevMessages, `Game Code: ${data["gameCode"]}`]);
            });
    
            socketInstance.on("join_room", function(data) {
                setChatMessages(prevMessages => [...prevMessages, `${data["username"]} has joined the game`]);
            });
    
            socketInstance.on("leave_room", function(data) {
                setChatMessages(prevMessages => [...prevMessages, `${data["username"]} has left the game`]);
            });
        }
    
        // Clean up the listener when the component is unmounted or when socketInstance changes.
        return () => {
            if (socketInstance) {
                socketInstance.off("pass_game");
                socketInstance.off("join_room");
                socketInstance.off("leave_room");
            }
        };
    }, [socketInstance]);
    

    return (
        <div>
        <AppBar position="static" className={classes.appBar}>
            <Toolbar>
                <a href="/" style={{ textDecoration: 'none', color: 'white' }}>
                    <Typography variant="h6" className={classes.appName}>Clue-Less</Typography>
                </a>
                {user && (
                    <Typography variant="subtitle1" className={classes.loggedInUsername}>
                        {user}
                    </Typography>
                )}
            </Toolbar>
        </AppBar>
        <Paper className={classes.container}>
            <Typography variant="h4" className={classes.title}>Clue-Less</Typography>
            <Typography variant="h5" className={classes.header}>Login</Typography>

            {!isSubmitted ? (
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
                    {validationError && <Typography color="error">{validationError}</Typography>}
                    <Button type="submit" variant="contained" color="primary" fullWidth>
                        Login/Register
                    </Button>
                </form>
            ) : null}

            {message && <Typography variant="h6" style={{ marginTop: 20 }}>{message}</Typography>}

            {/* Chat Box */}
            {isSubmitted && (
                <div className={classes.chatBox}>
                    <Typography variant="h6">Event Log</Typography>
                    <List>
                        {chatMessages.map((chatMessage, idx) => (
                            <ListItem key={idx} className={classes.chatMessage}>
                                <ListItemIcon>
                                    <ChatIcon color="primary" />
                                </ListItemIcon>
                                <Typography variant="body1">{chatMessage}</Typography>
                            </ListItem>
                        ))}
                    </List>
                </div>
            )}

        </Paper>

      </div>
    );
}

export default App;
