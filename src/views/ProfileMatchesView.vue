<template>
    <div class="matches-container">
      <h2>Matched Profiles</h2>
      <div v-if="loading" class="loading">Loading matches...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="matches.length">
        <div v-for="match in matches" :key="match.id" class="match-card">
          <img :src="match.photo ? '/uploads/' + match.photo : '/img/default-avatar.jpg'" @error="onImgError" alt="Match Photo">
          <div class="match-info">
            <p><strong>{{ match.name }}</strong> ({{ match.username }})</p>
            <p>{{ match.description }}</p>
            <p><strong>Match Score:</strong> {{ match.match_score }} / 6</p>
          </div>
        </div>
      </div>
      <div v-else>No matches found based on criteria.</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ProfileMatches',
    data() {
      return {
        matches: [],
        error: '',
        loading: true,
        sourceProfile: {}  // Added for debugging purposes
      };
    },
    methods: {
      onImgError(e) {
        e.target.src = '/img/default-avatar.jpg';
      },
      async fetchMatches() {
        const token = localStorage.getItem('jwt_token');
        const profileId = this.$route.params.id;
  
        try {
          const res = await axios.get(`/api/profiles/matches/${profileId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
  
          console.log('API response:', res.data); // Debugging the API response
  
          if (res.data.error) {
            this.error = res.data.message;
            return;
          }
  
          if (res.data.matches && res.data.matches.length > 0) {
            this.matches = res.data.matches;
          } else {
            this.error = "No matches found.";
          }
  
          console.log('Matches:', this.matches); // Check matches data
  
          // Store the source profile data
          if (res.data.source_profile) {
            this.sourceProfile = res.data.source_profile;
            console.log('Source profile data:', this.sourceProfile);  // Check source profile data
          }
  
        } catch (err) {
          console.error('Error fetching matches:', err); // Log any errors
          this.error = err.response?.data?.message || 'Unable to fetch matches';
        } finally {
          this.loading = false;
        }
      }
    },
    mounted() {
      this.fetchMatches();
    }
  };
  </script>
  
  <style scoped>
  .matches-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
  }
  .loading {
    font-style: italic;
    color: #999;
  }
  .error {
    color: red;
    background: #ffe0e0;
    padding: 10px;
    border-radius: 4px;
  }
  .match-card {
    display: flex;
    gap: 15px;
    padding: 10px;
    background: #f2f8fc;
    margin-bottom: 15px;
    border-radius: 8px;
    align-items: center;
  }
  .match-card img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid #3498db;
  }
  .match-info {
    flex-grow: 1;
  }
  </style>
  
