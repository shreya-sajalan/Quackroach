<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// --- 1. The Strict Frontend Schema ---
// This defines the exact structure you requested, completely hidden from the backend.
const assetCategories = {
  personal: {
    title: "Personal Information",
    icon: "person-outline",
    subtypes: {
      identity: {
        title: "Core Identity",
        fields: [
          { key: 'fullName', label: 'Full Name', type: 'text' },
          { key: 'dob', label: 'Date of Birth', type: 'date' },
          { key: 'govId', label: 'Gov ID (PAN/Aadhaar/Passport)', type: 'text' },
          { key: 'nationality', label: 'Nationality', type: 'text' },
          { key: 'bloodGroup', label: 'Blood Group', type: 'text' },
          { key: 'emergencyContact', label: 'Emergency Contact', type: 'text' },
          { key: 'address', label: 'Residential Address', type: 'text' },
          { key: 'taxId', label: 'Tax ID Number', type: 'text' },
        ]
      }
    }
  },
  financial: {
    title: "Financial Assets",
    icon: "wallet-outline",
    subtypes: {
      bank: {
        title: "Bank Account",
        fields: [
          { key: 'bankName', label: 'Bank Name', type: 'text' },
          { key: 'accType', label: 'Account Type (Savings/Current)', type: 'text' },
          { key: 'accNum', label: 'Account Number', type: 'text' },
          { key: 'ifsc', label: 'IFSC / SWIFT', type: 'text' },
          { key: 'branch', label: 'Branch', type: 'text' },
          { key: 'nominee', label: 'Nominee Name', type: 'text' },
          { key: 'linkedContact', label: 'Linked Mobile/Email', type: 'text' },
        ]
      },
      investment: {
        title: "Investment Portfolio",
        fields: [
          { key: 'type', label: 'Type (Stocks, Crypto, Mutual Funds)', type: 'text' },
          { key: 'platform', label: 'Platform Name', type: 'text' },
          { key: 'portfolioId', label: 'Portfolio ID / Acc No.', type: 'text' },
          { key: 'value', label: 'Approximate Value', type: 'text' },
          { key: 'access', label: 'Access Instructions', type: 'text' },
        ]
      },
      insurance: {
        title: "Insurance Policy",
        fields: [
          { key: 'provider', label: 'Insurance Provider', type: 'text' },
          { key: 'policyNum', label: 'Policy Number', type: 'text' },
          { key: 'coverage', label: 'Coverage Amount', type: 'text' },
          { key: 'nominee', label: 'Nominee', type: 'text' },
        ]
      }
    }
  },
  digital: {
    title: "Digital Accounts",
    icon: "laptop-outline",
    subtypes: {
      account: {
        title: "Online Account",
        fields: [
          { key: 'platform', label: 'Platform Name (e.g. Google, Binance)', type: 'text' },
          { key: 'url', label: 'URL / Website', type: 'text' },
          { key: 'username', label: 'Username', type: 'text' },
          { key: 'recoveryEmail', label: 'Recovery Email', type: 'text' },
          { key: 'twoFactor', label: '2FA Method', type: 'text' },
          { key: 'backupCodes', label: 'Backup Codes', type: 'text' },
          { key: 'instructions', label: 'Legacy Instructions (e.g. Delete after death)', type: 'text' },
        ]
      }
    }
  },
  physical: {
    title: "Physical Assets",
    icon: "home-outline",
    subtypes: {
      realEstate: {
        title: "Real Estate",
        fields: [
          { key: 'type', label: 'Property Type', type: 'text' },
          { key: 'location', label: 'Location', type: 'text' },
          { key: 'ownership', label: 'Ownership Type (Joint/Sole)', type: 'text' },
          { key: 'regNum', label: 'Registration Number', type: 'text' },
          { key: 'heir', label: 'Nominee / Heir', type: 'text' },
        ]
      },
      vehicle: {
        title: "Vehicle",
        fields: [
          { key: 'type', label: 'Vehicle Type (Car, Bike)', type: 'text' },
          { key: 'regNum', label: 'Registration Number', type: 'text' },
          { key: 'insurance', label: 'Insurance Policy', type: 'text' },
          { key: 'location', label: 'Physical Location', type: 'text' },
        ]
      }
    }
  }
}

// --- UI State ---
const selectedCategory = ref(null)
const selectedSubtype = ref(null)
const formData = ref({})
const vaultPassword = ref('')
const isEncrypting = ref(false)
const errorMessage = ref('')

// Handle selection
const selectSubtype = (catKey, subKey) => {
  selectedCategory.value = catKey
  selectedSubtype.value = subKey
  formData.value = {} // Reset form
}

// --- Cryptography Engine ---
function bufferToBase64(buffer) {
  let binary = ''; const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
  return window.btoa(binary);
}
function base64ToBuffer(base64) {
  const binary_string = window.atob(base64); const len = binary_string.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = binary_string.charCodeAt(i);
  return bytes;
}
async function deriveKey(password, salt) {
  const enc = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"])
  return crypto.subtle.deriveKey({ name: "PBKDF2", salt: salt, iterations: 250000, hash: "SHA-256" }, keyMaterial, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"])
}
async function encryptVault(password, dataObj) {
  const enc = new TextEncoder()
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const salt = crypto.getRandomValues(new Uint8Array(16))
  const key = await deriveKey(password, salt)
  const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, enc.encode(JSON.stringify(dataObj)))
  return { ciphertext: bufferToBase64(encrypted), iv: bufferToBase64(iv), salt: bufferToBase64(salt) }
}
async function decryptVault(password, encryptedObj) {
  const dec = new TextDecoder()
  const key = await deriveKey(password, base64ToBuffer(encryptedObj.salt))
  const decrypted = await crypto.subtle.decrypt({ name: "AES-GCM", iv: base64ToBuffer(encryptedObj.iv) }, key, base64ToBuffer(encryptedObj.ciphertext))
  return JSON.parse(dec.decode(decrypted))
}

// --- Save & Encrypt Logic ---
const handleSave = async () => {
  if (!vaultPassword.value) {
    errorMessage.value = "Vault password is required to encrypt this data."
    return
  }
  
  isEncrypting.value = true
  errorMessage.value = ''
  
  try {
    const token = localStorage.getItem('access_token')
    
    // 1. Fetch the existing encrypted vault
    const getRes = await axios.get('http://127.0.0.1:8000/api/vault/', { headers: { Authorization: `Bearer ${token}` }})
    
    let currentData = { items: [] }
    
    // 2. Decrypt it to append the new item (if it exists)
    if (getRes.data.ciphertext) {
      currentData = await decryptVault(vaultPassword.value, getRes.data)
      if (!currentData.items) currentData.items = []
    }

    // 3. Format the new item
    const newItem = {
      id: Date.now(),
      title: formData.value[assetCategories[selectedCategory.value].subtypes[selectedSubtype.value].fields[0].key] || 'Unnamed Asset', // Uses first field as title
      type: assetCategories[selectedCategory.value].subtypes[selectedSubtype.value].title,
      details: 'Added on ' + new Date().toLocaleDateString(),
      icon: assetCategories[selectedCategory.value].icon,
      data: formData.value // The full nested structured data!
    }

    // 4. Append and Re-encrypt
    currentData.items.push(newItem)
    const encryptedPackage = await encryptVault(vaultPassword.value, currentData)
    encryptedPackage.item_count = currentData.items.length
    // 5. Save back to Django
    await axios.post('http://127.0.0.1:8000/api/vault/', encryptedPackage, { headers: { Authorization: `Bearer ${token}` }})

    router.push('/vault')
  } catch (error) {
    console.error(error)
    errorMessage.value = "Encryption failed. Incorrect password or network error."
  } finally {
    isEncrypting.value = false
  }
}
</script>

<template>
  <div class="container mx-auto  py-5 mt-8 max-w-5xl">
    
    <header class="mb-10 border-b border-gray-800 pb-6 flex items-center gap-4">
      <button @click="router.push('/vault')" class="text-gray-400 hover:text-white transition bg-[#1A1C23] p-2 rounded-full">
        <ion-icon name="arrow-back-outline" class="text-xl"></ion-icon>
      </button>
      <div>
        <h2 class="text-4xl font-serif font-bold mb-2">Add to Vault</h2>
        <p class="text-gray-400 text-lg">Select an asset type to securely encrypt.</p>
      </div>
    </header>

    <div v-if="!selectedSubtype" class="space-y-8">
      <div v-for="(category, catKey) in assetCategories" :key="catKey">
        <h3 class="text-xl font-bold text-[#E5B869] mb-4 flex items-center gap-2">
          <ion-icon :name="category.icon"></ion-icon>
          {{ category.title }}
        </h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <button 
            v-for="(subtype, subKey) in category.subtypes" 
            :key="subKey"
            @click="selectSubtype(catKey, subKey)"
            class="bg-[#12141c] border border-gray-800 rounded-xl p-6 text-left hover:border-[#E5B869] hover:bg-[#1A1C23] transition-all group shadow-lg"
          >
            <h4 class="font-bold text-lg text-white group-hover:text-[#E5B869]">{{ subtype.title }}</h4>
            <p class="text-sm text-gray-500 mt-1">Add a new {{ subtype.title.toLowerCase() }}</p>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="max-w-2xl mx-auto bg-[#12141c] border border-gray-800 rounded-2xl p-8 shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-2xl font-bold text-[#E5B869]">{{ assetCategories[selectedCategory].subtypes[selectedSubtype].title }}</h3>
        <button @click="selectedSubtype = null" class="text-sm text-gray-400 hover:text-white">Change Type</button>
      </div>

      <form @submit.prevent="handleSave" class="space-y-5">
        
        <div v-for="field in assetCategories[selectedCategory].subtypes[selectedSubtype].fields" :key="field.key">
          <label class="block text-sm font-medium text-gray-300 mb-1">{{ field.label }}</label>
          <input 
            v-model="formData[field.key]" 
            :type="field.type" 
            class="w-full p-3 border border-gray-700 rounded-md bg-background text-foreground focus:border-[#E5B869] focus:ring-1 focus:ring-[#E5B869] transition"
            required
          />
        </div>

        <hr class="border-gray-800 my-6" />

        <div class="bg-red-900/20 border border-red-900/50 p-4 rounded-lg">
          <label class="block text-sm font-medium text-red-400 mb-2 flex items-center gap-2">
            <ion-icon name="lock-closed"></ion-icon> Verify Vault Password to Encrypt
          </label>
          <input 
            v-model="vaultPassword" 
            type="password" 
            placeholder="Enter your Vault Password"
            required
            class="w-full p-3 border border-gray-700 rounded-md bg-background text-foreground text-center tracking-widest"
          />
          <p v-if="errorMessage" class="text-red-500 text-sm mt-2 font-medium">{{ errorMessage }}</p>
        </div>

        <button type="submit" :disabled="isEncrypting" class="w-full bg-[#E5B869] hover:bg-[#d0a75d] text-black font-bold p-4 rounded-xl flex items-center justify-center gap-2 transition-transform hover:scale-[1.02] shadow-lg disabled:opacity-50">
          <ion-icon v-if="!isEncrypting" name="shield-checkmark-outline" class="text-xl"></ion-icon>
          <ion-icon v-else name="sync-outline" class="text-xl animate-spin"></ion-icon>
          <span>{{ isEncrypting ? 'Encrypting & Saving...' : 'Encrypt & Save to Vault' }}</span>
        </button>
      </form>
    </div>

  </div>
</template>