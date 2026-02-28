<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router' // Import the router for redirection
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const router = useRouter() // Initialize the router

// UI State
const activeTab = ref('signin') // Controls which tab is active
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Login Form State
const loginEmail = ref('')
const loginPassword = ref('')

// Signup Form State
const signupName = ref('')
const signupEmail = ref('')
const signupPassword = ref('')

// --- LOGIN LOGIC ---
const handleLogin = async () => {
  // 1. Reset messages and start loading state
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // 2. Send the POST request to Django
    // Note: If you are using standard SimpleJWT, this endpoint might be '/api/token/' instead of '/api/login/'
    const response = await axios.post('http://127.0.0.1:8000/api/login/', {
      email: loginEmail.value,
      password: loginPassword.value
    })

    if (response.status === 200) {
      // 3. Save tokens to localStorage
      localStorage.setItem('access_token', response.data.access || response.data.token)
      if (response.data.refresh) {
        localStorage.setItem('refresh_token', response.data.refresh)
      }
      
      // 4. Redirect to the protected dashboard
      router.push('/dashboard') 
    }

  } catch (error) {
    // 5. Catch and display invalid credentials
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.detail || 
                           error.response.data.error || 
                           "Invalid email or password."
    } else {
      errorMessage.value = "Network error. Please make sure your Django server is running."
    }
    console.error("Login error:", error)
  } finally {
    isLoading.value = false
  }
}

// --- SIGNUP LOGIC ---
const handleSignup = async () => {
  // 1. Reset messages and start loading state
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // 2. Send the POST request to Django
    const response = await axios.post('http://127.0.0.1:8000/api/register/', {
      full_name: signupName.value, 
      email: signupEmail.value,
      password: signupPassword.value
    })

    // 3. Handle successful registration
    if (response.status === 201 || response.status === 200) {
      successMessage.value = 'Account created successfully! Please sign in.'
      
      // Clear the signup form
      signupName.value = ''
      signupEmail.value = ''
      signupPassword.value = ''
      
      // Automatically flip the UI back to the Sign In tab
      activeTab.value = 'signin'
    }

  } catch (error) {
    // 4. Handle errors (e.g., email already exists)
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.error || 
                           error.response.data.detail || 
                           Object.values(error.response.data)[0]?.[0] || 
                           "Registration failed. Please try again."
    } else {
      errorMessage.value = "Network error. Please make sure your Django server is running."
    }
    console.error("Signup error:", error)
  } finally {
    // 5. Stop the loading state
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-[#0d0e15] text-white px-4 font-sans">
    
    <div class="text-center mb-8">
      <h1 class="text-5xl font-bold text-[#e1b86e] mb-2 font-serif tracking-wide">Endura</h1>
      <p class="text-gray-400 text-sm font-medium">Your Digital Legacy Vault</p>
    </div>

    <div class="bg-[#12141c] border border-gray-800 rounded-2xl w-full max-w-md p-6 shadow-2xl">
      
      <Tabs v-model="activeTab" class="w-full">
        
        <TabsList class="grid w-full grid-cols-2 bg-[#090a0f] rounded-xl p-1 mb-8">
          <TabsTrigger 
            value="signin" 
            class="rounded-lg py-2.5 text-sm font-semibold data-[state=active]:bg-[#e1b86e] data-[state=active]:text-black text-gray-500 transition-all"
          >
            Sign In
          </TabsTrigger>
          <TabsTrigger 
            value="signup" 
            class="rounded-lg py-2.5 text-sm font-semibold data-[state=active]:bg-[#e1b86e] data-[state=active]:text-black text-gray-500 transition-all"
          >
            Sign Up
          </TabsTrigger>
        </TabsList>

        <div v-if="successMessage" class="mb-6 p-3 bg-green-500/10 border border-green-500/50 rounded-xl flex items-center gap-3">
          <p class="text-sm text-green-400 font-medium">{{ successMessage }}</p>
        </div>

        <TabsContent value="signin">
          <form @submit.prevent="handleLogin" class="space-y-5">
            
            <div v-if="errorMessage && activeTab === 'signin'" class="mb-2 p-3 bg-red-500/10 border border-red-500/50 rounded-xl flex items-center gap-3">
              <p class="text-sm text-red-400 font-medium">{{ errorMessage }}</p>
            </div>

            <div class="space-y-2">
              <Label for="email" class="text-xs font-semibold text-gray-400 ml-1">Email Address</Label>
              <Input 
                id="email" 
                type="email" 
                v-model="loginEmail" 
                placeholder="you@example.com" 
                class="bg-[#12141c] border-gray-800 focus-visible:ring-1 focus-visible:ring-[#e1b86e] focus-visible:border-[#e1b86e] text-gray-200 h-12 rounded-xl"
                required
              />
            </div>

            <div class="space-y-2">
              <Label for="password" class="text-xs font-semibold text-gray-400 ml-1">Password</Label>
              <Input 
                id="password" 
                type="password" 
                v-model="loginPassword" 
                placeholder="••••••••" 
                class="bg-[#12141c] border-gray-800 focus-visible:ring-1 focus-visible:ring-[#e1b86e] focus-visible:border-[#e1b86e] text-gray-200 h-12 rounded-xl"
                required
              />
            </div>

            <div class="flex justify-end pt-1">
              <a href="#" class="text-xs text-[#e1b86e] hover:text-[#f2ce8a] transition-colors">Forgot password?</a>
            </div>

            <Button 
              type="submit" 
              :disabled="isLoading"
              class="w-full bg-[#e1b86e] hover:bg-[#d0a75d] text-black font-bold h-12 rounded-xl mt-4 text-base disabled:opacity-70 disabled:cursor-not-allowed transition-all"
            >
              <span v-if="isLoading">Signing In...</span>
              <span v-else>Sign In</span>
            </Button>
          </form>
        </TabsContent>

        <TabsContent value="signup">
          <form @submit.prevent="handleSignup" class="space-y-5">
            
            <div v-if="errorMessage && activeTab === 'signup'" class="mb-2 p-3 bg-red-500/10 border border-red-500/50 rounded-xl flex items-center gap-3">
              <p class="text-sm text-red-400 font-medium">{{ errorMessage }}</p>
            </div>

            <div class="space-y-2">
              <Label for="name" class="text-xs font-semibold text-gray-400 ml-1">Full Name</Label>
              <Input 
                id="name" 
                type="text" 
                v-model="signupName" 
                placeholder="James Morrison" 
                class="bg-[#12141c] border-gray-800 focus-visible:ring-1 focus-visible:ring-[#e1b86e] focus-visible:border-[#e1b86e] text-gray-200 h-12 rounded-xl"
                required
              />
            </div>

            <div class="space-y-2">
              <Label for="signup-email" class="text-xs font-semibold text-gray-400 ml-1">Email Address</Label>
              <Input 
                id="signup-email" 
                type="email" 
                v-model="signupEmail" 
                placeholder="you@example.com" 
                class="bg-[#12141c] border-gray-800 focus-visible:ring-1 focus-visible:ring-[#e1b86e] focus-visible:border-[#e1b86e] text-gray-200 h-12 rounded-xl"
                required
              />
            </div>

            <div class="space-y-2">
              <Label for="signup-password" class="text-xs font-semibold text-gray-400 ml-1">Password</Label>
              <Input 
                id="signup-password" 
                type="password" 
                v-model="signupPassword" 
                placeholder="••••••••" 
                class="bg-[#12141c] border-gray-800 focus-visible:ring-1 focus-visible:ring-[#e1b86e] focus-visible:border-[#e1b86e] text-gray-200 h-12 rounded-xl"
                required
                minlength="8"
              />
            </div>

            <Button 
              type="submit" 
              :disabled="isLoading"
              class="w-full bg-[#e1b86e] hover:bg-[#d0a75d] text-black font-bold h-12 rounded-xl mt-2 text-base disabled:opacity-70 disabled:cursor-not-allowed transition-all"
            >
              <span v-if="isLoading">Creating Account...</span>
              <span v-else>Create Account</span>
            </Button>

            <p class="text-center text-[11px] text-gray-500 mt-4">
              By creating an account, you agree to our Terms of Service
            </p>
          </form>
        </TabsContent>

      </Tabs>
    </div>
  </div>
</template>