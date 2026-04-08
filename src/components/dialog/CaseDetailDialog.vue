<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :title="caseDetail.caseRefNum"
          title-icon="edit"
          :subtitle="sysGenRefNum"
          :buttons="buttons"
          @update:title="handleCaseRefNumUpdate"
        />

        <!-- Case Type / Client Contact -->
        <CaseTypeClientContactFields
          v-model:case-type="form.caseType"
          v-model:phone="form.phone"
          v-model:email="form.email"
          v-model:phone-client="clientFlags.phone"
          v-model:email-client="clientFlags.email"
          :case-type-options="caseTypeOptions"
          email-placeholder="tan_alice@gmail.com"
        />

        <!-- Team fields -->
        <TeamFields v-model="teamData" />

        <!-- Document viewer -->
        <v-row dense class="mb-2 flex-grow-1">
          <v-col cols="12">
            <DocumentUploadArea v-model="documents" @fields-parsed="handleFieldsParsed" />
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
import type { ButtonConfig, Document, CaseDetail, ParsedFields } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeaderFields.vue'
import CaseTypeClientContactFields from '@/components/dialog-sections/CaseTypeClientContactFields.vue'
import TeamFields from '@/components/dialog-sections/TeamFields.vue'
import DocumentUploadArea from '@/components/dialog-sections/DocumentUploadArea.vue'
import RoleSelector from '@/components/dialog-sections/IndividualCommercialToggle.vue'
import FormFieldsSectionRight, { type FormFieldConfig } from '@/components/dialog-sections/RightSideFields.vue'

const route = useRoute()

const emit = defineEmits<{
  (e: 'next'): void
}>()

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

onMounted(() => {
  // TODO: fetch case data from API using caseId
  caseDetail.value = {
    caseRefNum: caseId.value || 'HS(HL).65431',
    sysGenRefNum: 'SOW-1-2026',
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

const propertyData = reactive<Record<string, string>>({})

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

function handleFieldsParsed({ detectedType, fields }: { index: number; detectedType: string; fields: ParsedFields }) {
  if (detectedType === 'WhatsApp Screenshot') {
    if (fields.phone) form.phone = fields.phone
    if (fields.email) form.email = fields.email
    return
  }

  if (detectedType === 'OTP') {
    if (fields.postcode) propertyData.postcode = fields.postcode
    if (fields.floor) propertyData.floor = fields.floor
    if (fields.unit) propertyData.unit = fields.unit
    if (fields.block) propertyData.block = fields.block
    if (fields.street) propertyData.street = fields.street
    if (fields.buildingName) propertyData.buildingName = fields.buildingName
    if (fields.propertyPrice) propertyData.propertyPrice = fields.propertyPrice
    if (fields.optionDate) propertyData.optionDate = fields.optionDate
    if (fields.optionExpiry) propertyData.optionExpiry = fields.optionExpiry
    if (fields.completionDate) propertyData.completionDate = fields.completionDate
    if (fields.weeksUponExercising) propertyData.weeksUponExercising = fields.weeksUponExercising
  }
}

function handleNext() {
  emit('next')
}

function handleCaseRefNumUpdate(newTitle: string) {
  caseDetail.value.caseRefNum = newTitle
  // TODO: save to API
}
</script>

<style scoped lang="scss">
.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}
</style>
