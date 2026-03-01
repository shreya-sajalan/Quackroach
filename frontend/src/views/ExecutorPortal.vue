<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const file = ref(null)
const statusMsg = ref('')
const isUploading = ref(false)

const handleFileUpload = (event) => {
  file.value = event.target.files[0]
}

const submitVerification = async () => {
  if (!file.value) return
  isUploading.value = true
  
  const formData = new FormData()
  formData.append('email', email.value)
  formData.append('document', file.value)

  try {
    await axios.post('http://127.0.0.1:8000/api/verify-executor/', formData)
    statusMsg.value = "Documents submitted successfully. You will be notified once access is granted."
  } catch (e) {
    statusMsg.value = "Verification failed. Please ensure the email matches the one in our records."
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#0e1016] flex items-center justify-center p-6">
    <div class="max-w-xl w-full bg-[#12141c] border border-gray-800 rounded-3xl p-10 shadow-2xl">
      <div class="text-center mb-8">
          <h2 class="text-3xl font-serif font-bold text-[#E5B869] mb-2">Executor Verification</h2>
          <p class="text-gray-400">Please provide documentation to begin the legacy handover process.</p>
      </div>

      <div class="space-y-6">
        <div>
          <label class="block text-sm text-gray-500 mb-2 uppercase tracking-widest">Confirm Your Email</label>
          <input v-model="email" type="email" class="w-full p-4 bg-black border border-gray-800 rounded-xl text-white outline-none focus:border-[#E5B869]" placeholder="your@email.com" />
        </div>

        <div class="border-2 border-dashed border-gray-800 rounded-2xl p-8 text-center hover:border-[#E5B869] transition-colors cursor-pointer relative">
          <input type="file" @change="handleFileUpload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
          <ion-icon name="cloud-upload-outline" class="text-4xl text-gray-600 mb-2"></ion-icon>
          <p class="text-gray-400">{{ file ? file.name : 'Upload Death Certificate or ID' }}</p>
        </div>

        <button @click="submitVerification" :disabled="isUploading" class="w-full bg-[#E5B869] text-black font-bold py-4 rounded-xl hover:scale-[1.01] transition disabled:opacity-50">
          {{ isUploading ? 'Uploading...' : 'Submit for Verification' }}
        </button>

        <p v-if="statusMsg" class="text-center text-sm text-[#E5B869] mt-4 font-medium">{{ statusMsg }}</p>
      </div>
    </div>
  </div>
</template>