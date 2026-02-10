<template>
  <v-card class="dialog-card-layout pa-4">
    <v-row class="dialog-card-full-height-row">
      <!-- Left Column -->
      <v-col md="6" class="dialog-card-text-half-content">
        <DialogHeader
          :show-input="true"
          input-label="Your Case Reference Number"
          v-model:input-value="form.reference"
          :buttons="buttons"
        />

        <!-- Case Type row labels -->
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

        <!-- Case Type row fields -->
        <v-row dense class="mt-1">
          <v-col md="3">
            <v-select
              v-model="form.caseType"
              :items="caseTypeOptions"
              variant="outlined"
              rounded="lg"
              density="compact"
              hide-details
              placeholder="Select"
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
              placeholder="jane@gmail.com"
            ></v-text-field>
          </v-col>
        </v-row>

        <!-- Team fields -->
        <TeamFields v-model="teamData" />

        <!-- Document drop area -->
        <v-row dense class="mb-2 flex-grow-1">
          <v-col cols="12">
            <div class="document-drop-area d-flex flex-column align-center justify-center rounded-xl">
              <v-icon size="95" color="grey-lighten-1" opacity="55%">mdi-arrow-up-box</v-icon>
              <p class="text-grey mt-4 text-center">
                Start by drag and drop<br />
                OTP, IC, AML, LO, ACRA for biz, and<br />
                other documents
              </p>
            </div>
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
            :disabled="!hasDocuments"
            submit-label="Submit"
            @submit="handleSubmit"
          />
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { ButtonConfig } from '@/common/types'
import DialogHeader from '@/components/dialog-sections/DialogHeader.vue'
import TeamFields from '@/components/dialog-sections/TeamFields.vue'
import RoleSelector from '@/components/dialog-sections/RoleSelector.vue'
import PropertyFields from '@/components/dialog-sections/PropertyFields.vue'

const emit = defineEmits<{
  (e: 'submit', data: typeof form): void
}>()

const buttons: ButtonConfig[] = [
  { label: 'Save Draft', icon: 'mdi-content-save', color: 'white' }
]

// TODO: demo data to be removed
const caseTypeOptions = ['Purchase', 'Sales', 'Commercial']

const form = reactive({
  reference: '',
  caseType: '',
  phone: '',
  email: '',
  role: '',
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

const uploadedDocuments = ref<File[]>([])

const hasDocuments = computed(() => uploadedDocuments.value.length > 0)

function handleSubmit() {
  const payload = {
    ...form,
    team: teamData,
    property: propertyData,
    clientFlags
  }
  console.log('New case submitted:', payload)
  emit('submit', form)
}
</script>

<style scoped>
.document-drop-area {
  background-color: #f5f5f5;
  border: 2px dashed #e0e0e0;
  min-height: 475px;
  height: 100%;
  padding-top: 60px;
}

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
