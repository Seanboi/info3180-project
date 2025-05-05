<template>
    <div class="Register-container">
      <RegisterForm />
    </div>
  </template>
  
  <script setup>
import RegisterForm from '../components/RegisterForm.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const regMessage = ref('Registering you...');


const register = async () => {
  try {

    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error) {
    console.error('Error during register:', error);
    regMessage.value = 'An error occurred during register. Please try again.';
    
  }
};

onMounted(() => {
  register();
});


  </script>
  
  <style scoped>
  .Register-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
  }
  
  .form-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 28px;
    color: #333;
  }
  </style>