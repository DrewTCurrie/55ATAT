import * as React from "react";
import {useState} from 'react';
import {Box,Typography,TextField,Button} from '@mui/material'
import { useAuth } from "../funcitons/AuthProvider";


//https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5 Template to build this off of


export default function Login(){
    //Hook for Credentials Object to be passed to AuthProvider
    const [credentials, setCredentials] = useState({
      username: '',
      password: ''
    });

    //Input Change handler
    const handleChnage = (event: React.ChangeEvent<HTMLInputElement>) => {
      const {name, value} = event.target;
      setCredentials((prev) => ({
        ...prev,
        [name]: value,
      }));
    };

    //Loading and Error Handling
    const [error, setError] = useState('')
    const [success, setSuccess] = useState(false)
    const [loading, setLoading] = useState(false)

    //Initialize authProvider as auth
    const auth = useAuth();
    //Submit Handler.
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
      setLoading(true)
      event.preventDefault();
      if(credentials.username !== '' && credentials.password !== ''){
        const loginError = await auth?.attemptLogin(credentials) //only returns error messages.
        if(loginError){
          setError(loginError);
          setSuccess(false)
        } else {
          setSuccess(true)
          setError('')
        }
        
      }
      setLoading(false)
    }


    return(
    <Box
      sx={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f0f0f0',
      }}
    >
      <Box
        sx={{
          padding: '2rem',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
          minWidth: '300px',
        }}
      >
        <Typography variant="h5" component="h1" gutterBottom color='black'>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Username"
            name="username"
            variant="outlined"
            fullWidth
            margin="normal"
            value={credentials.username}
            onChange={handleChnage}
            required
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={credentials.password}
            onChange={handleChnage}
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ marginTop: '1rem',mb:'.4rem' }}
            disabled={loading}
          >
            {loading ? 'Loading' : 'Login'}
          </Button>
          {success ? <Typography variant="h6" color='green'>Login Successful</Typography> : ''}
          {error ? <Typography variant="h6" color='red'>{error}</Typography> : ''}
        </form>
      </Box>
    </Box>
    )
}