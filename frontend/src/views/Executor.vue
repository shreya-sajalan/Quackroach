<script setup>
import { ref } from 'vue'

// Mock data to visualize the layout before we connect your Django backend
const executors = ref([
  { id: 1, name: 'Jane Doe', email: 'jane.doe@example.com', relationship: 'Spouse', status: 'Active' },
  { id: 2, name: 'John Smith', email: 'john.smith@example.com', relationship: 'Attorney', status: 'Pending Invitation' }
])
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl">
    
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Trusted Executors</h1>
        <p class="text-muted-foreground mt-2">Manage the people authorized to access your AfterMe vault.</p>
      </div>
      <button class="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md font-medium text-sm transition-colors">
        Add New Executor
      </button>
    </div>

    <div class="border rounded-lg bg-card text-card-foreground shadow-sm">
      <div class="p-6">
        
        <div v-if="executors.length === 0" class="text-center py-10 text-muted-foreground">
          You haven't added any executors yet.
        </div>
        
        <div v-else class="space-y-4">
          <div 
            v-for="executor in executors" 
            :key="executor.id" 
            class="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 border rounded-md gap-4"
          >
            <div>
              <h3 class="font-medium text-lg">{{ executor.name }}</h3>
              <p class="text-sm text-muted-foreground">{{ executor.email }} • {{ executor.relationship }}</p>
            </div>
            
            <div class="flex items-center gap-4">
              <span :class="[
                'px-2.5 py-0.5 rounded-full text-xs font-semibold',
                executor.status === 'Active' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
              ]">
                {{ executor.status }}
              </span>
              <button class="text-sm text-red-500 hover:text-red-700 font-medium transition-colors">
                Remove
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
    
  </div>
</template>