<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const recipient = ref('')
const content = ref('')
const vaultPassword = ref('')
const isEncrypting = ref(false)
const errorMessage = ref('')

// --- Crypto Engine (PBKDF2 + AES-GCM) ---
async function deriveKey(password, salt) {
  const enc = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"])
  return crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: 250000, hash: "SHA-256" }, 
    keyMaterial, 
    { name: "AES-GCM", length: 256 }, 
    false, 
    ["encrypt"]
  )
}

async function encryptLetter(password, text) {
  const enc = new TextEncoder()
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const salt = crypto.getRandomValues(new Uint8Array(16))
  const key = await deriveKey(password, salt)
  const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, enc.encode(text))
  
  return {
    ciphertext: btoa(String.fromCharCode(...new Uint8Array(encrypted))),
    iv: btoa(String.fromCharCode(...iv)),
    salt: btoa(String.fromCharCode(...salt))
  }
}

const handleSaveLetter = async () => {
  if (!vaultPassword.value) {
    errorMessage.value = "Vault password is required to seal this letter."
    return
  }
  
  isEncrypting.value = true
  errorMessage.value = ''
  
  try {
    const encrypted = await encryptLetter(vaultPassword.value, content.value)
    const token = localStorage.getItem('access_token')
    
    await axios.post('http://127.0.0.1:8000/api/letters/', {
      recipient: recipient.value,
      ...encrypted
    }, { headers: { Authorization: `Bearer ${token}` } })

    router.push('/letters')
  } catch (e) {
    errorMessage.value = "Encryption failed. Is your Vault Password correct?"
    console.error(e)
  } finally {
    isEncrypting.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-3xl mt-10">
    <header class="mb-8 flex items-center gap-4">
      <button @click="router.push('/letters')" class="text-gray-400 hover:text-white transition bg-[#1A1C23] p-2 rounded-full">
        <ion-icon name="arrow-back-outline" class="text-xl"></ion-icon>
      </button>
      <h2 class="text-3xl font-serif font-bold text-white">Write Legacy Letter</h2>
    </header>

    <form @submit.prevent="handleSaveLetter" class="space-y-6">
      <div class="bg-[#12141c] border border-gray-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <input 
          v-model="recipient" 
          type="text" 
          placeholder="To (Recipient Name)" 
          class="w-full bg-transparent text-xl font-bold border-b border-gray-800 pb-2 focus:border-[#E5B869] outline-none text-white" 
          required 
        />
        <textarea 
          v-model="content" 
          placeholder="Write your final words here. This content will be encrypted locally..." 
          class="w-full h-64 bg-transparent border-none focus:ring-0 text-gray-300 resize-none text-lg" 
          required
        ></textarea>
      </div>

      <div class="bg-red-900/10 border border-red-900/30 p-5 rounded-xl">
        <label class="block text-sm font-medium text-red-400 mb-2 flex items-center gap-2">
          <ion-icon name="lock-closed"></ion-icon> Seal with Vault Password
        </label>
        <input 
          v-model="vaultPassword" 
          type="password" 
          placeholder="••••••••" 
          class="w-full p-3 bg-black border border-gray-800 rounded-lg text-center tracking-widest text-white" 
          required 
        />
        <p v-if="errorMessage" class="text-red-500 text-sm mt-2 font-medium">{{ errorMessage }}</p>
      </div>

      <button 
        type="submit" 
        :disabled="isEncrypting" 
        class="w-full bg-[#E5B869] text-black font-bold py-4 rounded-xl transition hover:scale-[1.02] flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
      >
        <ion-icon v-if="!isEncrypting" name="mail-unread-outline" class="text-xl"></ion-icon>
        <ion-icon v-else name="sync" class="animate-spin text-xl"></ion-icon>
        <span>{{ isEncrypting ? 'Encrypting Letter...' : 'Seal & Store Legacy Letter' }}</span>
      </button>
    </form>
  </div>
</template>