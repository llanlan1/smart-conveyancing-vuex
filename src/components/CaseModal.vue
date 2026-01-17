<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <v-col md="6" class="dialog-card-text-half-content">
        <v-row class="dialog-card-text-title-without-border">
          <v-col md="4">
            <!-- New case: show text field for reference input -->
            <v-text-field
              v-if="isNew"
              v-model="newReferenceInput.value"
              placeholder="Enter Reference Number"
              variant="outlined"
              density="compact"
              class="reference-input"
              hide-details
            ></v-text-field>
            <!-- Existing case: show reference as title -->
            <v-card-title v-else>{{ modalTitle }}</v-card-title>
          </v-col>
          <!-- TODO: more actions to be added -->
          <v-col md="4" class="d-flex align-center">
            <v-btn
              color="grey-darken-4"
              rounded="lg"
              outlined
              block
              prepend-icon="mdi-tray-arrow-down"
            >
              Download Cover
            </v-btn>
          </v-col>
          <v-col md="4" class="d-flex align-center">
            <v-btn color="grey-darken-4" rounded="lg" outlined block prepend-icon="mdi-printer"
              >Print All</v-btn
            >
          </v-col>
        </v-row>
        <v-row class="dialog-card-text-without-border"> </v-row>
        <v-row class="dialog-card-text-with-border rounded-xl"> </v-row>
      </v-col>
      <v-col md="6" class="dialog-card-text-half-content dialog-card-text-with-border rounded-xl">
        <!-- TODO: Top right corner cancel button to be added -->
        <v-row dense align-start class="tight-row">
          <v-col
            v-for="(field, index) in fields"
            :key="index"
            :md="field.md"
            class="dialog-card-text-fields"
          >
            <v-label class="dialog-card-text-fields-label">{{ field.label }}</v-label>
            <!-- Text / Email -->
            <v-text-field
              dense
              v-if="field.type === 'text' || field.type === 'email'"
              v-model="form[field.model]"
              :type="field.type"
              variant="outlined"
            ></v-text-field>

            <!-- Select -->
            <v-select
              dense
              v-else-if="field.type === 'select'"
              v-model="form[field.model]"
              :items="field.options"
            ></v-select>
            <!-- TODO: more fields to be added -->
          </v-col>
        </v-row>
        <v-spacer></v-spacer>
        <v-row class="dialog-card-submit-row">
          <v-btn block class="h-100" color="grey-darken-2" @click="submit"
            >Submit and Close</v-btn
          ></v-row
        >
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'

// Props interface
interface CaseData {
  name: string
  reference: string
  systemReference: string
  address: string
  caseType: string
  client: string
  team: string
  status?: string
  shortfall?: string
}

const props = defineProps<{
  isNew: boolean
  caseData: CaseData | null
}>()

// Computed title - shows reference for existing case
const modalTitle = computed(() => {
  if (props.isNew) {
    return '' // Will show text field instead
  }
  return props.caseData?.reference || 'Case Details'
})

// Reference input for new cases
const newReferenceInput = reactive({
  value: ''
})

// Watch for changes to reset the input when opening a new case
watch(() => props.isNew, (isNew) => {
  if (isNew) {
    newReferenceInput.value = ''
  }
})

// TODO: demo data to be removed
const fields = [
  { type: 'text', label: 'First Name', md: 6, model: 'firstName' },
  { type: 'text', label: 'Last Name', md: 6, model: 'lastName' },
  { type: 'email', label: 'Email', md: 12, model: 'email' },
  { type: 'select', label: 'Country', md: 6, model: 'country', options: ['USA', 'Canada', 'UK'] },
  { type: 'text', label: 'City', md: 6, model: 'city' },
  { type: 'text', label: 'City', md: 6, model: 'city' },
  { type: 'text', label: 'City', md: 6, model: 'city' },
  { type: 'text', label: 'City', md: 6, model: 'city' },
  { type: 'email', label: 'Email', md: 9, model: 'email' },
  { type: 'text', label: 'Random Name', md: 6, model: 'firstName' },

]

const form = reactive<Record<string, string>>({})

fields.forEach((f) => {
  form[f.model] = '' // initialize reactive model
})

function submit() {
  console.log(form)
  // Include the reference for new cases
  if (props.isNew && newReferenceInput.value) {
    console.log('New case reference:', newReferenceInput.value)
  }
}
</script>

<style scoped>
.reference-input {
  max-width: 200px;
}
</style>
