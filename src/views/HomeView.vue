<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();
const latestProfiles = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");
const isLoggedIn = ref(false);
const user = ref(null);
const showSearch = ref(false);

// Search functionality
const searchResults = ref([]);
const isSearching = ref(false);
const searchErrorMessage = ref('');
const searchForm = reactive({
  name: '',
  birthYear: '',
  sex: '',
  race: ''
});

onMounted(async () => {
  try {
    const userId = localStorage.getItem('user_id');
    isLoggedIn.value = !!userId;
    // Fetch the latest profiles (most recent 4)
    const response = await fetch('/api/profiles?latest=1&per_page=4');
    
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

const toggleSearch = () => {
  showSearch.value = !showSearch.value;
  // Reset search results when hiding search
  if (!showSearch.value) {
    searchResults.value = [];
  }
};

const performSearch = async () => {
  isSearching.value = true;
  searchErrorMessage.value = '';
  
  try {
    // Build query parameters based on filled fields
    const params = {};
    if (searchForm.name) params.name = searchForm.name;
    if (searchForm.birthYear) params.birth_year = searchForm.birthYear;
    if (searchForm.sex) params.sex = searchForm.sex;
    if (searchForm.race) params.race = searchForm.race;

    // Make the API call without requiring authentication
    const response = await axios.get('/api/search', { params });
    
    if (response.data && !response.data.error) {
      searchResults.value = response.data.results || [];
      // Display a message if no results were found
      if (searchResults.value.length === 0 && !searchErrorMessage.value) {
        searchErrorMessage.value = 'No profiles match your search criteria';
      }
    } else {
      searchErrorMessage.value = response.data.message || 'Failed to retrieve search results';
      searchResults.value = [];
    }
  } catch (err) {
    console.error('Search error:', err);
    searchErrorMessage.value = err.response?.data?.message || 'Error during search. Please try again.';
    searchResults.value = [];
  } finally {
    isSearching.value = false;
  }
};


const clearSearch = () => {
  searchForm.name = '';
  searchForm.birthYear = '';
  searchForm.sex = '';
  searchForm.race = '';
  searchResults.value = [];
};

const viewProfile = (profileId) => {
  router.push(`/profiles/${profileId}`);
};

const calculateAge = (birthYear) => {
  return new Date().getFullYear() - birthYear;
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

    <div class="row mt-5 how-it-works-section">
      <div class="col-md-8 offset-md-2">
        <div class="card how-it-works-card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">How It Works</h3>
            <div class="row text-center">
              <div class="col-md-4">
                <div class="step-icon">1</div>
                <h5>Create Your Profile</h5>
                <p>Sign up and create your detailed profile to get started</p>
              </div>
              <div class="col-md-4">
                <div class="step-icon">2</div>
                <h5>Find Matches</h5>
                <p>Search profiles or let our system find your perfect match</p>
              </div>
              <div class="col-md-4">
                <div class="step-icon">3</div>
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
          
          <!-- Search toggle button -->
          <div class="text-center mb-4">
            <button @click="toggleSearch" class="btn btn-lg" :class="{'btn-primary': !showSearch, 'btn-secondary': showSearch}">
              <i class="bi" :class="{'bi-search': !showSearch, 'bi-x-lg': showSearch}"></i>
              {{ showSearch ? 'Hide Search' : 'Search Profiles' }}
            </button>
          </div>
          
          <!-- Search form -->
          <div v-if="showSearch" class="search-container mb-5">
            <div class="card">
              <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Search Profiles</h4>
              </div>
              <div class="card-body">
                <form @submit.prevent="performSearch">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label for="name" class="form-label">Name</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        id="name" 
                        v-model="searchForm.name"
                        placeholder="Enter name or part of name"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="birthYear" class="form-label">Birth Year</label>
                      <input 
                        type="number" 
                        class="form-control" 
                        id="birthYear" 
                        v-model="searchForm.birthYear"
                        placeholder="e.g. 1990"
                        min="1900"
                        max="2006"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="sex" class="form-label">Sex</label>
                      <select class="form-select" id="sex" v-model="searchForm.sex">
                        <option value="">Select Sex</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label for="race" class="form-label">Race</label>
                      <select class="form-select" id="race" v-model="searchForm.race">
                        <option value="">Select Race</option>
                        <option value="Black">Black</option>
                        <option value="East Indian">East Indian</option>
                        <option value="Caucasian">Caucasian</option>
                        <option value="Chinese">Chinese</option>
                        <option value="Mixed">Mixed</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div class="col-12 text-center mt-3">
                      <button type="submit" class="btn btn-primary me-2" :disabled="isSearching">
                        <span v-if="isSearching" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                        <span v-else class="bi bi-search me-1"></span>
                        {{ isSearching ? 'Searching...' : 'Search' }}
                      </button>
                      <button type="button" class="btn btn-secondary" @click="clearSearch" :disabled="isSearching">
                        <i class="bi bi-x-circle me-1"></i> Clear
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
            
            <!-- Search results -->
            <div v-if="searchErrorMessage" class="alert alert-danger mt-4" role="alert">
              {{ searchErrorMessage }}
            </div>
            
            <div v-else-if="searchResults.length > 0" class="mt-4">
              <h3 class="text-center mb-4">Search Results</h3>
              <div class="row">
                <div v-for="profile in searchResults" :key="profile.id" class="col-md-3 mb-4">
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
                        <small>{{ profile.parish }} • {{ calculateAge(profile.birth_year) }} years</small>
                      </p>
                      <p class="card-text text-truncate">{{ profile.description }}</p>
                    </div>
                    <div class="card-footer bg-white border-top-0">
                      <button 
                        class="btn btn-outline-primary btn-sm w-100"
                        @click="viewProfile(profile.id)"
                      >
                        View Profile
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="searchResults.length === 0 && !isSearching && !searchErrorMessage" class="alert alert-info mt-4 text-center">
              <p class="mb-0">No profiles match your search criteria. Please try different filters.</p>
            </div>
          </div>
          
          <!-- Latest profiles section -->
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
  </div>
  </div>
</template>

<style scoped>
.display-4 {
  font-weight: bold;
  color: #FFD700; 
}

.lead {
  font-size: 1.2rem;
  font-weight: 500;
  color: #000;
}

/* Fixed background image implementation */
.container.py-5 {
  /* Try the absolute path from public folder */
  background-image: url('/images/Home_Page_Background.jpg'); 
  background-size: cover;
  background-position: center;
  color: white;
  padding: 5rem 1rem !important;
  border-radius: 10px;
  position: relative;
  z-index: 1;
}

/* Made the before element transparent as requested */
.container.py-5::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: transparent; /* Completely transparent */
  z-index: -1;
  border-radius: 10px;
}

.btn-primary {
  background-color: #0B6623;
  border: none;
  font-weight: bold;
  padding: 10px 20px;
}

.btn-success {
  background-color: #FFD700;
  border: none;
  color: #0B6623;
  font-weight: bold;
  padding: 10px 20px;
}

.btn-primary:hover {
  background-color: #095526;
}

.btn-success:hover {
  background-color: #e6c200;
  color: #0B6623;
}

.card {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-weight: 600;
  color: #000;
}

.card-text small {
  color: #666;
}

.card-footer button {
  font-weight: 500;
}

.display-5 {
  color: #FFD700;
  font-weight: bold;
  margin-bottom: 10px;
}

.text-center.mb-4 {
  font-size: 24px;
  font-weight: bold;
  color: #0B6623;
}

.how-it-works-card {
  background-color: #0B6623; 
  color: white;
  border: none;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.step-icon {
  background-color: #FFD700; 
  color: #0B6623;
  font-weight: bold;
  font-size: 24px;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  margin: 0 auto 15px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.how-it-works-section h5 {
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: #FFD700;
}

.how-it-works-section p {
  font-size: 0.95rem;
  color: white;
}

.search-container {
  margin-bottom: 2rem;
}

.search-container .card-header {
  background-color: #0B6623 !important;
}

.form-label {
  font-weight: 500;
}
</style>