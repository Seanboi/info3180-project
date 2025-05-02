<template>
    <div class="about container">
      <h2>About</h2>
      <p>This is an about page.</p>
    </div>
    <div class="profile container">
      <h1 class="profile-title">{{ profile description}}</h1>
      <div v-if="error" class="error">{{ error}}</div>
      <div v-else-if="loading" class="loading">Loading profile...</div>
      <div v-else class="profile-details">
        <p><strong>Parish:</strong>{{UsersView.parish}}</p>
        <p><strong>Biography:</strong>{{UsersView.biography}}</p>
        <p><strong>Sex:</strong>{{UsersView.sex}}</p>
        <p><strong>Race:</strong>{{UsersView.race}}</p>
        <p><strong>Birth Year:</strong>{{UsersView.View.birth_year}}</p>
        <p><strong>Height:</strong>{{UsersView.height}}</p>
        <p><strong>Favourite Cuisine:</strong> {{ UsersView.fav_cuisine || 'N/A' }}</p>
        <p><strong>Favourite Colour:</strong> {{ UsersView.fav_colour || 'N/A' }}</p>
        <p><strong>Favourite Subject:</strong> {{ UsersView.fav_school_subject || 'N/A' }}</p>
        <p><strong>Political:</strong> {{ UsersView.political ? 'Yes' : 'No' }}</p>
        <p><strong>Religious:</strong> {{ UsersView.religious ? 'Yes' : 'No' }}</p>
        <p><strong>Family Oriented:</strong> {{ UsersView.family_oriented ? 'Yes' : 'No' }}</p>
      </div>
    </div>
  </template>
  
  <script>
    import axios from 'axios';
    export default {
      data() {
        return {
          profile: {},
          loading: true,
          error: ''
        };
      },
      async created() {
        const profileId = this.$route.params.id;
        try {
          const res = await axios.get(`/api/profiles/${profileId}`);
          this.profile = res.data.profile;
        } catch (err) {
          this.error = err.response?.data?.message || 'Failed to load profile';
        } finally {
          this.loading = false;
        }
      }
    };
  </script>
  <style>
    .form-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .heading {
    color: #333;
    margin-bottom: 20px;
    font-size: 2rem;
  }
  
  .subheading {
    margin-top: 30px;
    margin-bottom: 15px;
    font-size: 1.5rem;
    color: #2c3e50;
  }
  
  .user-info {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .user-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 15px;
    border: 3px solid #3498db;
  }
  
  .profile-card {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 4px solid #3498db;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  
  .profile-card p {
    margin: 10px 0;
  }
  
  .favorites-section {
    background-color: #e8f4f8;
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
  }
  
  .error {
    color: #e74c3c;
    font-weight: bold;
    padding: 10px;
    background-color: #fadbd8;
    border-radius: 4px;
  }
  
  .loading {
    text-align: center;
    color: #7f8c8d;
    font-style: italic;
    margin: 20px 0;
  }
  </style>