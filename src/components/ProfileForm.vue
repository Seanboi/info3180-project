<template>
  <div class="profile-form-container">
    <form id="profileForm" @submit.prevent="submitProfile" class="profile-form">
    
      <h2 class="form-title">Complete Your Profile</h2>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <input type="text" id="description" v-model="description" class="form-control" required maxlength="160" />
        <small class="form-text text-muted">Maximum 160 characters</small>
      </div>

      <div class="form-group mb-3">
        <label for="parish" class="form-label">Parish</label>
        <select id="parish" v-model="parish" class="form-control" required>
          <option value="">Select a parish</option>
          <option value="Kingston">Kingston</option>
          <option value="St. Andrew">St. Andrew</option>
          <option value="St. Thomas">St. Thomas</option>
          <option value="Portland">Portland</option>
          <option value="St. Mary">St. Mary</option>
          <option value="St. Ann">St. Ann</option>
          <option value="Trelawny">Trelawny</option>
          <option value="St. James">St. James</option>
          <option value="Hanover">Hanover</option>
          <option value="Westmoreland">Westmoreland</option>
          <option value="St. Elizabeth">St. Elizabeth</option>
          <option value="Manchester">Manchester</option>
          <option value="Clarendon">Clarendon</option>
          <option value="St. Catherine">St. Catherine</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="biography" class="form-label">Biography</label>
        <textarea id="biography" v-model="biography" class="form-control" required maxlength="300" rows="4"></textarea>
        <small class="form-text text-muted">Maximum 300 characters</small>
      </div>

      <div class="form-group mb-3">
        <label for="sex" class="form-label">Sex</label>
        <select id="sex" v-model="sex" class="form-control" required>
          <option value="">Select one</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="race" class="form-label">Race</label>
        <input type="text" id="race" v-model="race" class="form-control" required maxlength="30" />
        <small class="form-text text-muted">Maximum 30 characters</small>
      </div>

      <div class="form-group mb-3">
        <label for="birth_year" class="form-label">Birth Year</label>
        <input type="number" id="birth_year" v-model="birth_year" class="form-control" required min="1900" :max="currentYear" />
        <small class="form-text text-muted">Must be at least 18 years old</small>
      </div>

      <div class="form-group mb-3">
        <label for="height" class="form-label">Height (in cm)</label>
        <input type="number" id="height" v-model="height" class="form-control" required min="50" max="250" step="0.1" />
        <small class="form-text text-muted">Between 50cm and 250cm</small>
      </div>

      <div class="form-group mb-3">
        <label for="fav_cuisine" class="form-label">Favorite Cuisine</label>
        <input type="text" id="fav_cuisine" v-model="fav_cuisine" class="form-control" required maxlength="80" />
        <small class="form-text text-muted">Maximum 80 characters</small>
      </div>

      <div class="form-group mb-3">
        <label for="fav_colour" class="form-label">Favorite Color</label>
        <input type="text" id="fav_colour" v-model="fav_colour" class="form-control" required maxlength="80" />
        <small class="form-text text-muted">Maximum 80 characters</small>
      </div>

      <div class="form-group mb-3">
        <label for="fav_school_subject" class="form-label">Favorite School Subject</label>
        <input type="text" id="fav_school_subject" v-model="fav_school_subject" class="form-control" required maxlength="80" />
        <small class="form-text text-muted">Maximum 80 characters</small>
      </div>

      <div class="form-group mb-3">
        <div class="form-check">
          <input type="checkbox" id="political" v-model="political" class="form-check-input" />
          <label for="political" class="form-check-label">Political</label>
        </div>
      </div>

      <div class="form-group mb-3">
        <div class="form-check">
          <input type="checkbox" id="religious" v-model="religious" class="form-check-input" />
          <label for="religious" class="form-check-label">Religious</label>
        </div>
      </div>

      <div class="form-group mb-3">
        <div class="form-check">
          <input type="checkbox" id="family_oriented" v-model="family_oriented" class="form-check-input" />
          <label for="family_oriented" class="form-check-label">Family Oriented</label>
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="photo" class="form-label">Profile Photo</label>
        <input type="file" id="photo" @change="onFileChange" class="form-control" required />
      </div>

      <button type="submit" class="btn btn-primary">Save Profile</button>

      <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
      <div v-if="errors.length" class="alert alert-danger mt-3">
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Emits
const emit = defineEmits(['submit-success']);

// Form data
const description = ref('');
const parish = ref('');
const biography = ref('');
const sex = ref('');
const race = ref('');
const birth_year = ref('');
const height = ref('');
const fav_cuisine = ref('');
const fav_colour = ref('');
const fav_school_subject = ref('');
const political = ref(false);
const religious = ref(false);
const family_oriented = ref(false);
const photo = ref(null);

// Status messages
const message = ref('');
const errors = ref([]);

// Computed values
const currentYear = computed(() => new Date().getFullYear());

// File handling
const onFileChange = (event) => {
  photo.value = event.target.files[0];
};

// Validation
const validateAge = () => {
  if (!birth_year.value) return true;
  const age = currentYear.value - birth_year.value;
  return age >= 18;
};

const csrf_token = ref('');

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((res) => res.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((err) => {
      console.error("Failed to fetch CSRF token:", err);
    });
}

onMounted(() => {
  getCsrfToken();
});


// Form submission
const submitProfile = async () => {
  // Clear previous messages/errors
  message.value = '';
  errors.value = [];
  
  // Form validation
  let isValid = true;

  if (!description.value.trim()) {
    errors.value.push('Description is required');
    isValid = false;
  }

  if (!parish.value.trim()) {
    errors.value.push('Parish is required');
    isValid = false;
  }

  if (!biography.value.trim()) {
    errors.value.push('Biography is required');
    isValid = false;
  }

  if (!sex.value) {
    errors.value.push('Sex is required');
    isValid = false;
  }

  if (!race.value.trim()) {
    errors.value.push('Race is required');
    isValid = false;
  }

  if (!birth_year.value) {
    errors.value.push('Birth year is required');
    isValid = false;
  } else if (!validateAge()) {
    errors.value.push('You must be at least 18 years old');
    isValid = false;
  }

  if (!height.value) {
    errors.value.push('Height is required');
    isValid = false;
  }

  if (!fav_cuisine.value.trim()) {
    errors.value.push('Favorite cuisine is required');
    isValid = false;
  }

  if (!fav_colour.value.trim()) {
    errors.value.push('Favorite color is required');
    isValid = false;
  }

  if (!fav_school_subject.value.trim()) {
    errors.value.push('Favorite school subject is required');
    isValid = false;
  }

  if (!photo.value) {
    errors.value.push('Profile photo is required');
    isValid = false;
  }

  if (!isValid) return;

  // Prepare form data for submission
  const formData = new FormData();
  formData.append('description', description.value);
  formData.append('parish', parish.value);
  formData.append('biography', biography.value);
  formData.append('sex', sex.value);
  formData.append('race', race.value);
  formData.append('birth_year', birth_year.value);
  formData.append('height', height.value);
  formData.append('fav_cuisine', fav_cuisine.value);
  formData.append('fav_colour', fav_colour.value);
  formData.append('fav_school_subject', fav_school_subject.value);
  formData.append('political', political.value);
  formData.append('religious', religious.value);
  formData.append('family_oriented', family_oriented.value);
  formData.append('photo', photo.value);

  try {
    const response = await fetch('/api/profiles', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrf_token.value
      },
      credentials: 'include' // IMPORTANT if using session auth
    });

    const data = await response.json();

    if (response.ok) {
      // Emit success and pass the profile ID or any relevant data
      emit('submit-success', data.profileId);  // Adjust depending on the API response
      message.value = 'Profile successfully created!';
      window.location.href = `/profiles/${data.profileId}`;  // Redirect to the new profile page
    } else {
      console.error('Profile creation error:', data.errors || data);
      errors.value.push(data.errors || 'An error occurred');
    }
  } catch (err) {
    console.error('Error submitting profile:', err);
    errors.value.push('An error occurred while submitting your profile.');
  }
};

</script>

<style scoped>
.profile-form-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.form-title {
  margin-bottom: 20px;
  text-align: center;
}
.form-group {
  margin-bottom: 15px;
}
.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}
.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
}
.form-text {
  font-size: 0.875em;
  margin-top: 0.25rem;
}
.form-check {
  display: flex;
  align-items: center;
}
.form-check-input {
  margin-right: 8px;
}
.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}
.btn-primary:hover {
  background-color: #0069d9;
}
.alert {
  padding: 10px 15px;
  border-radius: 4px;
  margin-top: 15px;
}
.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
  