<template>
  <div class="form-container">
    <h2 class="heading">My Account</h2>

    <div v-if="user">
      <div class="user-info">
        <img :src="userPhotoUrl" @error="onImgError" alt="User Photo" class="user-photo"/>
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Joined:</strong> {{ formatDate(user.date_joined) }}</p>
      </div>

      <h3 class="subheading">Profiles</h3>
      <div v-if="user.profiles && user.profiles.length">
  <div v-for="profile in user.profiles" :key="profile.id" class="profile-block">
    <ProfileCard :profile="profile" />
    <router-link
      :to="`/profiles/matches/${profile.id}`"
      class="button match-button"
    >
      <i class="fas fa-heart"></i> Match Me
    </router-link>
  </div>
</div>
      <p v-else>No profile created yet.</p>

      <div class="favorites-section">
        <h3 class="subheading">Popularity</h3>
        <p v-if="user.favorite_count > 0">
          This user has been favorited by {{ user.favorite_count }} people!
        </p>
        <p v-else>This user has no favourites yet.</p>

        <div v-if="favourites && favourites.length" class="favorites-list">
          <h3 class="subheading">Users You've Favorited</h3>
          <ul>
            <li v-for="fav in favourites" :key="fav.id" class="favorite-user compact-user">
              <img
                :src="fav.profile.photo ? '/uploads/' + fav.profile.photo : '/img/default-avatar.jpg'"
                @error="onImgError"
                alt="Favorite Photo"
                class="favorite-photo"
              />
              <div>
                <p><strong>{{ fav.favorited_user.name }}</strong> ({{ fav.favorited_user.username }})</p>
                <p v-if="fav.profile?.description">{{ fav.profile.description }}</p>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No users found in your favourites list.</p>
        </div>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <div v-if="loadingUser || loadingFavourites" class="loading">Loading user data...</div>
  </div>
</template>

<script>
import axios from 'axios';
import ProfileCard from '@/components/ProfileCard.vue';

export default {
  name: 'UsersView',
  components: { ProfileCard },
  data() {
    return {
      user: null,
      favourites: [],
      error: '',
      loadingUser: true,
      loadingFavourites: true,
    };
  },
  computed: {
    userPhotoUrl() {
      return this.user?.photo ? `/uploads/${this.user.photo}` : '/img/default-avatar.jpg';
    }
  },
  methods: {
    formatDate(dateString) {
      return dateString ? new Date(dateString).toLocaleDateString() : '';
    },
    yesNo(value) {
      return value ? 'Yes' : 'No';
    },
    onImgError(event) {
      event.target.src = '/img/default-avatar.jpg';
    },
    async fetchUserData() {
      try {
        const token = localStorage.getItem('jwt_token');
        let userId = this.$route.params.id || localStorage.getItem('user_id');

        if (!userId) {
          this.error = 'Authentication required';
          return;
        }

        const [userRes, favsRes] = await Promise.all([
          axios.get(`/api/users/${userId}`, { headers: { Authorization: `Bearer ${token}` } }),
          axios.get(`/api/users/${userId}/favourites`, { headers: { Authorization: `Bearer ${token}` } })
        ]);

        this.user = userRes.data.user;
        this.favourites = favsRes.data.favourites;
      } catch (err) {
        this.error = err.response?.data?.message || 'Unable to load user data';
        console.error('Fetch error:', err);
      } finally {
        this.loadingUser = false;
        this.loadingFavourites = false;
      }
    }
  },
  mounted() {
    this.fetchUserData();
  }
};
</script>

<style>
.form-container {
  background-color: rgb(255, 200, 0);
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
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
.profile-block {
  margin-bottom: 20px;
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
.favorites-section {
  background-color: #e8f4f8;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}
.favorite-user.compact-user {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding: 8px 12px;
  background-color: #ffffff;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.favorite-user .favorite-photo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #3498db;
}
router-link.match-button {
  background-color: #2ecc71;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  display: inline-block;
  margin-top: 10px;
}

router-link.match-button:hover {
  background-color: #27ae60; 
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

