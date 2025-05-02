<template>
    <div class="form-container">
      <h2 class="heading">My Account</h2>
      <div v-if="user">
        <div class="user-info">
          <img :src="userPhotoUrl" alt="User Photo" class="user-photo"/>
          <p><strong>Name:</strong> {{user.name}}</p>
          <p><strong>Username:</strong> {{user.username}}</p>
          <p><strong>Email:</strong> {{user.email}}</p>
          <p><strong>Joined:</strong> {{ formatDate(user.date_joined) }}</p>
        </div>
  
        <h3 class="subheading">Profile</h3>
        <div v-if="user.profile" class="profile-card">
          <p><strong>Description:</strong> {{user.profile.description}}</p>
          <p><strong>Parish:</strong> {{user.profile.parish}}</p>
          <p><strong>Biography:</strong> {{user.profile.biography}}</p>
          <p><strong>Sex:</strong> {{user.profile.sex}}</p>
          <p><strong>Race:</strong> {{user.profile.race}}</p>
          <p><strong>Birth Year:</strong> {{user.profile.birth_year}}</p>
          <p><strong>Height:</strong> {{user.profile.height}} inches</p>
          <p><strong>Favorite Cuisine:</strong> {{user.profile.fav_cuisine}}</p>
          <p><strong>Favorite Color:</strong> {{user.profile.fav_colour}}</p>
          <p><strong>Favorite School Subject:</strong> {{user.profile.fav_school_subject}}</p>
          <p><strong>Political:</strong> {{user.profile.political ? 'Yes' : 'No'}}</p>
          <p><strong>Religious:</strong> {{user.profile.religious ? 'Yes' : 'No'}}</p>
          <p><strong>Family Oriented:</strong> {{user.profile.family_oriented ? 'Yes' : 'No'}}</p>
        </div>
        <p v-else>No profile created yet.</p>
        
        <div v-if="user.favorite_count > 0" class="favorites-section">
          <h3 class="subheading">Popularity</h3>
          <p>This user has been favorited by {{user.favorite_count}} people!</p>
        </div>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <div v-if="loading" class="loading">Loading user data...</div>
    </div>
  </template>
    
  <script>
  import axios from 'axios';
  export default {
    name: 'UsersView',
    data() {
      return {
        user: null,
        error: '',
        loading: true
      };
    },
    computed: {
      userPhotoUrl() {
        // Create a computed property for the photo URL
        if (this.user && this.user.photo) {
          return `/uploads/${this.user.photo}`;
        }
        return '/img/default-avatar.jpg'; // Fallback default avatar
      }
    },
    methods: {
      formatDate(dateString) {
        if (!dateString) return '';
        return new Date(dateString).toLocaleDateString();
      }
    },
    async created() {
      try {
        this.loading = true;
        // Get token from local storage
        const token = localStorage.getItem('token');
        
        // Get user ID either from route params or from token
        // Depending on your authentication implementation
        let userId = this.$route.params.id;
        if (!userId) {
          // If no ID in route params, assume we're showing current user profile
          userId = localStorage.getItem('user_id');
        }
        
        if (!userId || !token) {
          this.error = 'Authentication required';
          this.loading = false;
          return;
        }
        
        // Make API request to get user details
        const res = await axios.get(`/api/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.user = res.data.user;
        this.loading = false;
      } catch (err) {
        console.error('Error fetching user data:', err);
        this.error = err.response?.data?.message || 'Unable to load user data';
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