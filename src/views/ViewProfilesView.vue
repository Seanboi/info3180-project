<template>
  <div class="profile-container">
    <div class="profile-header">
      <img :src="profile.photo || 'https://via.placeholder.com/150'" alt="Profile Photo" class="profile-photo" />
      <div class="profile-title-group">
        <h1 class="profile-title">Jam-Date</h1>
        <h2 class="profile-username">{{ Users.description }}</h2>
        <p class="profile-bio">{{ Users.biography }}</p>
      </div>
    </div>

    <div class="profile-columns">
      <ul class="profile-list">
        <li><strong>Description:</strong> {{ Users.description }}</li>
        <li><strong>Parish:</strong> {{ Users.parish }}</li>
        <li><strong>Sex:</strong> {{ Users.sex }}</li>
        <li><strong>Height:</strong> {{ Users.height }} inches</li>
      </ul>
      <ul class="profile-list">
        <li><strong>Biography:</strong> {{ Users.biography }}</li>
        <li><strong>Birth Year:</strong> {{ Users.birth_year }}</li>
        <li><strong>Race:</strong> {{ Users.race }}</li>
        <li><strong>Favourite Colour:</strong> {{ Users.fav_colour }}</li>
      </ul>
    </div>

    <div class="profile-tags">
      <div class="tag">Political: {{ Users.political ? 'Yes' : 'No' }}</div>
      <div class="tag">Religious: {{ Users.religious ? 'Yes' : 'No' }}</div>
      <div class="tag">Family Oriented: {{ Users.family_oriented ? 'Yes' : 'No' }}</div>
      <div class="tag">Favourite Subject: {{ Users.fav_school_subject || 'N/A' }}</div>
    </div>

    <div class="profile-buttons">
      <button class="button email-button">Email User</button>
      <button class="button favorite-button">Add to Favorites</button>
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
.profile-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  background: linear-gradient(to bottom, #66bb6a, #43a047);
  border-radius: 20px;
  color: #fff;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-photo {
  width: 120px;
  height: 120px;
  border-radius: 10px;
  margin-right: 20px;
  object-fit: cover;
}

.profile-title-group {
  flex: 1;
}

.profile-title {
  font-size: 2.5em;
  margin: 0;
}

.profile-username {
  font-size: 1.5em;
  margin: 5px 0;
}

.profile-bio {
  font-size: 1em;
}

.profile-columns {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.profile-list {
  list-style: none;
  padding: 0;
}

.profile-list li {
  margin-bottom: 10px;
}

.profile-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.tag {
  background: #2e7d32;
  padding: 10px;
  border-radius: 10px;
  flex: 1 1 150px;
  text-align: center;
}

.profile-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.button {
  background: #e53935;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
}

.button:hover {
  background: #d32f2f;
}

.email-button {
  background: #ff5252;
}

.favorite-button {
  background: #ff1744;
}
</style>
