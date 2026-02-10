<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :title="caseDetail.systemReference"
        />

        <CaseHeaderInfo
          :reference-number="caseDetail.reference"
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
            <v-text-field
              v-model="form.remarks"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
              placeholder="Value"
            ></v-text-field>
          </v-col>
        </v-row>

        <!-- Upload ID button -->
        <v-row dense class="mt-4">
          <v-col md="5">
            <v-btn
              block
              rounded="xl"
              color="grey-darken-3"
              class="text-none"
              prepend-icon="mdi-upload"
            >
              Upload ID
            </v-btn>
          </v-col>
          <v-col md="5">
            <v-btn
              block
              rounded="xl"
              variant="outlined"
              class="text-none"
            >
              Go to AML Website
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
          <!-- Client info section -->
          <div class="client-section rounded-xl pt-6 px-6 d-flex flex-column">
            <v-row dense>
              <v-col md="4">
                <v-label class="dialog-card-text-fields-label mb-1">Role</v-label>
                <v-select
                  v-model="form.role"
                  :items="roleOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
              <v-col md="4">
                <v-label class="dialog-card-text-fields-label mb-1">Marital Status</v-label>
                <v-select
                  v-model="form.maritalStatus"
                  :items="maritalStatusOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
              <v-col md="4">
                <v-label class="dialog-card-text-fields-label mb-1">ID Type</v-label>
                <v-select
                  v-model="form.idType"
                  :items="idTypeOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <div class="d-flex align-center mb-1">
                  <v-label class="dialog-card-text-fields-label">Name on ID</v-label>
                  <v-btn icon variant="text" size="x-small" class="ml-1">
                    <v-icon size="14">mdi-content-copy</v-icon>
                  </v-btn>
                </div>
                <v-text-field
                  v-model="form.nameOnId"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  :disabled="!hasIdUploaded"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <div class="d-flex align-center mb-1">
                  <v-label class="dialog-card-text-fields-label">ID No.</v-label>
                  <v-btn icon variant="text" size="x-small" class="ml-1">
                    <v-icon size="14">mdi-content-copy</v-icon>
                  </v-btn>
                </div>
                <v-text-field
                  v-model="form.idNo"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  :disabled="!hasIdUploaded"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <div class="d-flex align-center mb-1">
                  <v-label class="dialog-card-text-fields-label">Asian Characters on ID</v-label>
                  <v-btn icon variant="text" size="x-small" class="ml-1">
                    <v-icon size="14">mdi-content-copy</v-icon>
                  </v-btn>
                </div>
                <v-text-field
                  v-model="form.asianChars"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  :disabled="!hasIdUploaded"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <div class="d-flex align-center mb-1">
                  <v-label class="dialog-card-text-fields-label">Date of Birth</v-label>
                  <v-btn icon variant="text" size="x-small" class="ml-1">
                    <v-icon size="14">mdi-content-copy</v-icon>
                  </v-btn>
                </div>
                <v-text-field
                  v-model="form.dateOfBirth"
                  type="date"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  :disabled="!hasIdUploaded"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Citizenship</v-label>
                <v-select
                  v-model="form.citizenship"
                  :items="countryOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Residence / Jurisdiction</v-label>
                <v-select
                  v-model="form.residence"
                  :items="countryOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <!-- Additional Person section -->
            <v-divider class="my-4"></v-divider>

            <v-row dense>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Additional Person</v-label>
                <v-select
                  v-model="form.additionalPerson"
                  :items="additionalPersonOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">ID Type</v-label>
                <v-select
                  v-model="form.additionalIdType"
                  :items="idTypeOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-divider class="mx-n6 mt-auto"></v-divider>
            <div class="submit-area">
              <span class="submit-btn" @click="handleSubmit">Submit and Close</span>
            </div>
          </div>

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
import DialogHeader from '@/components/dialog-sections/DialogHeader.vue'
import CaseHeaderInfo from '@/components/dialog-sections/CaseHeaderInfo.vue'
import DocumentViewer from '@/components/dialog-sections/DocumentViewer.vue'
import type { Document, CaseDetail } from '@/common/types'

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
  role: 'Main Client',
  maritalStatus: 'Unknown',
  idType: 'IC',
  nameOnId: '',
  idNo: '',
  asianChars: '',
  dateOfBirth: '',
  citizenship: 'Singapore',
  residence: 'Singapore',
  additionalPerson: '',
  additionalIdType: 'IC'
})

const documents = ref<Document[]>([])

// TODO: demo data to be removed
const roleOptions = ['Main Client', 'Client', 'Nominee', 'POA - Donee', 'Trustee', 'Executor']
const maritalStatusOptions = ['Unknown', 'Single', 'Married', 'Divorced', 'Widowed']
const idTypeOptions = ['IC', 'Passport', 'FIN', 'Birth Certificate']
const countryOptions = ['Singapore', 'Malaysia', 'Indonesia', 'China', 'India']
const additionalPersonOptions = ['Select', 'None', 'Client', 'Nominee', 'POA - Donee', 'Trustee', 'Executor']

const hasIdUploaded = computed(() => {
  return documents.value.some(doc => doc.type === 'IC')
})

const canUploadAml = computed(() => hasIdUploaded.value)

onMounted(() => {
  // TODO: fetch case data from API using caseId
  caseDetail.value = {
    reference: caseId.value || 'HS(JL).65431',
    systemReference: 'SOW-1-2026',
    address: '123 ABCDE Ave 3 #01-02 123456',
    caseType: 'Sales HDB Flat',
    client: 'Alice Tan'
  }
})

function handleSubmit() {
  console.log('Client form submitted:', form)
}
</script>

<style scoped>
.client-section {
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.right-content-scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 0.9rem;
}

.submit-area {
  flex-shrink: 0;
  height: 60px;
  line-height: 60px;
  text-align: center;
}

.submit-btn {
  color: #9e9e9e;
  letter-spacing: 0.5px;
  font-weight: 400;
  font-size: 14px;
  cursor: pointer;
}

.submit-btn:hover {
  color: #616161;
}

.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}
</style>
