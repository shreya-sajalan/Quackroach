<script setup>
import { ref } from 'vue'
import axios from 'axios'

const executorEmail = ref('')
const targetEmail = ref('')
const vaultPassword = ref('')
const statusMsg = ref('')
const isUnlocking = ref(false)

const decryptedVault = ref([])
const decryptedLetters = ref([])
const hasUnlocked = ref(false)

// --- Helper: Clean Base64 Strings ---
// Removes Python byte-string artifacts (e.g., b'...') and whitespace
const cleanBase64 = (str) => {
  if (!str) return '';
  let s = String(str).trim();
  if ((s.startsWith("b'") && s.endsWith("'")) || (s.startsWith('b"') && s.endsWith('"'))) {
    s = s.substring(2, s.length - 1);
  }
  return s.replace(/\s+/g, '');
};

// --- Web Crypto API Decryption Logic ---
const decryptData = async (rawCiphertext, rawIv, rawSalt, password) => {
  try {
    const enc = new TextEncoder();
    const dec = new TextDecoder();

    // 1. Clean the incoming data
    const ciphertextBase64 = cleanBase64(rawCiphertext);
    const ivBase64 = cleanBase64(rawIv);
    const saltBase64 = cleanBase64(rawSalt);

    // 2. Decode Base64 into Uint8Arrays
    const ciphertext = Uint8Array.from(atob(ciphertextBase64), c => c.charCodeAt(0));
    const iv = Uint8Array.from(atob(ivBase64), c => c.charCodeAt(0));
    const salt = Uint8Array.from(atob(saltBase64), c => c.charCodeAt(0));

    // 3. Derive Key using PBKDF2 
    // FIXED: Iterations set to 250000 to match Addvault.vue and AddLetter.vue
    const keyMaterial = await window.crypto.subtle.importKey(
      "raw", enc.encode(password), { name: "PBKDF2" }, false, ["deriveKey"]
    );
    const key = await window.crypto.subtle.deriveKey(
      { name: "PBKDF2", salt: salt, iterations: 250000, hash: "SHA-256" },
      keyMaterial, { name: "AES-GCM", length: 256 }, false, ["decrypt"]
    );

    // 4. Decrypt the ciphertext
    const decryptedBuffer = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv: iv }, key, ciphertext
    );
    
    // 5. Parse the resulting string safely
    const decryptedString = dec.decode(decryptedBuffer);
    try {
      // Vault items are stored as JSON objects
      return JSON.parse(decryptedString);
    } catch (e) {
      // Letters are stored as raw text strings
      return decryptedString; 
    }

  } catch (error) {
    console.error("Decryption failed. Ensure password is correct and parameters match.", error);
    return null; // Return null if decryption fails (e.g., wrong password)
  }
}

const unlockVault = async () => {
  if (!executorEmail.value || !targetEmail.value || !vaultPassword.value) {
    statusMsg.value = "All fields are required."
    return
  }
  
  isUnlocking.value = true
  statusMsg.value = "Authenticating and fetching encrypted payload..."
  decryptedVault.value = []
  decryptedLetters.value = []

  try {
    // Fetch encrypted data from backend
    const response = await axios.post('http://127.0.0.1:8000/api/legacy-data/', {
      executor_email: executorEmail.value,
      target_email: targetEmail.value
    })

    const { vault_items, letters } = response.data
    statusMsg.value = "Data retrieved. Decrypting locally..."

    let decryptionFailed = false;

    // Decrypt Vault Items
    for (const item of vault_items) {
      const decrypted = await decryptData(item.ciphertext, item.iv, item.salt, vaultPassword.value)
      if (decrypted) {
        // Addvault.vue packages items inside an `items` array. We extract them for a cleaner UI.
        if (decrypted.items && Array.isArray(decrypted.items)) {
          decryptedVault.value.push(...decrypted.items)
        } else {
          decryptedVault.value.push(decrypted)
        }
      } else {
        decryptionFailed = true;
      }
    }

    // Decrypt Letters
    for (const letter of letters) {
      const decrypted = await decryptData(letter.ciphertext, letter.iv, letter.salt, vaultPassword.value)
      if (decrypted) {
        decryptedLetters.value.push({ recipient: letter.recipient, content: decrypted })
      } else {
        decryptionFailed = true;
      }
    }

    if (decryptionFailed) {
      statusMsg.value = "Decryption failed. The Vault Password you entered is incorrect."
      decryptedVault.value = []
      decryptedLetters.value = []
    } else {
      statusMsg.value = ""
      hasUnlocked.value = true
    }

  } catch (e) {
    statusMsg.value = e.response?.data?.error || "Failed to connect to the server or retrieve data."
    console.error(e)
  } finally {
    isUnlocking.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#0e1016] mt-9 text-white p-6 font-sans">
    
    <div v-if="!hasUnlocked" class="max-w-xl mx-auto mt-20 bg-[#12141c] border border-gray-800 rounded-3xl p-10 shadow-2xl">
      <div class="text-center mb-8">
          <h2 class="text-3xl font-serif font-bold text-[#E5B869] mb-2">Unlock Legacy Vault</h2>
          <p class="text-gray-400">Enter your credentials and the offline Shared Secret to decrypt the payload.</p>
      </div>

      <div class="space-y-6">
        <div>
          <label class="block text-sm text-gray-500 mb-2 uppercase tracking-widest">Your Email (Executor)</label>
          <input v-model="executorEmail" type="email" class="w-full p-4 bg-black border border-gray-800 rounded-xl outline-none focus:border-[#E5B869]" />
        </div>
        <div>
          <label class="block text-sm text-gray-500 mb-2 uppercase tracking-widest">Target User Email</label>
          <input v-model="targetEmail" type="email" class="w-full p-4 bg-black border border-gray-800 rounded-xl outline-none focus:border-[#E5B869]" />
        </div>
        <div>
          <label class="block text-sm text-gray-500 mb-2 uppercase tracking-widest">Vault Password (Shared Secret)</label>
          <input v-model="vaultPassword" type="password" class="w-full p-4 bg-black border border-gray-800 rounded-xl outline-none focus:border-[#E5B869]" />
        </div>

        <button @click="unlockVault" :disabled="isUnlocking" class="w-full bg-[#E5B869] text-black font-bold py-4 rounded-xl hover:bg-[#d97706] transition disabled:opacity-50">
          {{ isUnlocking ? 'Decrypting Payload...' : 'Unlock Data' }}
        </button>

        <p v-if="statusMsg" class="text-center text-sm mt-4 text-red-400">{{ statusMsg }}</p>
      </div>
    </div>

    <div v-else class="max-w-5xl mx-auto mt-10">
      <div class="text-center mb-10 border-b border-gray-800 pb-6">
        <h2 class="text-4xl font-serif font-bold text-[#4ade80]">Vault Decrypted Successfully</h2>
        <p class="text-gray-400 mt-2">Data is visible only in this secure local session. Do not refresh.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-[#12141c] p-6 rounded-2xl border border-gray-800 shadow-xl">
          <h3 class="text-2xl text-[#E5B869] mb-6 border-b border-gray-800 pb-2">Digital Assets</h3>
          <div v-if="decryptedVault.length === 0" class="text-gray-500 italic">No vault items found.</div>
          
          <div v-for="(item, index) in decryptedVault" :key="index" class="mb-4 p-5 bg-black rounded-xl border border-gray-800">
            <h4 class="text-[#E5B869] font-bold text-lg mb-1 flex items-center gap-2">
               <ion-icon :name="item.icon || 'document-outline'"></ion-icon>
               {{ item.title || 'Secure Asset' }}
            </h4>
            <p class="text-xs text-gray-500 mb-3 uppercase tracking-widest">{{ item.type || 'Unknown Type' }}</p>
            <div class="space-y-2">
              <div v-for="(value, key) in item.data" :key="key" class="text-sm">
                <span class="text-gray-500 capitalize">{{ key.replace(/([A-Z])/g, ' $1').trim() }}:</span> 
                <span class="text-gray-300 font-mono ml-2">{{ value }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-[#12141c] p-6 rounded-2xl border border-gray-800 shadow-xl">
          <h3 class="text-2xl text-[#E5B869] mb-6 border-b border-gray-800 pb-2">Legacy Letters</h3>
          <div v-if="decryptedLetters.length === 0" class="text-gray-500 italic">No letters found.</div>
          
          <div v-for="(letter, index) in decryptedLetters" :key="index" class="mb-6 bg-black p-5 rounded-xl border border-gray-800">
            <h4 class="text-[#E5B869] font-bold mb-3 border-b border-gray-800 pb-2 text-lg">To: {{ letter.recipient }}</h4>
            <p class="text-gray-300 leading-relaxed whitespace-pre-wrap">{{ letter.content }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>