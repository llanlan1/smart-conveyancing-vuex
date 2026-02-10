<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :title="caseDetail.reference"
          title-icon="link"
          :title-link="`#${caseDetail.reference}`"
          :subtitle="systemReference"
          :buttons="buttons"
        />

        <!-- Case Type row -->
        <v-row dense class="mt-6 align-end">
          <v-col md="3" class="d-flex align-center pb-0">
            <v-label class="dialog-card-text-fields-label mb-2">Case Type</v-label>
          </v-col>
          <v-col md="3" class="d-flex align-center pb-0">
            <v-label class="dialog-card-text-fields-label">Phone</v-label>
            <span class="text-caption ml-auto mr-1">Client</span>
            <v-checkbox v-model="clientFlags.phone" hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
          </v-col>
          <v-col md="5" class="d-flex align-center pb-0">
            <v-label class="dialog-card-text-fields-label">Email Address</v-label>
            <span class="text-caption ml-auto mr-1">Client</span>
            <v-checkbox v-model="clientFlags.email" hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
          </v-col>
        </v-row>

        <v-row dense class="mt-1">
          <v-col md="3">
            <v-select
              v-model="form.caseType"
              :items="caseTypeOptions"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
            ></v-select>
          </v-col>
          <v-col md="3">
            <v-text-field
              v-model="form.phone"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
              placeholder="87654321"
            ></v-text-field>
          </v-col>
          <v-col md="5">
            <v-text-field
              v-model="form.email"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
              placeholder="tan_alice@gmail.com"
            ></v-text-field>
          </v-col>
        </v-row>

        <!-- Team fields -->
        <TeamFields v-model="teamData" />

        <!-- Document viewer -->
        <v-row dense class="mb-2 flex-grow-1">
          <v-col cols="12">
            <DocumentViewer v-model="documents" />
          </v-col>
        </v-row>
      </v-col>

      <!-- Right Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <div class="right-side-non-card-content mt-6">
          <RoleSelector
            v-model:role="form.role"
            v-model:type="form.roleType"
          />
        </div>

        <div class="right-content-scrollable flex-grow-1">
          <PropertyFields
            v-model="propertyData"
            :show-copy-icons="true"
            :show-ethnic-quota="true"
            :identity-check-disabled="!hasOtpUploaded"
            submit-label="Next"
            @submit="handleNext"
          />
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { ButtonConfig } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeader.vue'
import TeamFields from '@/components/dialog-sections/TeamFields.vue'
import DocumentViewer from '@/components/dialog-sections/DocumentViewer.vue'
import RoleSelector from '@/components/dialog-sections/RoleSelector.vue'
import PropertyFields from '@/components/dialog-sections/PropertyFields.vue'

interface Document {
  name: string
  type: string
  previewUrl?: string
}

interface CaseDetail {
  reference: string
  systemReference: string
  caseType: string
}

const route = useRoute()

const emit = defineEmits<{
  (e: 'next'): void
}>()

const caseId = computed(() => route.params.id as string)

const caseDetail = ref<CaseDetail>({
  reference: '',
  systemReference: '',
  caseType: ''
})

const buttons: ButtonConfig[] = [
  { label: 'Save Draft', icon: 'mdi-content-save', color: 'white' }
]

const systemReference = computed(() => caseDetail.value.systemReference || 'SOW-1-2026')

onMounted(() => {
  // TODO: fetch case data from API using caseId
  caseDetail.value = {
    reference: caseId.value || 'HS(JL).65431',
    systemReference: 'SOW-1-2026',
    caseType: 'Sales'
  }
})

// TODO: demo data to be removed
const caseTypeOptions = ['Purchase', 'Sales', 'Commercial']

const form = reactive({
  caseType: '',
  phone: '',
  email: '',
  role: 'Client',
  roleType: 'individual' as 'individual' | 'corporate'
})

const clientFlags = reactive({
  phone: false,
  email: false
})

const teamData = reactive({
  bdm: '',
  lawyerIc: '',
  secretaryIc: ''
})

const propertyData = reactive({
  propertyType: '',
  checkEthnicQuota: false,
  postcode: '',
  floor: '',
  unit: '',
  block: '',
  street: '',
  buildingName: '',
  propertyPrice: '',
  optionDate: '',
  optionExpiry: '',
  completionDate: '',
  weeksUponExercising: ''
})

const documents = ref<Document[]>([])

const hasOtpUploaded = computed(() => {
  return documents.value.some(doc => doc.type === 'OTP')
})

function handleNext() {
  emit('next')
}
</script>

<style scoped>
.right-content-scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 0.9rem;
}

.right-side-non-card-content {
  padding: 0.9rem 0 0 0.9rem;
}

.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}
</style>
