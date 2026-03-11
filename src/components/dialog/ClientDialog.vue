<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :subtitle="sysGenRefNum"
          :buttons="buttons"
        />

        <CaseInfoLeftCopy
          :reference-number="caseDetail.caseRefNum"
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

        <!-- Upload ID / AML buttons -->
        <v-row dense class="mt-4">
          <v-col cols="12">
            <div class="action-btn-group">
              <v-btn
                rounded="xl"
                color="grey-darken-3"
                class="text-none"
                append-icon="mdi-information-outline"
              >
                Upload ID
              </v-btn>
              <v-btn
                rounded="xl"
                variant="outlined"
                class="text-none"
              >
                Go to AML Website
              </v-btn>
            </div>
          </v-col>
        </v-row>

        <!-- Document viewer -->
        <v-row dense class="mt-4 flex-grow-1" align="stretch">
          <v-col cols="12">
            <DocumentUploadArea v-model="documents" />
          </v-col>
        </v-row>
      </v-col>

      <!-- Right Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <div class="right-content-scrollable flex-grow-1 mt-6">
          <FormFieldsSection
            :fields="clientFields"
            v-model="clientData"
            submit-label="Submit and Close"
            @submit="handleSubmit"
          />

          <!-- Upload AML Document button -->
          <v-btn
            block
            rounded="xl"
            color="grey-darken-3"
            class="text-none mt-4"
            height="45px"
            :disabled="!canUploadAml"
          >
            Upload AML Document
          </v-btn>
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
import CaseInfoLeftCopy from '@/components/dialog-sections/ReadOnlyDialogHeader.vue'
import DocumentUploadArea from '@/components/dialog-sections/DocumentUploadArea.vue'
import FormFieldsSection, { type FormFieldConfig } from '@/components/dialog-sections/RightSideFields.vue'

const route = useRoute()


const caseId = computed(() => route.params.id as string)

const caseDetail = ref<CaseDetail>({
  caseRefNum: '',
  sysGenRefNum: '',
  address: '',
  caseType: '',
  client: ''
})

const buttons: ButtonConfig[] = [
  { label: 'Save Draft', icon: 'mdi-content-save', color: 'white' }
]

const sysGenRefNum = computed(() => caseDetail.value.sysGenRefNum || 'SOW-1-2026')

const form = reactive({
  remarks: '',
})

const clientData = reactive({})

const documents = ref<Document[]>([])

// TODO: demo data to be removed
const roleOptions = ['Main Client', 'Client', 'Nominee', 'POA - Donee', 'Trustee', 'Executor']
const maritalStatusOptions = ['Unknown', 'Single', 'Married', 'Divorced', 'Widowed']
const idTypeOptions = ['IC', 'Passport', 'FIN', 'Birth Certificate']
const countryOptions = ['Singapore', 'Malaysia', 'Indonesia', 'China', 'India']
const additionalPersonOptions = ['Select', 'None', 'Client', 'Nominee', 'POA - Donee', 'Trustee', 'Executor']

const clientFields = computed<FormFieldConfig[]>(() => [
  { type: 'select', label: 'Role', model: 'role', md: 4, items: roleOptions, defaultValue: 'Main Client' },
  { type: 'select', label: 'Marital Status', model: 'maritalStatus', md: 4, items: maritalStatusOptions, defaultValue: 'Unknown' },
  { type: 'select', label: 'ID Type', model: 'idType', md: 4, items: idTypeOptions, defaultValue: 'IC' },
  { type: 'text', label: 'Name on ID', model: 'nameOnId', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'text', label: 'ID No.', model: 'idNo', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'text', label: 'Asian Characters on ID', model: 'asianChars', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'date', label: 'Date of Birth', model: 'dateOfBirth', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'select', label: 'Citizenship', model: 'citizenship', md: 6, items: countryOptions, defaultValue: 'Singapore' },
  { type: 'select', label: 'Residence / Jurisdiction', model: 'residence', md: 6, items: countryOptions, defaultValue: 'Singapore' },
  { type: 'divider' },
  { type: 'select', label: 'Additional Person', model: 'additionalPerson', md: 6, items: additionalPersonOptions },
  { type: 'select', label: 'ID Type', model: 'additionalIdType', md: 6, items: idTypeOptions, defaultValue: 'IC' },
])

const hasIdUploaded = computed(() => {
  return documents.value.some(doc => doc.type === 'IC')
})

const canUploadAml = computed(() => hasIdUploaded.value)

onMounted(() => {
  // TODO: fetch case data from API using caseId
  caseDetail.value = {
    caseRefNum: caseId.value || 'HS(JL).65431',
    sysGenRefNum: 'SOW-1-2026',
    address: '123 ABCDE Ave 3 #01-02 123456',
    caseType: 'Sales HDB Flat',
    client: 'Alice Tan'
  }
})

function handleSubmit() {
  console.log('Client form submitted:', form)
}
</script>

<style scoped lang="scss">
.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}

:deep(.header-subtitle) {
  font-size: 24px;
  letter-spacing: 1.2px;
}

:deep(.case-header-info .v-row) {
  align-items: flex-start !important;
}

.flex-grow-1 :deep(.v-col) {
  height: 100%;
}

.action-btn-group :deep(.v-btn) {
  flex: 1;
}

.action-btn-group :deep(.v-btn:first-child) {
  border-top-right-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
}

.action-btn-group :deep(.v-btn:last-child) {
  border-top-left-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
}
</style>
