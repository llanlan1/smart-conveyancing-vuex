<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :title="caseDetail.reference"
          title-icon="edit"
          :buttons="shortfallButtons"
        />

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
          <!-- SOW/SOF fields -->
          <div class="shortfall-section rounded-xl pt-6 px-6 d-flex flex-column">
            <v-row dense>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Property Price</v-label>
                <v-text-field
                  v-model="form.propertyPrice"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  placeholder="SGD"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Occupation</v-label>
                <v-text-field
                  v-model="form.occupation"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Approved Amount</v-label>
                <v-text-field
                  v-model="form.approvedAmount"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  placeholder="SGD"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Type</v-label>
                <v-select
                  v-model="form.approvedType"
                  :items="approvedTypeOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Grant Amount</v-label>
                <v-text-field
                  v-model="form.grantAmount"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  placeholder="SGD"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Type</v-label>
                <v-select
                  v-model="form.grantType"
                  :items="grantTypeOptions"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Bank Balance</v-label>
                <v-text-field
                  v-model="form.bankBalance"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  placeholder="SGD"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Type</v-label>
                <v-select
                  v-model="form.bankType"
                  :items="['Bank Statement']"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-row dense class="mt-2">
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Annual Income - Y1</v-label>
                <v-text-field
                  v-model="form.annualIncomeY1"
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  placeholder="SGD"
                ></v-text-field>
              </v-col>
              <v-col md="6">
                <v-label class="dialog-card-text-fields-label mb-1">Type</v-label>
                <v-select
                  v-model="form.incomeTypeY1"
                  :items="incomeTypeOptions"
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
import type { Document, CaseDetail, ButtonConfig } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeader.vue'
import CaseHeaderInfo from '@/components/dialog-sections/CaseHeaderInfo.vue'
import DocumentViewer from '@/components/dialog-sections/DocumentViewer.vue'


const route = useRoute()


const caseId = computed(() => route.params.id as string)

const caseDetail = ref<CaseDetail>({
  reference: '',
  systemReference: '',
  address: '',
  caseType: '',
  client: ''
})

const shortfallButtons: ButtonConfig[] = [
  { label: 'Print AML', icon: 'mdi-printer', color: 'white' },
  { label: 'Save Draft', icon: 'mdi-content-save', color: 'white' }
]

const form = reactive({
  remarks: '',
  propertyPrice: '',
  occupation: '',
  approvedAmount: '',
  approvedType: 'Loan Approved',
  grantAmount: '',
  grantType: 'HDB Grant',
  bankBalance: '',
  bankType: 'Bank Statement',
  annualIncomeY1: '',
  incomeTypeY1: 'NOA - Past 1 Year'
})

const documents = ref<Document[]>([])

// TODO: demo data to be removed
const approvedTypeOptions = ['Loan Approved', 'CPF Approved']
const grantTypeOptions = ['HDB Grant', 'CPF Grant']
const incomeTypeOptions = ['NOA - Past 1 Year', 'NOA - Past 2 Years', 'NOA - Past 3 Years']

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
.shortfall-section {
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
