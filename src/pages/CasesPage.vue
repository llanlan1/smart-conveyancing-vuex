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
      <v-col cols="12" md="3" class="ml-auto">
        <v-btn
          prepend-icon="mdi-plus"
          color="grey-darken-4"
          rounded="xl"
          size="x-large"
          block
          class="btn-clean"
          @click="openNewCase"
        >
          New Check</v-btn
        >
      </v-col>
    </v-row>
  </v-card>
  <v-card class="filters-card">
    <v-card-text style="padding: 0 !important">
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
  <v-card class="card-layout card-content-height">
    <v-card-text style="padding: 0 !important">
      <CaseDataTable @open-case="handleOpenCase"></CaseDataTable>
    </v-card-text>
  </v-card>

  <!-- Dialog container for child routes -->
  <v-dialog v-model="isDialogOpen" class="dialog-90" @dragover.prevent @drop.prevent>
    <v-btn
      icon
      variant="text"
      size="small"
      class="dialog-close-btn"
      @click="closeDialog"
    >
      <v-icon>mdi-close</v-icon>
    </v-btn>
    <router-view />
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CaseDataTable from '@/components/CaseDataTable.vue'
import type { CaseData } from '@/common/types'

const route = useRoute()
const router = useRouter()

const search = ref('')
const selectedStatuses = ref(null)
const selectedCaseTypes = ref(null)
const selectTimeFilter = ref(null)

const caseDetailColumns = ['reference', 'address', 'caseType', 'roles']

const isDialogOpen = computed({
  get: () => route.matched.length > 1,
  set: (value) => {
    if (!value) closeDialog()
  }
})

function openNewCase() {
  router.push({ name: 'NewCase' })
}

function handleOpenCase(caseData: CaseData, column: string) {
  const caseId = caseData.systemReference || caseData.reference

  if (caseDetailColumns.includes(column)) {
    router.push({ name: 'CaseDetail', params: { id: caseId } })
  } else if (column === 'client') {
    router.push({ name: 'CaseClient', params: { id: caseId } })
  } else if (column === 'shortfall') {
    router.push({ name: 'CaseShortfall', params: { id: caseId } })
  }
}

function closeDialog() {
  router.push({ name: 'Cases' })
}

// TODO: demo data to be removed
const statuses = ['Open', 'In Progress', 'Closed']
const caseTypes = ['Purchase', 'Sub-Purchase', 'Commercial', 'Sales']
const timeFilters = ['Today', 'This Week', 'This Month', 'Past Year', 'All Time']
</script>
