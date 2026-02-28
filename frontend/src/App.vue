<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div class="relative flex min-h-screen flex-col bg-background text-foreground">
    <Navbar />

    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>