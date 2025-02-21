import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  AppBar,
  Toolbar,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Chip,
  Avatar,
  Stack,
  Divider,
  useTheme,
  IconButton,
  Tooltip,
  Link,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import UpdateIcon from '@mui/icons-material/Update';
import SourceIcon from '@mui/icons-material/Source';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

const StyledPaper = styled(Paper)(({ theme }) => ({
  p: 0,
  display: 'flex',
  flexDirection: 'column',
  height: 'auto',
  minHeight: 320,
  position: 'relative',
  overflow: 'hidden',
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

const ContentContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  display: 'flex',
  flexDirection: 'column',
  flexGrow: 1,
}));

const ImageContainer = styled(Box)(({ theme }) => ({
  height: 200,
  width: '100%',
  overflow: 'hidden',
  position: 'relative',
  '&::after': {
    content: '""',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: '40px',
    background: 'linear-gradient(to top, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 100%)',
  },
  '& img': {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transition: 'transform 0.3s ease-in-out',
  },
  '&:hover img': {
    transform: 'scale(1.05)',
  },
}));

const CategoryChip = styled(Chip)(({ theme }) => ({
  position: 'absolute',
  top: theme.spacing(2),
  left: theme.spacing(2),
  zIndex: 1,
  backgroundColor: 'rgba(255, 255, 255, 0.9)',
  backdropFilter: 'blur(4px)',
}));

const PriorityChip = styled(Chip)(({ theme, priority }) => ({
  backgroundColor: priority === 'high' ? theme.palette.error.light :
                  priority === 'medium' ? theme.palette.warning.light :
                  theme.palette.success.light,
  color: theme.palette.getContrastText(
    priority === 'high' ? theme.palette.error.light :
    priority === 'medium' ? theme.palette.warning.light :
    theme.palette.success.light
  ),
}));

const TruncatedTypography = styled(Typography)({
  overflow: 'hidden',
  textOverflow: 'ellipsis',
  display: '-webkit-box',
  WebkitLineClamp: 3,
  WebkitBoxOrient: 'vertical',
});

const MetaInfo = styled(Stack)(({ theme }) => ({
  flexDirection: 'row',
  alignItems: 'center',
  gap: theme.spacing(0.5),
  color: theme.palette.text.secondary,
  '& svg': {
    fontSize: '1rem',
  },
}));

const SourceLink = styled(Link)(({ theme }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: theme.spacing(0.5),
  color: theme.palette.primary.main,
  textDecoration: 'none',
  '&:hover': {
    textDecoration: 'underline',
    '& .MuiSvgIcon-root': {
      transform: 'translateY(-1px)',
    },
  },
  '& .MuiSvgIcon-root': {
    fontSize: '1rem',
    transition: 'transform 0.2s ease-in-out',
  },
}));

const App = () => {
  const theme = useTheme();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/messages/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const jsonData = await response.json();
        console.log('API Response:', jsonData);
        if (!Array.isArray(jsonData)) {
          console.log('Response type:', typeof jsonData);
          if (jsonData.results && Array.isArray(jsonData.results)) {
            setData(jsonData.results);
          } else {
            throw new Error('Expected an array of messages from the server');
          }
        } else {
          setData(jsonData);
        }
        setLoading(false);
      } catch (err) {
        console.error('Fetch error:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSourceClick = (url, event) => {
    event.preventDefault();
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <Box sx={{ flexGrow: 1, bgcolor: 'grey.50', minHeight: '100vh' }}>
      <AppBar position="static" elevation={0} sx={{ bgcolor: 'white', color: 'primary.main' }}>
        <Toolbar>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            InfoSphere Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
            <CircularProgress />
          </Box>
        ) : error ? (
          <Paper sx={{ p: 3, backgroundColor: '#fff3f3' }}>
            <Typography color="error">Error: {error}</Typography>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {data && data.map((item, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <StyledPaper>
                  {item.image_url ? (
                    <ImageContainer>
                      <img src={item.image_url} alt={item.title} />
                      {item.category && (
                        <CategoryChip 
                          label={item.category}
                          size="small"
                        />
                      )}
                    </ImageContainer>
                  ) : (
                    item.category && (
                      <Box sx={{ pt: 2, px: 2 }}>
                        <CategoryChip 
                          label={item.category}
                          size="small"
                        />
                      </Box>
                    )
                  )}
                  
                  <ContentContainer>
                    <Stack direction="row" spacing={1} mb={2}>
                      {item.priority && (
                        <PriorityChip 
                          icon={<PriorityHighIcon />}
                          label={item.priority}
                          size="small"
                          priority={item.priority.toLowerCase()}
                        />
                      )}
                      <Chip 
                        icon={item.is_read ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon />}
                        label={item.is_read ? "Read" : "Unread"}
                        size="small"
                        sx={{
                          bgcolor: item.is_read ? 'success.50' : 'grey.100',
                          color: item.is_read ? 'success.main' : 'text.secondary',
                        }}
                      />
                    </Stack>

                    <Typography 
                      variant="h6" 
                      gutterBottom 
                      sx={{ 
                        fontWeight: 600,
                        fontSize: '1.1rem',
                        mb: 2,
                        lineHeight: 1.3,
                      }}
                    >
                      {item.title}
                    </Typography>

                    <TruncatedTypography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ mb: 2 }}
                    >
                      {item.content}
                    </TruncatedTypography>

                    <Box sx={{ mt: 'auto' }}>
                      <Divider sx={{ my: 2 }} />

                      {item.author && (
                        <Stack direction="row" spacing={1} alignItems="center" mb={2}>
                          <Avatar 
                            sx={{ 
                              width: 32, 
                              height: 32,
                              bgcolor: 'primary.main',
                              fontSize: '0.9rem',
                            }}
                          >
                            {item.author.charAt(0)}
                          </Avatar>
                          <Typography variant="body2" fontWeight={500}>
                            {item.author}
                          </Typography>
                        </Stack>
                      )}

                      <Stack spacing={1}>
                        {item.source_name && (
                          <MetaInfo>
                            <SourceIcon />
                            {item.url ? (
                              <SourceLink
                                href={item.url}
                                onClick={(e) => handleSourceClick(item.url, e)}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                {item.source_name}
                                <OpenInNewIcon />
                              </SourceLink>
                            ) : (
                              <Typography variant="caption">
                                {item.source_name}
                              </Typography>
                            )}
                          </MetaInfo>
                        )}
                        
                        <MetaInfo>
                          <CalendarTodayIcon />
                          <Typography variant="caption">
                            Published: {item.published_at 
                              ? new Date(item.published_at).toLocaleDateString('de-DE', {
                                  year: 'numeric',
                                  month: 'long',
                                  day: 'numeric'
                                })
                              : new Date(item.created_at).toLocaleDateString('de-DE', {
                                  year: 'numeric',
                                  month: 'long',
                                  day: 'numeric'
                                })}
                          </Typography>
                        </MetaInfo>

                        {item.updated_at && new Date(item.updated_at).getTime() !== new Date(item.created_at).getTime() && (
                          <MetaInfo>
                            <UpdateIcon />
                            <Typography variant="caption">
                              Updated: {new Date(item.updated_at).toLocaleDateString('de-DE', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                              })}
                            </Typography>
                          </MetaInfo>
                        )}
                      </Stack>
                    </Box>
                  </ContentContainer>
                </StyledPaper>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </Box>
  );
};

export default App; 