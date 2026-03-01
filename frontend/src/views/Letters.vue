<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const letters = ref([])
const router = useRouter()

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get('http://127.0.0.1:8000/api/letters/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    letters.value = res.data
  } catch (e) { console.error("Fetch failed", e) }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl mt-10">
    <div class="flex justify-between items-start mb-12">
      <header>
        <h2 class="text-4xl font-serif font-bold mb-2 text-white">Legacy Letters</h2>
        <p class="text-gray-400 text-lg">Your encrypted words, waiting for their time.</p>
      </header>
      <button @click="router.push('/add-letter')" class="bg-[#E5B869] hover:bg-[#d0a75d] text-black font-semibold py-3 px-6 rounded-xl flex items-center space-x-2 transition-transform hover:scale-105 shadow-lg">
        <ion-icon name="create-outline" class="text-xl"></ion-icon>
        <span>Write New</span>
      </button>
    </div>

    <div v-if="letters.length === 0" class="text-center py-20 text-gray-500 border border-dashed border-gray-800 rounded-2xl">
      No letters written yet.
    </div>

    <div v-else class="space-y-4">
      <div v-for="letter in letters" :key="letter.id" class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 hover:border-[#E5B869] transition-all flex items-center justify-between group">
        <div class="flex items-center space-x-6">
          <div class="w-12 h-12 rounded-full bg-red-900/20 border border-red-900/40 flex items-center justify-center">
            <div class="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]"></div>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white uppercase tracking-tight">To: {{ letter.recipient }}</h3>
            <p class="text-xs text-gray-500 font-mono">ENCRYPTED ID: {{ letter.id }}</p>
          </div>
        </div>
        <div class="text-sm text-gray-500">{{ new Date(letter.created_at).toLocaleDateString() }}</div>
      </div>
    </div>
  </div>
</template>