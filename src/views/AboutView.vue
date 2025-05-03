<template>
  <div class="about-page">
    <!-- Background section that fills empty space -->
    <div class="background-fill"></div>

    <!-- Centered content box -->
    <div class="about-content-box">
      <div class="about-content">
        <h2 class="title">About Jam-Date</h2>

        <p class="lead">
          <strong>Jam-Date</strong> is Jamaica’s freshest digital matchmaking platform — built for islanders who vibe with authenticity, culture, and meaningful connections. 
          Whether you're looking for love, friendship, or just someone to share a good oxtail recipe with, Jam-Date helps you connect with people who match your energy.
        </p>

        <p>
          Designed with Caribbean flair and personality in mind, Jam-Date makes it easy to create rich personal profiles that reflect who you are — from your favourite school subject to how important family is to you. 
          You’re more than just a swipe — and Jam-Date gets that.
        </p>

        <p>
          What makes Jam-Date different? We believe matches should be based on more than just appearance. That’s why our system considers personality traits, lifestyle preferences, and cultural values — giving you real connections, not just random clicks.
        </p>

        <p>
          So whether you’re a Kingston creative, a country soul, or just ready to find your person — Jam-Date is here to help you meet someone who truly fits your vibe.
        </p>

        <p class="note">
          Jam-Date: <span class="gold">Real People. Real Culture. Real Connections.</span>
        </p>
      </div>
    </div>

    <!-- Background section again below the content -->
    <div class="background-fill"></div>
  </div>
</template>

<style scoped>
.about-page {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 75px); 
}

.background-fill {
  flex-grow: 1;
  background-image: url('/images/Home_Page_Background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Centered content section */
.about-content-box {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  background-color: white;
}

.about-content {
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 2rem;
  max-width: 900px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 32px;
  color: #0B6623;
  font-weight: bold;
  margin-bottom: 1rem;
}

.lead {
  font-size: 1.15rem;
  margin-bottom: 1rem;
  color: #333;
}

p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.note {
  font-weight: bold;
  font-style: italic;
  margin-top: 2rem;
  color: #0B6623;
  text-align: center;
}

.gold {
  color: #FFD700;
}
</style>
