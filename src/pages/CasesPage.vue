<template>
  <v-card class="v-card-no-shadow" style="margin-bottom: 9px">
    <v-row dense align-items="center">
      <v-col cols="12" md="2">
        <v-select
            placeholder="All Time"
            :items="timeFilters"
            v-model="selectTimeFilter"
            clearable
            dense
            variant="plain"
            rounded="lg"
            class="time-select"
        />
      </v-col>
      <v-col cols="12" md="3"  class="ml-auto">
        <v-btn
            prepend-icon="mdi-plus"
            color="grey-darken-4"
            rounded="xl"
            size="x-large"
            block
            class="btn-clean"
            @click="openNewCaseModal"
          >
            New Check</v-btn
          >
      </v-col>
    </v-row>
  </v-card>
  <v-card class="filters-card">
    <v-card-text style="padding: 0 !important;">
      <v-row dense align-items="center">
        <v-col cols="12" md="6">
          <v-text-field
            label="Search cases, clients, ..."
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
  <v-card class="card-layout">
    <v-card-text class="h-100" style="padding: 0 !important;">
      <CaseDataTable></CaseDataTable>
    </v-card-text>
  </v-card>
  <v-dialog v-model="isCaseModalOpen" class="dialog-90" fullscreen hide-overlay>
    <CaseModal />
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CaseModal from '@/components/CaseModal.vue'
import CaseDataTable from '@/components/CaseDataTable.vue'

const search = ref('')
const selectedStatuses = ref(null)
const selectedCaseTypes = ref(null)
const selectTimeFilter = ref(null)
const isCaseModalOpen = ref(false)

function openNewCaseModal() {
  console.log('New Case button clicked - open modal!')

  isCaseModalOpen.value = true
}

// TODO: demo data to be removed
const statuses = ['Open', 'In Progress', 'Closed']
const caseTypes = ['Personal Injury', 'Property', 'Contract']
const timeFilters = ['Today', 'This Week', 'This Month', 'Past Year', 'All Time']
</script>
