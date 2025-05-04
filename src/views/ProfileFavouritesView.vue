<template>
  <div class="form-container">
    <h2 class="heading">Top 20 Most Favourited Users</h2>

    <div v-if="loading" class="loading">Loading top users...</div>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="topUsers.length" class="favorites-list">
      <ul>
        <li
          v-for="user in topUsers"
          :key="user.id"
          class="favorite-user compact-user"
        >
          <img
            :src="user.photo ? '/uploads/' + user.photo : '/img/default-avatar.jpg'"
            @error="onImgError"
            alt="User Photo"
            class="favorite-photo"
          />
          <div>
            <p>
              <strong>{{ user.name }}</strong> ({{ user.username }})
            </p>
            <p v-if="user.profile?.description">{{ user.profile.description }}</p>
            <p>This user has been favourited by {{ user.favorite_count }} people.</p>

            <div v-if="user.favourites && user.favourites.length">
              <p class="subheading">They have favourited:</p>
              <ul>
                <li
                  v-for="fav in user.favourites"
                  :key="fav.id"
                  class="favorite-user compact-user"
                >
                  <img
                    :src="fav.profile?.photo ? '/uploads/' + fav.profile.photo : '/img/default-avatar.jpg'"
                    @error="onImgError"
                    alt="Favorite Photo"
                    class="favorite-photo"
                  />
                  <div>
                    <p>
                      <strong>{{ fav.favorited_user.name }}</strong>
                      ({{ fav.favorited_user.username }})
                    </p>
                    <p v-if="fav.profile?.description">{{ fav.profile.description }}</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfileFavouritesView',
  data() {
    return {
      topUsers: [],
      error: '',
      loading: true,
    };
  },
  methods: {
    onImgError(event) {
      event.target.src = '/img/default-avatar.jpg';
    },
    async fetchTopFavouritedUsers() {
      try {
        const token = localStorage.getItem('jwt_token');
        const res = await axios.get('/api/users/favourites/20', {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (res.data.error) {
          this.error = res.data.message || 'Failed to fetch top users.';
          return;
        }

        const users = res.data.top_users;

        // Fetch each user's favourites
        const enrichedUsers = await Promise.all(
          users.map(async user => {
            try {
              const favRes = await axios.get(`/api/users/${user.id}/favourites`, {
                headers: { Authorization: `Bearer ${token}` }
              });
              return {
                ...user,
                favourites: favRes.data.favourites || []
              };
            } catch (e) {
              console.error(`Failed to fetch favourites for user ${user.id}`, e);
              return {
                ...user,
                favourites: []
              };
            }
          })
        );

        this.topUsers = enrichedUsers;
      } catch (err) {
        this.error = err.response?.data?.message || 'An error occurred while fetching top users.';
        console.error('Fetch error:', err);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchTopFavouritedUsers();
  }
};
</script>

<style scoped>
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
  font-weight: bold;
  margin-top: 10px;
}
.favorites-list {
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
.favorite-photo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #3498db;
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




