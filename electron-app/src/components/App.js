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
  Alert,
  Fade,
} from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import UpdateIcon from '@mui/icons-material/Update';
import SourceIcon from '@mui/icons-material/Source';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';
import FilterListIcon from '@mui/icons-material/FilterList';

// Styled Components
const StyledPaper = styled(Paper)(({ theme, hasImage }) => ({
  p: 0,
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  minHeight: hasImage ? 420 : 280,
  position: 'relative',
  overflow: 'hidden',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  backgroundColor: theme.palette.background.paper,
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 24px ${alpha(theme.palette.primary.main, 0.1)}`,
  },
}));

const ContentContainer = styled(Box)(({ theme, hasImage }) => ({
  padding: theme.spacing(3),
  display: 'flex',
  flexDirection: 'column',
  flexGrow: 1,
  gap: theme.spacing(2),
  height: '100%',
  position: 'relative',
  ...(hasImage ? {} : {
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      height: '4px',
      background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    }
  })
}));

const ImageContainer = styled(Box)(({ theme }) => ({
  height: 200,
  width: '100%',
  overflow: 'hidden',
  position: 'relative',
  backgroundColor: alpha(theme.palette.primary.main, 0.05),
  '&::after': {
    content: '""',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: '40px',
    background: `linear-gradient(to top, ${alpha(theme.palette.common.black, 0.4)} 0%, transparent 100%)`,
  },
  '& img': {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  '&:hover img': {
    transform: 'scale(1.05)',
  },
}));

const CategoryChip = styled(Chip)(({ theme, hasImage }) => ({
  position: 'relative',
  marginBottom: theme.spacing(1),
  backgroundColor: alpha(theme.palette.background.paper, 1),
  border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
  transition: 'all 0.2s ease-in-out',
  '&:hover': {
    backgroundColor: alpha(theme.palette.background.paper, 1),
    transform: 'scale(1.05)',
    border: `1px solid ${alpha(theme.palette.primary.main, 0.4)}`,
  },
}));

const PriorityChip = styled(Chip)(({ theme, priority }) => {
  const getColor = () => {
    switch (priority) {
      case 'high':
        return theme.palette.error;
      case 'medium':
        return theme.palette.warning;
      default:
        return theme.palette.success;
    }
  };
  const color = getColor();
  
  return {
    backgroundColor: alpha(color.main, 0.1),
    color: color.main,
    borderColor: alpha(color.main, 0.3),
    '&:hover': {
      backgroundColor: alpha(color.main, 0.2),
    },
  };
});

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
  fontSize: '0.875rem',
  '& svg': {
    fontSize: '1rem',
  },
}));

const SourcesContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  gap: theme.spacing(1),
  marginTop: theme.spacing(1.5),
  paddingTop: theme.spacing(1.5),
  borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
}));

const SourceLink = styled(Link)(({ theme }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: theme.spacing(1),
  color: theme.palette.primary.main,
  textDecoration: 'none',
  fontSize: '0.875rem',
  fontWeight: 500,
  padding: theme.spacing(0.75, 1.5),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.primary.main, 0.05),
  transition: 'all 0.2s ease-in-out',
  '&:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
    color: theme.palette.primary.dark,
    textDecoration: 'none',
    transform: 'translateY(-1px)',
    '& .MuiSvgIcon-root:last-child': {
      transform: 'translateX(2px)',
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
  backgroundColor: alpha(theme.palette.background.paper, 0.8),
  backdropFilter: 'blur(8px)',
  [theme.breakpoints.down('sm')]: {
    flexDirection: 'column',
    alignItems: 'stretch',
  },
}));

const SearchTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    backgroundColor: theme.palette.background.paper,
    transition: 'all 0.2s ease-in-out',
    '&:hover': {
      backgroundColor: alpha(theme.palette.primary.main, 0.02),
    },
    '&.Mui-focused': {
      backgroundColor: theme.palette.background.paper,
      '& .MuiOutlinedInput-notchedOutline': {
        borderColor: theme.palette.primary.main,
        borderWidth: 2,
      },
    },
  },
}));

// Main App Component
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
        if (!Array.isArray(jsonData)) {
          if (jsonData.results && Array.isArray(jsonData.results)) {
            setData(jsonData.results);
          } else {
            throw new Error('Expected an array of messages from the server');
          }
        } else {
          setData(jsonData);
        }
      } catch (err) {
        console.error('Fetch error:', err);
        setError(err.message);
      } finally {
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
    <Box sx={{ 
      flexGrow: 1, 
      bgcolor: 'grey.50', 
      minHeight: '100vh',
      pb: 4
    }}>
      <AppBar 
        position="sticky" 
        elevation={0} 
        sx={{ 
          bgcolor: alpha(theme.palette.background.paper, 0.8),
          backdropFilter: 'blur(8px)',
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Toolbar>
          <Typography 
            variant="h5" 
            component="div" 
            sx={{ 
              flexGrow: 1, 
              fontWeight: 600,
              background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            InfoSphere
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {error && (
          <Alert 
            severity="error" 
            sx={{ mb: 3 }}
            onClose={() => setError(null)}
          >
            {error}
          </Alert>
        )}

        <FilterBar>
          <SearchTextField
            fullWidth
            placeholder="Search messages..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
            }}
            sx={{ flexGrow: 1 }}
          />

          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Category</InputLabel>
            <Select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              label="Category"
              startAdornment={
                <InputAdornment position="start">
                  <FilterListIcon fontSize="small" />
                </InputAdornment>
              }
            >
              {categories.map(category => (
                <MenuItem key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Priority</InputLabel>
            <Select
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              label="Priority"
              startAdornment={
                <InputAdornment position="start">
                  <PriorityHighIcon fontSize="small" />
                </InputAdornment>
              }
            >
              {priorities.map(priority => (
                <MenuItem key={priority} value={priority}>
                  {priority.charAt(0).toUpperCase() + priority.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Sort by</InputLabel>
            <Select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              label="Sort by"
              startAdornment={
                <InputAdornment position="start">
                  <SortIcon fontSize="small" />
                </InputAdornment>
              }
            >
              <MenuItem value="date">Date</MenuItem>
              <MenuItem value="title">Title</MenuItem>
              <MenuItem value="priority">Priority</MenuItem>
            </Select>
          </FormControl>

          <Tooltip title="Toggle sort order">
            <IconButton 
              onClick={() => setSortOrder(order => order === 'asc' ? 'desc' : 'asc')}
              sx={{ 
                transform: `rotate(${sortOrder === 'asc' ? 0 : 180}deg)`,
                transition: 'transform 0.2s ease-in-out',
              }}
            >
              <UpdateIcon />
            </IconButton>
          </Tooltip>
        </FilterBar>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : filteredAndSortedData.length === 0 ? (
          <Paper 
            sx={{ 
              p: 4, 
              textAlign: 'center',
              backgroundColor: alpha(theme.palette.background.paper, 0.8),
              backdropFilter: 'blur(8px)',
            }}
          >
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No messages found
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Try adjusting your search criteria or filters
            </Typography>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {filteredAndSortedData.map((item, index) => {
              const hasImage = Boolean(item.image_url);
              
              return (
                <Fade 
                  in={true} 
                  timeout={300} 
                  style={{ transitionDelay: `${index * 50}ms` }}
                  key={item.id}
                >
                  <Grid item xs={12} sm={6} md={4}>
                    <StyledPaper hasImage={hasImage}>
                      {hasImage && (
                        <ImageContainer>
                          <img 
                            src={item.image_url} 
                            alt={item.title}
                            onError={(e) => {
                              e.target.onerror = null;
                              e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24"%3E%3Cpath fill="%23ccc" d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/%3E%3C/svg%3E';
                            }}
                          />
                        </ImageContainer>
                      )}
                      <ContentContainer hasImage={hasImage}>
                        <Stack spacing={2} sx={{ height: '100%' }}>
                          <Box>
                            {item.category && (
                              <CategoryChip
                                label={item.category}
                                size="small"
                                icon={<SourceIcon />}
                                hasImage={hasImage}
                              />
                            )}
                            <Typography 
                              variant="h6" 
                              gutterBottom 
                              sx={{ 
                                fontWeight: 600,
                                fontSize: hasImage ? '1.125rem' : '1.25rem',
                                lineHeight: 1.3,
                              }}
                            >
                              {item.title}
                            </Typography>
                            <TruncatedTypography 
                              variant="body2" 
                              color="text.secondary"
                              sx={{
                                WebkitLineClamp: hasImage ? 3 : 4,
                              }}
                            >
                              {item.content}
                            </TruncatedTypography>
                          </Box>

                          <Box sx={{ mt: 'auto' }}>
                            <Stack 
                              direction="row" 
                              spacing={1} 
                              alignItems="center"
                              flexWrap="wrap"
                              sx={{ mb: 1 }}
                            >
                              {item.priority && (
                                <PriorityChip
                                  label={item.priority}
                                  size="small"
                                  priority={item.priority}
                                  variant="outlined"
                                />
                              )}
                              <MetaInfo>
                                <CalendarTodayIcon />
                                <Typography variant="caption">
                                  {new Date(item.published_at || item.created_at).toLocaleDateString()}
                                </Typography>
                              </MetaInfo>
                            </Stack>

                            <SourcesContainer>
                              <Stack direction="column" spacing={1}>
                                {/* Hauptquelle */}
                                {item.url && (
                                  <SourceLink
                                    href={item.url}
                                    onClick={(e) => handleSourceClick(item.url, e)}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    <SourceIcon />
                                    <Box component="span" sx={{ flexGrow: 1 }}>
                                      {item.source_name || 'Original Source'}
                                    </Box>
                                    <OpenInNewIcon />
                                  </SourceLink>
                                )}
                                
                                {/* Alternative URL */}
                                {item.source_url && item.source_url !== item.url && (
                                  <SourceLink
                                    href={item.source_url}
                                    onClick={(e) => handleSourceClick(item.source_url, e)}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    <SourceIcon />
                                    <Box component="span" sx={{ flexGrow: 1 }}>
                                      {item.source_name || 'Alternative Source'}
                                    </Box>
                                    <OpenInNewIcon />
                                  </SourceLink>
                                )}

                                {/* Link */}
                                {item.link && item.link !== item.url && item.link !== item.source_url && (
                                  <SourceLink
                                    href={item.link}
                                    onClick={(e) => handleSourceClick(item.link, e)}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    <SourceIcon />
                                    <Box component="span" sx={{ flexGrow: 1 }}>
                                      {item.link_name || 'Related Link'}
                                    </Box>
                                    <OpenInNewIcon />
                                  </SourceLink>
                                )}

                                {/* Zusätzliche Quellen */}
                                {item.additional_sources?.map((source, idx) => (
                                  <SourceLink
                                    key={idx}
                                    href={source.url}
                                    onClick={(e) => handleSourceClick(source.url, e)}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    <SourceIcon />
                                    <Box component="span" sx={{ flexGrow: 1 }}>
                                      {source.name || `Additional Source ${idx + 1}`}
                                    </Box>
                                    <OpenInNewIcon />
                                  </SourceLink>
                                ))}
                              </Stack>
                            </SourcesContainer>
                          </Box>
                        </Stack>
                      </ContentContainer>
                    </StyledPaper>
                  </Grid>
                </Fade>
              );
            })}
          </Grid>
        )}
      </Container>
    </Box>
  );
};

export default App; 