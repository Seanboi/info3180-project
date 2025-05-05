<template>
  <div class="profile-container">
    <div class="profile-header">
      <img :src="profilePhotoUrl || 'https://via.placeholder.com/150'" alt="Profile Photo" class="profile-photo" />
      <div class="profile-title-group">
        <h1 class="profile-title">{{ profile.name }}</h1>
        <h2 class="profile-username">{{ profile.description }}</h2>
        <p class="profile-bio">{{ profile.biography }}</p>
      </div>
    </div>

    <div class="profile-columns">
      <ul class="profile-list">
        <li><strong>Sex:</strong> {{ profile.sex }}</li>
        <li><strong>Height:</strong> {{ profile.height }} inches</li>
        <li><strong>Birth Year:</strong> {{ profile.birth_year }}</li>
        <li><strong>Race:</strong> {{ profile.race }}</li>
        <li><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</li>
        <li><strong>Favourite Subject:</strong> {{ profile.fav_school_subject || 'N/A' }}</li>
      </ul>
    </div>

    <div class="profile-tags">
      <div class="tag">Political: {{ profile.political ? 'Yes' : 'No' }}</div>
      <div class="tag">Religious: {{ profile.religious ? 'Yes' : 'No' }}</div>
      <div class="tag">Family Oriented: {{ profile.family_oriented ? 'Yes' : 'No' }}</div>
    </div>

    <div class="profile-buttons">
      <button class="button email-button">Email User</button>
      <button class="button favorite-button" @click="addToFavourites" :disabled="favourited">
        <span v-if="favourited">❤️</span>
        <span v-else>🤍</span>
      </button>
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
      error: '',
      favourited: false,
      csrf_token: ''
    };
  },
  computed: {
    profilePhotoUrl() {
      if (this.profile && this.profile.photo) {
        return `/uploads/${this.profile.photo}`;
      }
      return '/img/default-avatar.jpg';
    }
  },
  methods: {
    async addToFavourites() {
      try {
        console.log('Attempting to favorite profile:', this.profile.user_id);
        const userId = this.profile.user_id;
        console.log('Sending request to:', `/api/profiles/${userId}/favourite`);

        const res = await axios.post(
          `/api/profiles/${userId}/favourite`,
          {},
          {
            headers: {
              'X-CSRFToken': this.csrf_token
            },
            withCredentials: true
          }
        );

        console.log('Response:', res.data);

        if (!res.data.error) {
          this.favourited = true;
          alert(res.data.message);
        } else {
          alert(res.data.message);
        }
      } catch (err) {
        console.error('Error details:', err.response || err);

        if (err.response && err.response.status === 400) {
          alert('Cannot add yourself to favorites');
        } else if (err.response && err.response.status === 409) {
          this.favourited = true;
          alert('This user is already in your favorites');
        } else {
          const message = err.response?.data?.message || 'Failed to add to favourites';
          alert(message);
        }
      }
    },

    async fetchProfile() {
      const profileId = this.$route.params.id;
      try {
        const res = await axios.get(`/api/profiles/${profileId}`);
        this.profile = res.data.profile;
        await this.checkIfFavorited();
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load profile';
      } finally {
        this.loading = false;
      }
    },

    getCsrfToken() {
      fetch('/api/v1/csrf-token')
        .then((res) => res.json())
        .then((data) => {
          this.csrf_token = data.csrf_token;
        })
        .catch((err) => {
          console.error("Failed to fetch CSRF token:", err);
        });
    }
  },
  created() {
    this.fetchProfile();
    this.getCsrfToken();
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
  background: transparent;
  color: white;
  font-size: 1.2em;
  border: 2px solid white;
  transition: all 0.3s ease;
}

.favorite-button:hover {
  background: rgb(241, 88, 88);
}
</style>
