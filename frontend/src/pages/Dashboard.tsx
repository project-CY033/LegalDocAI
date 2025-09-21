import React from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../store/store';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { documents } = useSelector((state: RootState) => state.documents);

  const stats = [
    {
      title: 'Documents Processed',
      value: user?.documents_processed || 0,
      color: 'primary.main',
    },
    {
      title: 'API Calls',
      value: user?.api_calls_count || 0,
      color: 'secondary.main',
    },
    {
      title: 'Recent Documents',
      value: documents.length,
      color: 'success.main',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
        Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Welcome back! Here's what's happening with your legal documents.
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {stat.title}
                </Typography>
                <Typography variant="h4" sx={{ color: stat.color, fontWeight: 'bold' }}>
                  {stat.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Quick Actions */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/upload')}
                sx={{ justifyContent: 'flex-start' }}
              >
                📄 Upload New Document
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/documents')}
                sx={{ justifyContent: 'flex-start' }}
              >
                📂 View All Documents
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <List>
              {documents.slice(0, 3).map((doc, index) => (
                <ListItem key={index} divider>
                  <ListItemText
                    primary={doc.original_filename}
                    secondary={`Status: ${doc.status} • ${new Date(doc.created_at).toLocaleDateString()}`}
                  />
                </ListItem>
              ))}
              {documents.length === 0 && (
                <ListItem>
                  <ListItemText
                    primary="No documents yet"
                    secondary="Upload your first legal document to get started"
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;