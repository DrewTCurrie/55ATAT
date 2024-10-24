import { AppBar, Box, Divider, Drawer, IconButton, List, ListItem, ListItemButton, ListItemText, Toolbar, Typography } from '@mui/material';
import React from 'react';
import { useState, useEffect} from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../functions/AuthProvider';
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import MenuIcon from '@mui/icons-material/Menu';
import { Height } from '@mui/icons-material';
const navItems = [
  {text: 'Scanner', link: '/'},
  {text: 'Events', link:'/events'},
  {text: 'Attendees', link:'/clients'},
];

//This looks to get the window size on load of the side bar, and adjusts it as such.
const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);

    // Clean up the event listener on component unmount
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

export default function Sidebar() {
  //Set the drawer width as 15% of the window.
  const {width, height} = useWindowSize();
  const drawerWidth = width * .15;
  const drawerHeight = height * .08;

  //Add open/closing logic
  const [open, setOpen] = useState(false);
  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  }

  //Initialize authProvider as auth for Admin Initials
  const auth = useAuth();

  return(
      <Box sx={{mb: 4}}>
        <AppBar position="fixed" sx={{maxHeight: drawerHeight}}>
          <Toolbar>
            <IconButton
              aria-label="open drawer"
              onClick={toggleDrawer(true)}
              edge='start'
              sx={[
                {
                  mr: 2,
                },
                open && { display: 'none' },
              ]}
            >
              <MenuIcon sx={{color: 'white'}}/>
              <Typography variant="body1" sx={{ ml: "1rem", color:'white'}}>
                Open Sidebar
              </Typography>
            </IconButton>
            <Box sx={{flexGrow: 1}}/>
            <Typography variant="h6" noWrap component="div">
              Peach Tree Pediatric Attendance Tracker
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          sx={[{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            }}]
          }
          open={open}
          onClose={toggleDrawer(false)}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" sx={{ my: 2 }}>
              PTC
            </Typography>
            <Divider />
          </Box>
          <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            height: '100%',
          }}>
            <Box sx={{ overflow: 'auto' }}>
            <List>
                {navItems.map((item) => (
                  <ListItem key={item.text} disablePadding>
                    <ListItemButton component={Link} to={item.link} sx={{ textAlign: 'center' }}>
                      <ListItemText primary={item.text} />
                    </ListItemButton>
                  </ListItem>
                ))}
            </List>
            </Box>
            <Box
            sx={{
              padding:2,
              textAlign:'center'
            }}>
              {auth?.adminInitials ? 
                    <Typography sx={{mb:'.4rem'}}>{`Welcome, ${auth?.adminInitials}`}</Typography>: "" }
                <Divider/>
                <List>
                  <ListItemButton component={Link} to={`/settings`} sx={{ textAlign: 'center' }}>
                    <ListItemText primary={`Settings`}/>
                  </ListItemButton>
                {auth?.adminInitials ?
                  <ListItemButton onClick={auth?.logOut} sx={{ textAlign: 'center' }}>
                    <ListItemText primary={`Logout`}/>
                  </ListItemButton> 
                : <ListItemButton component={Link} to={`/login`} sx={{ textAlign: 'center' }}>
                    <ListItemText primary={`Login`}/>
                  </ListItemButton>
                }
                </List>
            </Box>
          </Box>
        </Drawer>
      </Box>
    );
}