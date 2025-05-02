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
</style>