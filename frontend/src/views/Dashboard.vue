<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 1. Initialize empty state variables for the UI
const user = ref({ fullname: 'Loading...' })
const completionPercentage = ref(0)
const vaultItemsCount = ref(0)
const lettersCount = ref(0)
const hasExecutor = ref('...')
const lastCheckIn = ref('...')

// 2. Math for the SVG circle animation
const radius = 80
const circumference = 2 * Math.PI * radius
const dashoffset = computed(() => {
  return circumference - (completionPercentage.value / 100) * circumference
})

// 3. Fetch real data from Django when the dashboard loads
onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token') 
    
    if (!token) {
      router.push('/login')
      return
    }
    
    const response = await axios.get('http://127.0.0.1:8000/api/dashboard/', {
      headers: {
        Authorization: `Bearer ${token}` 
      }
    })

    const data = response.data
    user.value.fullname = data.fullname
    completionPercentage.value = data.completionPercentage
    vaultItemsCount.value = data.vaultItemsCount // <--- This is ready for real data!
    lettersCount.value = data.lettersCount
    hasExecutor.value = data.hasExecutor
    lastCheckIn.value = data.lastCheckIn

  } catch (error) {
    console.error("Failed to load dashboard data:", error)
    
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/login')
    }
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    
    <header class="mb-12 border-b border-gray-800 pb-6">
      <h1 class="text-4xl font-serif font-bold text-white mb-2">
        Good to see you, {{ user.fullname }}
      </h1>
      <p class="text-gray-400 text-lg">
        Welcome to your Endura dashboard. Your legacy is currently <span class="text-[#E5B869] font-medium">{{ completionPercentage }}%</span> secured.
      </p>
    </header>

    <div class="flex justify-center my-12">
      <div class="relative flex items-center justify-center">
        <svg class="transform -rotate-90 w-56 h-56">
          <circle cx="112" cy="112" :r="radius" stroke="#1f222e" stroke-width="12" fill="none" />
          <circle 
            cx="112" cy="112" :r="radius" 
            stroke="#E5B869" 
            stroke-width="12" 
            fill="none" 
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="dashoffset"
            class="transition-all duration-1000 ease-out"
          />
        </svg>
        <div class="absolute text-center flex flex-col items-center">
          <span class="text-5xl font-serif font-bold text-[#E5B869]">{{ completionPercentage }}%</span>
          <span class="text-sm font-medium text-gray-400 mt-2 uppercase tracking-widest">Complete</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <div class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 shadow-lg hover:border-gray-700 hover:shadow-xl transition-all">
        <div class="flex items-center space-x-3 text-gray-400 mb-4">
          <ion-icon name="shield-checkmark-outline" class="text-2xl text-[#E5B869]"></ion-icon>
          <span class="text-sm font-medium tracking-wide">Vault Items</span>
        </div>
        <div class="text-4xl font-serif font-bold text-white">{{ vaultItemsCount }}</div>
      </div>
      
      <div class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 shadow-lg hover:border-gray-700 hover:shadow-xl transition-all">
        <div class="flex items-center space-x-3 text-gray-400 mb-4">
          <ion-icon name="document-text-outline" class="text-2xl text-[#E5B869]"></ion-icon>
          <span class="text-sm font-medium tracking-wide">Letters Written</span>
        </div>
        <div class="text-4xl font-serif font-bold text-white">{{ lettersCount }}</div>
      </div>

      <div class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 shadow-lg hover:border-gray-700 hover:shadow-xl transition-all">
        <div class="flex items-center space-x-3 text-gray-400 mb-4">
          <ion-icon name="person-add-outline" class="text-2xl text-[#E5B869]"></ion-icon>
          <span class="text-sm font-medium tracking-wide">Executor Assigned</span>
        </div>
        <div class="text-3xl font-serif font-bold text-white mt-1">{{ hasExecutor }}</div>
      </div>

      <div class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 shadow-lg hover:border-gray-700 hover:shadow-xl transition-all">
        <div class="flex items-center space-x-3 text-gray-400 mb-4">
          <ion-icon name="time-outline" class="text-2xl text-[#E5B869]"></ion-icon>
          <span class="text-sm font-medium tracking-wide">Last Check-in</span>
        </div>
        <div class="text-2xl font-serif font-bold text-white mt-2">{{ lastCheckIn }}</div>
      </div>
      
    </div>
  </div>
</template>