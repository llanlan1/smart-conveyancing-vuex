<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :title="caseDetail.reference"
          title-icon="edit"
          :subtitle="systemReference"
          :buttons="buttons"
          @update:title="handleTitleUpdate"
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
          <FormFieldsSectionRight
            :fields="propertyFields"
            v-model="propertyData"
            submit-label="Next"
            @submit="handleNext"
          >
            <v-row dense class="mt-3 mb-4">
              <v-col cols="12">
                <v-btn
                  block
                  rounded="xl"
                  color="grey-darken-3"
                  class="text-none"
                  style="letter-spacing: 0.4px"
                  height="45px"
                  :disabled="!hasOtpUploaded"
                >
                  Go to Identity Check
                </v-btn>
              </v-col>
            </v-row>
          </FormFieldsSectionRight>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { ButtonConfig, Document, CaseDetail } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeaderFields.vue'
import TeamFields from '@/components/dialog-sections/TeamFields.vue'
import DocumentViewer from '@/components/dialog-sections/UploadViewDocument.vue'
import RoleSelector from '@/components/dialog-sections/IndividualCommercialToggle.vue'
import FormFieldsSectionRight, { type FormFieldConfig } from '@/components/dialog-sections/RightSideFields.vue'

const route = useRoute()

const emit = defineEmits<{
  (e: 'next'): void
}>()

const caseId = computed(() => route.params.id as string)

const caseDetail = ref<CaseDetail>({
  reference: '',
  systemReference: '',
  address: '',
  caseType: '',
  client: ''
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
    address: '123 ABCDE Ave 3 #01-02 123456',
    caseType: 'Sales',
    client: 'Alice Tan'
  }
})

// TODO: demo data to be removed
const caseTypeOptions = ['Purchase', 'Sales', 'Commercial']

const form = reactive({
  caseType: '',
  phone: '',
  email: '',
  role: 'Client',
  roleType: 'individual' as 'individual' | 'commercial'
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

const propertyData = reactive({})

// TODO: demo data to be removed
const propertyTypeOptions = ['HDB Resale', 'Private', 'Commercial']

const propertyFields: FormFieldConfig[] = [
  { type: 'select', label: 'Property Type', model: 'propertyType', md: 5, items: propertyTypeOptions },
  { type: 'checkbox', label: 'Check Ethnic Quota', model: 'checkEthnicQuota', md: 7 },
  { type: 'text', label: 'Postcode', model: 'postcode', md: 4, copyable: true },
  { type: 'text', label: 'Floor', model: 'floor', md: 2, copyable: true },
  { type: 'text', label: 'Unit', model: 'unit', md: 2, copyable: true },
  { type: 'text', label: 'Block', model: 'block', md: 3, copyable: true },
  { type: 'text', label: 'Street', model: 'street', md: 6, copyable: true },
  { type: 'text', label: 'Building Name', model: 'buildingName', md: 5 },
  { type: 'text', label: 'Property Price', model: 'propertyPrice', md: 3 },
  { type: 'date', label: 'Option Date', model: 'optionDate', md: 4 },
  { type: 'date', label: 'Option Expiry', model: 'optionExpiry', md: 4 },
  { type: 'date', label: 'Completion Date', model: 'completionDate', md: 4 },
  { type: 'text', label: 'No. of Weeks upon exercising', model: 'weeksUponExercising', md: 2 },
]

const documents = ref<Document[]>([])

const hasOtpUploaded = computed(() => {
  return documents.value.some(doc => doc.type === 'OTP')
})

function handleNext() {
  emit('next')
}

function handleTitleUpdate(newTitle: string) {
  caseDetail.value.reference = newTitle
  // TODO: save to API
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
