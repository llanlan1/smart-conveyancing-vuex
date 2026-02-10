<template>
  <div class="role-selector">
    <v-label class="dialog-card-text-fields-label">Role</v-label>
    <div class="d-flex align-center">
      <v-select
        v-model="selectedRole"
        :items="roleOptions"
        variant="outlined"
        rounded="lg"
        density="compact"
        hide-details
        style="max-width: 150px"
      ></v-select>
      <v-btn-toggle
        v-model="selectedType"
        mandatory
        rounded="xl"
        density="compact"
        class="ml-auto"
        color="grey-darken-4"
      >
        <v-btn value="individual" class="text-none">Individual</v-btn>
        <v-btn value="corporate" class="text-none">Corporate</v-btn>
      </v-btn-toggle>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  role?: string
  type?: 'individual' | 'corporate'
  roleOptions?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:role', value: string): void
  (e: 'update:type', value: 'individual' | 'corporate'): void
}>()

const selectedRole = ref(props.role || '')
const selectedType = ref<'individual' | 'corporate'>(props.type || 'individual')

const roleOptions = props.roleOptions || ['Client', 'Agent', 'Lawyer']

watch(selectedRole, (val) => emit('update:role', val))
watch(selectedType, (val) => emit('update:type', val))
</script>
