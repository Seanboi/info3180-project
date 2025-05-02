<template>
    <div>
      <h1>Favourites Report</h1>
      <div>
        <h2>Top 20 Most Favourited Users</h2>
        <ul>
          <li v-for="user in sortedTopUsers" :key="user.id">
            <p>{{ user.name }} ({{ user.username }}) - Favourited {{ user.favorite_count }} times</p>
            <p v-if="user.profile">
              Parish: {{ user.profile.parish }} | Age: {{ getAge(user.profile.birth_year) }}
            </p>
          </li>
        </ul>
      </div>

      <div>
        <h2>Users You Have Favourited</h2>
        <ul>
          <li v-for="fav in sortedUserFavourites" :key="fav.id">
            <p>{{ fav.favorited_user.name }} {{ fav.favrited_user.username }}</p>
            <p v-if="fav.profile">
              Parish: {{ fav.profile.parish }} | Age: {{ getAge(fav.profile.birth_year) }}
            </p>
          </li>
        </ul>
      </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ProfileFavouritesView',
  setup() {
    const userFavourites = ref([]);
    const userId = ref(null);
    const token = ref(null);

    const fetchUserFavourites = async ()=> {
      try {
        const response = await axios.get(`/api/users/${userId.value}/favourites`, {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        });
        userFavourites.value = response.data.favourites;
      } catch (error) {
        console.error('Error fetching favourites:', error);
      }
    };
    onMounted(()=> {
      token.value = localStorage.getItem('token');
      const storedUser = JSON.parse(localStorage.getItem('user'));
      userId.value = storedUser?.id;

      if (userId.value && token.value){
        fetchUserFavourites();
      } else {
        console.warn('User not logged in or token missing');
      }
    });

    return {
      userFavourites
    };
  }
};
</script>
  
  <style>
  </style>