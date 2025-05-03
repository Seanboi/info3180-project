<template>
    <div class="logout-container">
      <div class="logout-message">
        <div class="spinner-border text-primary mb-3" role="status" v-if="isLoggingOut">
          <span class="visually-hidden">Loading...</span>
        </div>
        <h2>{{ logoutMessage }}</h2>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  const router = useRouter();
  const isLoggingOut = ref(true);
  const logoutMessage = ref('Logging you out...');
  
  const logout = async () => {
    try {
      // Optional: Call your backend logout endpoint if you have one
      // const response = await axios.post('/api/auth/logout');
      
      // Clear user data from localStorage
      localStorage.removeItem('user_id');
      localStorage.removeItem('token'); // If you use authentication tokens
      window.dispatchEvent(new Event('user-auth-changed'));
      // Any other cleanup needed
      
      logoutMessage.value = 'You have been successfully logged out!';
      
      // Redirect to home page after a short delay to show the success message
      setTimeout(() => {
        router.push('/');
      }, 1500);
    } catch (error) {
      console.error('Error during logout:', error);
      logoutMessage.value = 'An error occurred during logout. Please try again.';
      isLoggingOut.value = false;
    }
  };
  
  onMounted(() => {
    // Perform logout when component mounts
    logout();
  });
  </script>
  
  <style scoped>
  .logout-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
  }
  
  .logout-message {
    text-align: center;
    padding: 2rem;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 400px;
  }
  </style>
