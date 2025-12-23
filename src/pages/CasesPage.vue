<template>
  <v-card class="card-layout">
    <v-card-title>Cases Management</v-card-title>
    <v-card-text>
      <v-row dense>
        <v-col cols="12" md="4">
          <v-select
            label="Time Filter"
            :items="timeFilters"
            v-model="selectTimeFilter"
            clearable
            dense
            variant="outlined"
            rounded="lg"
          />
        </v-col>
        <v-col cols="12" md="5">
          <!-- Placeholder for future filter -->
        </v-col>
        <v-col cols="12" md="3">
          <v-btn
            prepend-icon="mdi-plus"
            color="grey-darken-4"
            rounded="xl"
            size="x-large"
            block
            @click="openNewCaseModal"
          >
            New Case</v-btn
          >
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="12" md="6">
          <v-text-field
            label="Search"
            prepend-inner-icon="mdi-magnify"
            v-model="search"
            clearable
            variant="outlined"
            rounded="lg"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            label="All Statuses"
            :items="statuses"
            v-model="selectedStatuses"
            clearable
            variant="outlined"
            rounded="lg"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            label="All Case Types"
            :items="caseTypes"
            v-model="selectedCaseTypes"
            multiple
            clearable
            variant="outlined"
            rounded="lg"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
  <v-dialog v-model="isCaseModalOpen" class="dialog-90" fullscreen hide-overlay>
    <CaseModal />
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CaseModal from '@/components/CaseModal.vue'

const search = ref('')
const selectedStatuses = ref(null)
const selectedCaseTypes = ref(null)
const selectTimeFilter = ref(null)
const isCaseModalOpen = ref(false)

function openNewCaseModal() {
  console.log('New Case button clicked - open modal!')

  isCaseModalOpen.value = true
}

// demo data
const statuses = ['Open', 'In Progress', 'Closed']
const caseTypes = ['Personal Injury', 'Property', 'Contract']
const timeFilters = ['Last 7 Days', 'Last 30 Days', 'Last Year']
</script>
