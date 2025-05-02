<template>
      <footer class="footer">
          <div class="container">
              <p>Copyright &copy {{ year }} JJBSAS Inc.</p>
          </div>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
.footer {
  background-color: black;
  color: #FFD700;
  text-align: center;
  padding: 1rem;
  margin-top: 2rem;
}

.footer-container {
  max-width: 900px;
  margin: 0 auto;
}

.footer-text {
  font-weight: bold;
  margin: 0;
}
</style>