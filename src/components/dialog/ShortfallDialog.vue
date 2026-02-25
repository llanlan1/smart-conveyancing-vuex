<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <v-row dense align="center" justify="space-between">
          <v-col>
            <DialogHeader
              :reference-number="caseDetail.reference"
              :address="caseDetail.address"
              :case-type="caseDetail.caseType"
            />
          </v-col>
          <v-col cols="auto">
            <v-btn
              color="white"
              rounded="lg"
              class="text-none header-btn"
              prepend-icon="mdi-content-save"
            >
              Save Draft
            </v-btn>
          </v-col>
        </v-row>

        <CaseHeaderInfo
          ref-label="Client"
          :reference-number="caseDetail.client"
          :address="caseDetail.address"
          :case-type="caseDetail.caseType"
        />

        <!-- Remarks -->
        <v-row dense class="mt-4">
          <v-col cols="12">
            <v-label class="dialog-card-text-fields-label">
              Remarks
              <v-icon size="14" class="ml-1">mdi-pencil</v-icon>
            </v-label>
            <v-textarea
              v-model="form.remarks"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
              rows="3"
            ></v-textarea>
          </v-col>
        </v-row>

        <!-- Upload button -->
        <v-row dense class="mt-4">
          <v-col cols="12">
            <v-btn
              block
              rounded="xl"
              color="grey-darken-3"
              class="text-none"
            >
              Upload All SOW / SOF Documents
            </v-btn>
          </v-col>
        </v-row>

        <!-- Document viewer -->
        <v-row dense class="mt-4 flex-grow-1">
          <v-col cols="12">
            <DocumentViewer v-model="documents" />
          </v-col>
        </v-row>
      </v-col>

      <!-- Right Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <div class="right-content-scrollable flex-grow-1 mt-6">
          <FormFieldsSection
            :fields="shortfallFields"
            v-model="shortfallData"
            submit-label="Submit and Close"
            @submit="handleSubmit"
          />

          <!-- Calculate button -->
          <v-btn
            block
            rounded="xl"
            color="grey-darken-3"
            class="text-none mt-4"
            height="45px"
            @click="handleCalculate"
          >
            Calculate and Analyse
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Document, CaseDetail } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/ReadOnlyDialogHeader.vue'
import CaseHeaderInfo from '@/components/dialog-sections/DialogHeaderFields.vue'
import DocumentViewer from '@/components/dialog-sections/UploadViewDocument.vue'
import FormFieldsSection, { type FormFieldConfig } from '@/components/dialog-sections/RightSideFields.vue'


const route = useRoute()


const caseId = computed(() => route.params.id as string)

const caseDetail = ref<CaseDetail>({
  reference: '',
  systemReference: '',
  address: '',
  caseType: '',
  client: ''
})


const form = reactive({
  remarks: '',
})

const shortfallData = reactive({})

const documents = ref<Document[]>([])

// TODO: demo data to be removed
const approvedTypeOptions = ['Loan Approved', 'CPF Approved']
const grantTypeOptions = ['HDB Grant', 'CPF Grant']
const incomeTypeOptions = ['NOA - Past 1 Year', 'NOA - Past 2 Years', 'NOA - Past 3 Years']

const shortfallFields: FormFieldConfig[] = [
  { type: 'text', label: 'Property Price', model: 'propertyPrice', md: 6, placeholder: 'SGD' },
  { type: 'text', label: 'Occupation', model: 'occupation', md: 6 },
  { type: 'text', label: 'Approved Amount', model: 'approvedAmount', md: 6, placeholder: 'SGD' },
  { type: 'select', label: 'Type', model: 'approvedType', md: 6, items: approvedTypeOptions, defaultValue: 'Loan Approved' },
  { type: 'text', label: 'Grant Amount', model: 'grantAmount', md: 6, placeholder: 'SGD' },
  { type: 'select', label: 'Type', model: 'grantType', md: 6, items: grantTypeOptions, defaultValue: 'HDB Grant' },
  { type: 'text', label: 'Bank Balance', model: 'bankBalance', md: 6, placeholder: 'SGD' },
  { type: 'select', label: 'Type', model: 'bankType', md: 6, items: ['Bank Statement'], defaultValue: 'Bank Statement' },
  { type: 'text', label: 'Annual Income - Y1', model: 'annualIncomeY1', md: 6, placeholder: 'SGD' },
  { type: 'select', label: 'Type', model: 'incomeTypeY1', md: 6, items: incomeTypeOptions, defaultValue: 'NOA - Past 1 Year' },
]

onMounted(() => {
  // TODO: fetch case data from API using caseId
  caseDetail.value = {
    reference: caseId.value || 'HS(JL).65431',
    systemReference: 'SOW-1-2026',
    address: '123 ABCDE Ave 3 #01-02 123456',
    caseType: 'Sales HDB Flat',
    client: 'Wong Xi An Sandy\nJorriah Ang Li Weng'
  }
})

function handleSubmit() {
  console.log('Shortfall form submitted:', form)
}

function handleCalculate() {
  console.log('Calculate and analyse:', form)
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

.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}
</style>
