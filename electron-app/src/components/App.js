import React, { useState, useEffect, useMemo } from 'react';
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
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  InputAdornment,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import UpdateIcon from '@mui/icons-material/Update';
import SourceIcon from '@mui/icons-material/Source';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';

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

const FilterBar = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(3),
  display: 'flex',
  gap: theme.spacing(2),
  flexWrap: 'wrap',
  alignItems: 'center',
  [theme.breakpoints.down('sm')]: {
    flexDirection: 'column',
    alignItems: 'stretch',
  },
}));

const App = () => {
  const theme = useTheme();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPriority, setSelectedPriority] = useState('all');
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState('desc');

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

  // Extract unique categories and priorities from data
  const categories = useMemo(() => {
    const uniqueCategories = [...new Set(data.map(item => item.category).filter(Boolean))];
    return ['all', ...uniqueCategories];
  }, [data]);

  const priorities = useMemo(() => {
    const uniquePriorities = [...new Set(data.map(item => item.priority).filter(Boolean))];
    return ['all', ...uniquePriorities];
  }, [data]);

  // Filter and sort logic
  const filteredAndSortedData = useMemo(() => {
    return data
      .filter(item => {
        const matchesSearch = searchQuery === '' ||
          item.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.content?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.author?.toLowerCase().includes(searchQuery.toLowerCase());

        const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
        const matchesPriority = selectedPriority === 'all' || item.priority === selectedPriority;

        return matchesSearch && matchesCategory && matchesPriority;
      })
      .sort((a, b) => {
        const order = sortOrder === 'asc' ? 1 : -1;
        
        switch (sortBy) {
          case 'title':
            return order * (a.title || '').localeCompare(b.title || '');
          case 'priority':
            const priorityOrder = { high: 3, medium: 2, low: 1 };
            return order * ((priorityOrder[a.priority] || 0) - (priorityOrder[b.priority] || 0));
          case 'date':
          default:
            const dateA = new Date(a.published_at || a.created_at);
            const dateB = new Date(b.published_at || b.created_at);
            return order * (dateA - dateB);
        }
      });
  }, [data, searchQuery, selectedCategory, selectedPriority, sortBy, sortOrder]);

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
          <>
            <FilterBar elevation={0}>
              <TextField
                placeholder="Search news..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                size="small"
                sx={{ minWidth: 200 }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />

              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Category</InputLabel>
                <Select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  label="Category"
                >
                  {categories.map(category => (
                    <MenuItem key={category} value={category}>
                      {category === 'all' ? 'All Categories' : category}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Priority</InputLabel>
                <Select
                  value={selectedPriority}
                  onChange={(e) => setSelectedPriority(e.target.value)}
                  label="Priority"
                >
                  {priorities.map(priority => (
                    <MenuItem key={priority} value={priority}>
                      {priority === 'all' ? 'All Priorities' : priority}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <Box sx={{ display: 'flex', gap: 1, ml: 'auto' }}>
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Sort by</InputLabel>
                  <Select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    label="Sort by"
                    startAdornment={
                      <InputAdornment position="start">
                        <SortIcon />
                      </InputAdornment>
                    }
                  >
                    <MenuItem value="date">Date</MenuItem>
                    <MenuItem value="title">Title</MenuItem>
                    <MenuItem value="priority">Priority</MenuItem>
                  </Select>
                </FormControl>

                <FormControl size="small" sx={{ minWidth: 100 }}>
                  <InputLabel>Order</InputLabel>
                  <Select
                    value={sortOrder}
                    onChange={(e) => setSortOrder(e.target.value)}
                    label="Order"
                  >
                    <MenuItem value="desc">Newest</MenuItem>
                    <MenuItem value="asc">Oldest</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </FilterBar>

            <Grid container spacing={3}>
              {filteredAndSortedData.length === 0 ? (
                <Grid item xs={12}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <Typography color="text.secondary">
                      No results found for your search criteria.
                    </Typography>
                  </Paper>
                </Grid>
              ) : (
                filteredAndSortedData.map((item, index) => (
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
                ))
              )}
            </Grid>
          </>
        )}
      </Container>
    </Box>
  );
};

export default App; 