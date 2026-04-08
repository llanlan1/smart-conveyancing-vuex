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
            <DocumentUploadArea
              v-model="documents"
              @fields-parsed="handleFieldsParsed"
            />
          </v-col>
        </v-row>
      </v-col>

      <!-- Right Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <div class="right-content-scrollable flex-grow-1 mt-6">
          <FormFieldsSection
            :fields="mainClientFields"
            v-model="clientData"
            submit-label="Submit and Close"
            @submit="handleSubmit"
          >
            <!-- Dynamic additional person sections -->
            <template v-for="(person, i) in additionalPersons" :key="person._key">
              <v-divider class="my-4" />
              <div class="text-body-2 font-weight-medium mb-3 px-1">
                Additional Person {{ i + 1 }}
              </div>
              <v-row dense>
                <v-col md="4" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Role</v-label>
                  <v-select v-model="person.role" :items="roleOptions" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="4" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Marital Status</v-label>
                  <v-select v-model="person.maritalStatus" :items="maritalStatusOptions" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="4" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">ID Type</v-label>
                  <v-select v-model="person.idType" :items="idTypeOptions" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Name on ID</v-label>
                  <v-text-field v-model="person.nameOnId" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">ID No.</v-label>
                  <v-text-field v-model="person.idNo" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Asian Characters on ID</v-label>
                  <v-text-field v-model="person.asianChars" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Date of Birth</v-label>
                  <v-text-field v-model="person.dateOfBirth" type="date" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Citizenship</v-label>
                  <v-select v-model="person.citizenship" :items="countryOptions" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
                <v-col md="6" class="mb-2">
                  <v-label class="dialog-card-text-fields-label">Residence / Jurisdiction</v-label>
                  <v-select v-model="person.residence" :items="countryOptions" variant="outlined" rounded="lg" density="compact" hide-details />
                </v-col>
              </v-row>
            </template>
          </FormFieldsSection>

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
import type { ButtonConfig, Document, CaseDetail, ParsedFields } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeaderFields.vue'
import CaseInfoLeftCopy from '@/components/dialog-sections/ReadOnlyDialogHeader.vue'
import DocumentUploadArea from '@/components/dialog-sections/DocumentUploadArea.vue'
import FormFieldsSection, { type FormFieldConfig } from '@/components/dialog-sections/RightSideFields.vue'

const route = useRoute()

const emit = defineEmits<{
  (e: 'fields-parsed', payload: { detectedType: string; fields: ParsedFields }): void
}>()

interface AdditionalPerson {
  _key: string
  idNo: string
  role: string
  maritalStatus: string
  idType: string
  nameOnId: string
  asianChars: string
  dateOfBirth: string
  citizenship: string
  residence: string
}

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

const clientData = reactive<Record<string, unknown>>({})
const documents = ref<Document[]>([])
const additionalPersons = ref<AdditionalPerson[]>([])

// TODO: demo data to be removed
const roleOptions = ['Main Client', 'Client', 'Nominee', 'POA - Donee', 'Trustee', 'Executor']
const maritalStatusOptions = ['Unknown', 'Single', 'Married', 'Divorced', 'Widowed']
const idTypeOptions = ['IC', 'Passport', 'FIN', 'Birth Certificate']
const countryOptions = ['Singapore', 'Malaysia', 'Indonesia', 'China', 'India']

const IC_TYPES = new Set(['IC—Front', 'IC—Back', 'IC—Both Sides', 'Passport'])

const hasIdUploaded = computed(() => {
  return documents.value.some(doc => IC_TYPES.has(doc.type))
})

const canUploadAml = computed(() => hasIdUploaded.value)

const mainClientFields = computed<FormFieldConfig[]>(() => [
  { type: 'select', label: 'Role', model: 'role', md: 4, items: roleOptions, defaultValue: 'Main Client' },
  { type: 'select', label: 'Marital Status', model: 'maritalStatus', md: 4, items: maritalStatusOptions, defaultValue: 'Unknown' },
  { type: 'select', label: 'ID Type', model: 'idType', md: 4, items: idTypeOptions, defaultValue: 'IC' },
  { type: 'text', label: 'Name on ID', model: 'nameOnId', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'text', label: 'ID No.', model: 'idNo', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'text', label: 'Asian Characters on ID', model: 'asianChars', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'date', label: 'Date of Birth', model: 'dateOfBirth', md: 6, copyable: true, disabled: !hasIdUploaded.value },
  { type: 'select', label: 'Citizenship', model: 'citizenship', md: 6, items: countryOptions, defaultValue: 'Singapore' },
  { type: 'select', label: 'Residence / Jurisdiction', model: 'residence', md: 6, items: countryOptions, defaultValue: 'Singapore' },
])

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

function handleFieldsParsed({ detectedType, fields }: { index: number; detectedType: string; fields: ParsedFields }) {
  if (detectedType === 'WhatsApp Screenshot') {
    emit('fields-parsed', { detectedType, fields })
    return
  }

  if (!IC_TYPES.has(detectedType)) return

  const mainClientEmpty = !clientData.nameOnId && !clientData.idNo
  const incomingId = fields.idNo

  if (mainClientEmpty) {
    populateClientData(clientData, fields, detectedType)
    return
  }

  if (incomingId && clientData.idNo === incomingId) {
    // Same person as main client — merge (fill gaps only)
    mergeClientData(clientData, fields)
    return
  }

  if (incomingId) {
    const existing = additionalPersons.value.find(p => p.idNo === incomingId)
    if (existing) {
      mergePersonFields(existing, fields)
    } else {
      additionalPersons.value.push(buildAdditionalPerson(fields, detectedType))
    }
  } else {
    // No ID number extracted — merge into last additional person or main client
    const last = additionalPersons.value[additionalPersons.value.length - 1]
    if (last) mergePersonFields(last, fields)
  }
}

function populateClientData(target: Record<string, unknown>, fields: ParsedFields, detectedType: string) {
  if (fields.nameOnId) target.nameOnId = fields.nameOnId
  if (fields.idNo) target.idNo = fields.idNo
  if (fields.asianChars) target.asianChars = fields.asianChars
  if (fields.dateOfBirth) target.dateOfBirth = fields.dateOfBirth
  if (fields.citizenship) target.citizenship = fields.citizenship
  if (detectedType === 'Passport') target.idType = 'Passport'
}

function mergeClientData(target: Record<string, unknown>, fields: ParsedFields) {
  if (!target.nameOnId && fields.nameOnId) target.nameOnId = fields.nameOnId
  if (!target.idNo && fields.idNo) target.idNo = fields.idNo
  if (!target.asianChars && fields.asianChars) target.asianChars = fields.asianChars
  if (!target.dateOfBirth && fields.dateOfBirth) target.dateOfBirth = fields.dateOfBirth
  if (!target.citizenship && fields.citizenship) target.citizenship = fields.citizenship
}

function mergePersonFields(person: AdditionalPerson, fields: ParsedFields) {
  if (!person.nameOnId && fields.nameOnId) person.nameOnId = fields.nameOnId
  if (!person.idNo && fields.idNo) person.idNo = fields.idNo
  if (!person.asianChars && fields.asianChars) person.asianChars = fields.asianChars
  if (!person.dateOfBirth && fields.dateOfBirth) person.dateOfBirth = fields.dateOfBirth
  if (!person.citizenship && fields.citizenship) person.citizenship = fields.citizenship
}

function buildAdditionalPerson(fields: ParsedFields, detectedType: string): AdditionalPerson {
  return {
    _key: fields.idNo || `person-${Date.now()}`,
    idNo: fields.idNo || '',
    role: 'Client',
    maritalStatus: 'Unknown',
    idType: detectedType === 'Passport' ? 'Passport' : 'IC',
    nameOnId: fields.nameOnId || '',
    asianChars: fields.asianChars || '',
    dateOfBirth: fields.dateOfBirth || '',
    citizenship: fields.citizenship || 'Singapore',
    residence: 'Singapore',
  }
}

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
