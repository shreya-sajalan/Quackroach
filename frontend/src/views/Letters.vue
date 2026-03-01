<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const letters = ref([])
const router = useRouter()

// --- Modal & Decryption State ---
const selectedLetter = ref(null)
const showViewModal = ref(false)
const vaultPassword = ref('')
const decryptedContent = ref('')
const isDecrypting = ref(false)
const decryptError = ref('')

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/letters/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    letters.value = res.data
  } catch (e) { console.error("Fetch failed", e) }
})

// --- Cryptography Helpers ---
function base64ToBuffer(base64) {
  const binary_string = window.atob(base64)
  const bytes = new Uint8Array(binary_string.length)
  for (let i = 0; i < binary_string.length; i++) bytes[i] = binary_string.charCodeAt(i)
  return bytes
}

async function deriveKey(password, salt) {
  const enc = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"])
  return crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: 250000, hash: "SHA-256" }, 
    keyMaterial, 
    { name: "AES-GCM", length: 256 }, 
    false, 
    ["decrypt"]
  )
}

// --- Action Functions ---
const openLetter = (letter) => {
  selectedLetter.value = letter
  showViewModal.value = true
  decryptedContent.value = ''
  decryptError.value = ''
  vaultPassword.value = ''
}

const closeLetter = () => {
  showViewModal.value = false
  selectedLetter.value = null
  decryptedContent.value = ''
  vaultPassword.value = ''
}

const handleDecrypt = async () => {
  isDecrypting.value = true
  decryptError.value = ''
  try {
    const salt = base64ToBuffer(selectedLetter.value.salt)
    const iv = base64ToBuffer(selectedLetter.value.iv)
    const ciphertext = base64ToBuffer(selectedLetter.value.ciphertext)
    
    const key = await deriveKey(vaultPassword.value, salt)
    const decrypted = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, ciphertext)
    
    const dec = new TextDecoder()
    decryptedContent.value = dec.decode(decrypted)
    vaultPassword.value = '' // Clear password immediately
  } catch (e) {
    decryptError.value = "Incorrect password or corrupted data."
  } finally {
    isDecrypting.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl mt-10">
    <div class="flex justify-between items-start mb-12">
      <header>
        <h2 class="text-4xl font-serif font-bold mb-2 text-white">Legacy Letters</h2>
        <p class="text-gray-400 text-lg">Your encrypted words, waiting for their time.</p>
      </header>
      <button @click="router.push('/add-letter')" class="bg-[#E5B869] hover:bg-[#d0a75d] text-black font-semibold py-3 px-6 rounded-xl flex items-center space-x-2 transition shadow-lg">
        <ion-icon name="create-outline" class="text-xl"></ion-icon>
        <span>Write New</span>
      </button>
    </div>

    <div v-if="letters.length === 0" class="text-center py-20 text-gray-500 border border-dashed border-gray-800 rounded-2xl">
      No letters written yet.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="letter in letters" 
        :key="letter.id" 
        @click="openLetter(letter)"
        class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 hover:border-[#E5B869] transition-all flex items-center justify-between group cursor-pointer"
      >
        <div class="flex items-center space-x-4">
          <div class="w-10 h-10 rounded-full bg-red-900/20 flex items-center justify-center">
            <ion-icon name="mail-outline" class="text-red-500"></ion-icon>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white uppercase tracking-tight">To: {{ letter.recipient }}</h3>
            <p class="text-xs text-gray-500">Locked on {{ new Date(letter.created_at).toLocaleDateString() }}</p>
          </div>
        </div>
        <ion-icon name="chevron-forward-outline" class="text-gray-600 group-hover:text-[#E5B869]"></ion-icon>
      </div>
    </div>

    <div v-if="showViewModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
      <div class="bg-[#0e1016] border border-gray-800 rounded-3xl p-8 max-w-lg w-full shadow-2xl relative">
        <button @click="closeLetter" class="absolute top-4 right-4 text-gray-500 hover:text-white transition">
          <ion-icon name="close-outline" class="text-3xl"></ion-icon>
        </button>

        <h3 class="text-2xl font-serif font-bold text-[#E5B869] mb-1">Letter to {{ selectedLetter?.recipient }}</h3>
        <p class="text-gray-500 text-sm mb-6">Encrypted on {{ new Date(selectedLetter?.created_at).toLocaleDateString() }}</p>

        <div v-if="!decryptedContent" class="space-y-4">
          <p class="text-gray-300 text-sm">Enter your Vault Password to unlock and read this letter.</p>
          <input 
            v-model="vaultPassword" 
            type="password" 
            placeholder="Vault Password" 
            class="w-full p-4 bg-black border border-gray-800 rounded-xl text-white text-center tracking-widest focus:border-[#E5B869] outline-none"
          />
          <p v-if="decryptError" class="text-red-500 text-xs font-medium">{{ decryptError }}</p>
          <button 
            @click="handleDecrypt" 
            :disabled="isDecrypting"
            class="w-full bg-[#E5B869] text-black font-bold py-4 rounded-xl hover:scale-[1.02] transition disabled:opacity-50"
          >
            {{ isDecrypting ? 'Decrypting...' : 'Unlock Letter' }}
          </button>
        </div>

        <div v-else class="bg-[#12141c] p-6 rounded-2xl border border-gray-800 max-h-[60vh] overflow-y-auto">
          <p class="text-gray-200 whitespace-pre-wrap leading-relaxed">{{ decryptedContent }}</p>
        </div>
      </div>
    </div>
  </div>
</template>