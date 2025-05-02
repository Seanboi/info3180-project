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
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import jamDateLogo from "@/assets/JamDate_Logo.png";
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