<template>
  <div class="logout-page" :style="backgroundStyle">
    <div class="overlay">
      <transition name="fade">
        <div class="logout-box" v-show="showBox">
          <h2 class="logout-title">{{ logoutMessage }}</h2>
          <p class="logout-subtitle" v-if="!isLoggingOut">{{ subtitleMessage }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggingOut = ref(true);
const showBox = ref(false);
const logoutMessage = ref('Logging you out...');
const subtitleMessage = ref('');

const backgroundStyle = {
  backgroundImage: "url('/images/Home_Page_Background.jpg')",
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  minHeight: 'calc(100vh - 75px)',
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
};

const logout = async () => {
  try {
    localStorage.removeItem('user_id');
    localStorage.removeItem('token');
    window.dispatchEvent(new Event('user-auth-changed'));

    logoutMessage.value = 'You have been successfully logged out!';
    subtitleMessage.value = 'We hope to see you again soon!';
    isLoggingOut.value = false;

    setTimeout(() => {
      router.push('/');
    }, 2000);
  } catch (error) {
    console.error('Error during logout:', error);
    logoutMessage.value = 'An error occurred during logout. Please try again.';
    isLoggingOut.value = false;
  }
};

onMounted(() => {
  showBox.value = true;
  logout();
});

</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 2rem 1rem;
  min-height: calc(100vh - 75px); 
}

.logout-box {
  background-color: #FFD700;
  padding: 40px 30px;
  border-radius: 10px;
  max-width: 450px;
  width: 100%;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.logout-title {
  font-size: 28px;
  font-weight: bold;
  color: black;
  margin-bottom: 10px;
}

.logout-subtitle {
  font-size: 16px;
  color: black;
}
</style>
