<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top jam-header">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="/">
          <img :src="jamDateLogo" alt="Jam Date Logo" class="logo-img me-2" />
          <span class="brand-text">Jam Date</span>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto" v-if="isLoggedIn">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">About</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/Users" class="nav-link" :class="{ active: $route.path === '/Users' }">Account</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/addprofile" class="nav-link" :class="{ active: $route.path === '/addprofile' }">Add Profile</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav me-auto" v-else>
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">About</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/login" class="nav-link" :class="{ active: $route.path === '/login' }">Login</RouterLink>
            </li>
          </ul>
          
          <!-- Right-aligned menu items for logged in users -->
          <ul class="navbar-nav ms-auto" v-if="isLoggedIn">
            <li class="nav-item">
              <RouterLink to="/Favourites" class="nav-link" :class="{ active: $route.path === '/Favourites' }">Reports</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/Logout" class="nav-link" :class="{ active: $route.path === '/Logout' }">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>
<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, computed } from "vue";
import jamDateLogo from "@/assets/JamDate_Logo.png";
import axios from 'axios';
const isLoggedIn = ref(false);
const user = ref(null);
onMounted(async () => {
  const userId = localStorage.getItem('user_id');
    isLoggedIn.value = !!userId;
  if (isLoggedIn.value) {
      try {
        const userId = localStorage.getItem('user_id');
          const userData = await axios.get(`/api/users/${userId}`);
          user.value = userData.data.user;
        
      } catch (userErr) {
        console.error("Error fetching user data:", userErr);
      }
    }
  const checkLogin = () => {
    const updatedUserId = localStorage.getItem('user_id');
    isLoggedIn.value = !!updatedUserId;
  };
  checkLogin();
  window.addEventListener('user-auth-changed', checkLogin);
});
</script>
<style>
.jam-header {
  background-color: #0B6623;
  padding: 0.5rem 1rem;
}
.logo-img {
  height: 45px;
  width: auto;
}
.nav-link {
  color: white !important;
  font-weight: normal;
  margin-right: 1rem;
  font-size: 1rem;
  text-decoration: none;
}
.nav-link.active {
  font-weight: bold;
  text-decoration: none;
}
</style>