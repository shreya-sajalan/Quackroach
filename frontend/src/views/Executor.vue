<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const executor = ref(null)
const formData = ref({
  name: '',
  email: '',
  phone: '',
  relationship: ''
})
const isLoading = ref(true)
const isSaving = ref(false)

// This should GET the data when the page loads
const fetchExecutor = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/executor/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    executor.value = res.data
  } catch (e) {
    executor.value = null
  } finally {
    isLoading.value = false
  }
}

// This should POST the data when you click the button
const handleAssign = async () => {
  isSaving.value = true
  try {
    const token = localStorage.getItem('access_token')
    await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/executor/`, formData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    // After successfully saving, fetch the new data to update the UI
    await fetchExecutor()
  } catch (e) {
    console.error("Assignment failed", e)
  } finally {
    isSaving.value = false
  }
}

onMounted(fetchExecutor)
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl mt-10">
    <header class="mb-12">
      <h2 class="text-4xl font-serif font-bold text-white mb-2">The Executor</h2>
      <p class="text-gray-400 text-lg">The one person who will bridge the gap between your life and your legacy.</p>
    </header>

    <div v-if="isLoading" class="text-center py-20 text-gray-500">Loading system status...</div>

    <div v-else>
      <div v-if="executor" class="bg-[#12141c] border border-gray-800 rounded-3xl p-8 shadow-xl">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-full bg-[#E5B869]/10 flex items-center justify-center text-[#E5B869]">
              <ion-icon name="person-outline" class="text-3xl"></ion-icon>
            </div>
            <div>
              <h3 class="text-2xl font-bold text-white">{{ executor.name }}</h3>
              <p class="text-[#E5B869] font-medium">{{ executor.relationship }}</p>
            </div>
          </div>
          <div class="px-4 py-1 rounded-full border border-green-500/30 bg-green-500/10 text-green-500 text-sm font-bold">
            System: {{ executor.status }}
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="p-4 bg-black/40 rounded-xl border border-gray-800">
            <p class="text-xs text-gray-500 uppercase mb-1">Email Address</p>
            <p class="text-white">{{ executor.email }}</p>
          </div>
          <div class="p-4 bg-black/40 rounded-xl border border-gray-800">
            <p class="text-xs text-gray-500 uppercase mb-1">Access Level</p>
            <p class="text-red-400">Zero Access (Until Verified)</p>
          </div>
        </div>

        <div class="p-6 bg-red-900/10 border border-red-900/20 rounded-2xl">
          <p class="text-sm text-gray-400 leading-relaxed">
            <ion-icon name="shield-half-outline" class="mr-1"></ion-icon>
            <strong>Privacy Guard:</strong> Your executor cannot see your Vault items or read your Legacy Letters. Access is only granted after our verification team confirms a legal death certificate or 6 months of inactivity.
          </p>
        </div>
      </div>

      <div v-else class="max-w-2xl mx-auto bg-[#12141c] border border-gray-800 rounded-3xl p-8 shadow-xl">
        <h3 class="text-2xl font-bold text-white mb-6">Assign Your Executor</h3>
        <form @submit.prevent="handleAssign" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-1">Legal Full Name</label>
            <input v-model="formData.name" type="text" class="w-full p-3 bg-black border border-gray-800 rounded-lg text-white" required />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-400 mb-1">Email Address</label>
              <input v-model="formData.email" type="email" class="w-full p-3 bg-black border border-gray-800 rounded-lg text-white" required />
            </div>
            <div>
              <label class="block text-sm text-gray-400 mb-1">Relationship</label>
              <input v-model="formData.relationship" type="text" placeholder="e.g. Spouse, Lawyer" class="w-full p-3 bg-black border border-gray-800 rounded-lg text-white" required />
            </div>
          </div>
          <button type="submit" :disabled="isSaving" class="w-full bg-[#E5B869] text-black font-bold py-4 rounded-xl mt-4 transition hover:scale-[1.01] shadow-lg">
            {{ isSaving ? 'Securing Relationship...' : 'Nominate Executor' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>