<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import bg from "@/assets/Home_Page_Background.jpg";
import axios from 'axios';

const router = useRouter();
const latestProfiles = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");
const isLoggedIn = ref(false);
const user = ref(null);

onMounted(async () => {
  try {
    const userId = localStorage.getItem('user_id');
    isLoggedIn.value = !!userId;
    // Fetch the latest profiles (most recent 4)
    const response = await fetch('/api/profiles');
    
    // Check if response is ok before trying to parse JSON
    if (!response.ok) {
      throw new Error(`Server responded with status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.error) {
      latestProfiles.value = data.profiles;
    } else {
      errorMessage.value = data.message || "Failed to load latest profiles";
    }

    if (isLoggedIn.value) {
      try {
        const userId = localStorage.getItem('user_id');
          const userData = await axios.get(`/api/users/${userId}`);
          user.value = userData.data.user;
        
      } catch (userErr) {
        console.error("Error fetching user data:", userErr);
      }
    }

    

  } catch (err) {
    console.error("Error fetching profiles:", err);
    errorMessage.value = "Error connecting to the server. Please try again later.";
    // Still set latestProfiles to empty array to ensure proper rendering
    latestProfiles.value = [];
  } finally {
    isLoading.value = false;
  }
});

 // Check if user is logged in

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};


</script>

<template>
  <div class="container py-5">
    <div v-if="!isLoggedIn">
    <div class="row mb-5">
      <div class="col-md-6 offset-md-3 text-center">
        <h1 class="display-4 mb-4">Welcome to Jam-Date</h1>
        <p class="lead">Find your perfect match in Jamaica today!</p>
        <div class="mt-5">
          <button class="btn btn-primary btn-lg me-3" @click="goToLogin">Login</button>
          <button class="btn btn-success btn-lg" @click="goToRegister">Register</button>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-12">
        <h2 class="text-center mb-4">Latest Profiles</h2>
        <div v-if="isLoading" class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else-if="errorMessage" class="alert alert-danger text-center">
          <p>{{ errorMessage }}</p>
          <p>Please try again later or contact support if the issue persists.</p>
        </div>
        <div v-else-if="latestProfiles.length === 0" class="text-center">
          <p>No profiles available yet. Be the first to create one!</p>
        </div>
        <div v-else class="row">
          <div v-for="profile in latestProfiles" :key="profile.id" class="col-md-3 mb-4">
            <div class="card h-100">
              <img 
                :src="profile.photo ? `/uploads/${profile.photo}` : '/placeholder.jpg'" 
                class="card-img-top" 
                alt="Profile photo"
                style="height: 200px; object-fit: cover;"
              >
              <div class="card-body">
                <h5 class="card-title">{{ profile.name }}</h5>
                <p class="card-text">
                  <small>{{ profile.parish }} • {{ new Date().getFullYear() - profile.birth_year }} years</small>
                </p>
                <p class="card-text text-truncate">{{ profile.description }}</p>
              </div>
              <div class="card-footer bg-white border-top-0">
                <button 
                  class="btn btn-outline-primary btn-sm w-100"
                  @click="router.push(`/profiles/${profile.id}`)"
                >
                  View Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-md-8 offset-md-2">
        <div class="card bg-light">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">How It Works</h3>
            <div class="row text-center">
              <div class="col-md-4">
                <div class="mb-3">
                  <i class="fas fa-user-plus fa-3x text-primary"></i>
                </div>
                <h5>Create Your Profile</h5>
                <p>Sign up and create your detailed profile to get started</p>
              </div>
              <div class="col-md-4">
                <div class="mb-3">
                  <i class="fas fa-search fa-3x text-primary"></i>
                </div>
                <h5>Find Matches</h5>
                <p>Search profiles or let our system find your perfect match</p>
              </div>
              <div class="col-md-4">
                <div class="mb-3">
                  <i class="fas fa-heart fa-3x text-primary"></i>
                </div>
                <h5>Connect</h5>
                <p>Add favorites and start your Jamaican love journey</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="isLoggedIn && user">
    <div class="row mb-4">
        <div class="col-12">
          <h1 class="display-5">Welcome back, {{ user.name }}!</h1>
          <p class="lead">Here's what's happening on Jam-Date today</p>
        </div>
      </div>
  </div>
  </div>
</template>

<style scoped>
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.card {
  transition: transform 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-5px);
}

.fas {
  color: #007bff;
}
</style> 