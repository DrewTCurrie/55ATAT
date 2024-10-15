import { Box, Divider, Drawer, List, ListItem, ListItemButton, ListItemText, Typography } from '@mui/material';
import React from 'react';
import { useState, useEffect} from 'react'
import { Link } from 'react-router-dom'

const navItems = [
  {text: 'Scanner', link: '/'},
  {text: 'Events', link:'/events'},
  {text: 'Clients', link:'/clients'},
];

const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
      });
    };

    window.addEventListener('resize', handleResize);

    // Clean up the event listener on component unmount
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

export default function Sidebar() {
  const {width} = useWindowSize();
  const drawerWidth = width * .15;
  return(
      <Box>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" sx={{ my: 2 }}>
              PTC
            </Typography>
            <Divider />
          </Box>
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
        </Drawer>
      </Box>
    );
}