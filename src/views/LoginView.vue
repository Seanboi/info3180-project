<template>
  <div class="login-page" :style="backgroundStyle">
    <div class="overlay">
      <div class="login-box">
        <h1 class="form-title">Login!</h1>
        <p class="subtitle">We are glad to have you here!</p>
        <LoginForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '../components/LoginForm.vue';

const backgroundStyle = {
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  height: '100vh',
  width: '100vw',
};
</script>

<style scoped>
.overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  padding: 1rem;
}

.login-box {
  background-color: #0B6623; 
  padding: 60px 40px;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.form-title {
  color: #FFD700; 
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
}

.subtitle {
  color: white;
  font-size: 16px;
  margin-bottom: 20px;
}
</style>
