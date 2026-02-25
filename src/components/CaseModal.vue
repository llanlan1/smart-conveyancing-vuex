<template>
  <v-card class="dialog-card-layout pa-4">
    <div class="dialog-card-layout-reduced-height">
      <v-row class="dialog-card-full-height-row">
        <v-col md="6" class="dialog-card-text-half-content">
          <v-row class="dialog-card-text-title-without-border">
            <v-col md="7">
              <!-- New case: show text field for reference input -->
              <v-label class="dialog-card-text-fields-label mt-2"
                >Your Case Reference Number</v-label
              >
              <v-text-field
                v-if="isNew"
                v-model="newReferenceInput.value"
                variant="outlined"
                density="compact"
                class="reference-input"
                hide-details
                rounded="lg"
              ></v-text-field>
              <!-- Existing case: show reference as title -->
              <v-card-title v-else>{{ modalTitle }}</v-card-title>
            </v-col>
            <!-- TODO: more actions to be added -->
            <v-col
              v-for="(button, index) in buttons"
              :key="index"
              md="4"
              class="d-flex align-center"
              :class="{ 'ml-auto': index === 0 }"
            >
              <v-btn
                :color="button.color"
                rounded="lg"
                block
                :style="{ boxShadow: 'none', border: '1px solid #d8d8d8', letterSpacing: '0.1px' }"
                :prepend-icon="button.icon"
                class="text-none"
              >
                {{ button.label }}
              </v-btn>
            </v-col>
          </v-row>
          <!-- Row 2a: Case Type labels -->
          <v-row dense class="mt-6 align-end">
            <v-col md="3" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label mb-2">Case Type</v-label>
            </v-col>
            <v-col md="3" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label">Phone</v-label>
              <span class="text-caption ml-auto mr-1">Client</span>
              <v-checkbox hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
            </v-col>
            <v-col md="5" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label">Email Address</v-label>
              <span class="text-caption ml-auto mr-1">Client</span>
              <v-checkbox hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
            </v-col>
          </v-row>

          <!-- Row 2b: Case Type fields -->
          <v-row dense class="mt-1">
            <v-col md="3">
              <v-select
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                :items="['Purchase', 'Sales', 'Commercial']"
              ></v-select>
            </v-col>
            <v-col md="3">
              <v-text-field
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                placeholder="87654321"
              ></v-text-field>
            </v-col>
            <v-col md="5">
              <v-text-field
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                placeholder="jane@gmail.com"
              ></v-text-field>
            </v-col>
          </v-row>

          <!-- Row 3a: Team labels -->
          <v-row dense class="mt-1">
            <v-col md="3" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label">BDM</v-label>
              <span class="text-caption mr-1 ml-auto">Save</span>
              <v-checkbox hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
            </v-col>
            <v-col md="4" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label">Lawyer-IC</v-label>
              <span class="text-caption mr-1 ml-auto">Save</span>
              <v-checkbox hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
            </v-col>
            <v-col md="4" class="d-flex align-center pb-0">
              <v-label class="dialog-card-text-fields-label">Secretary-IC</v-label>
              <span class="text-caption mr-1 ml-auto">Save</span>
              <v-checkbox hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
            </v-col>
          </v-row>

          <!-- Row 3b: Team fields -->
          <v-row dense class="mb-4 team-fields-row">
            <v-col md="3">
              <v-select
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                placeholder="Select"
                :items="['Select']"
              ></v-select>
            </v-col>
            <v-col md="4">
              <v-select
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                placeholder="Select"
                :items="['Select']"
              ></v-select>
            </v-col>
            <v-col md="4">
              <v-select
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                placeholder="Select"
                :items="['Select']"
              ></v-select>
            </v-col>
          </v-row>

          <!-- Row 4: Document drag-drop area -->
          <v-row dense class="mb-2 flex-grow-1">
            <v-col cols="12">
              <div
                class="document-drop-area d-flex flex-column align-center justify-center rounded-xl"
              >
                <v-icon size="95" color="grey-lighten-1" opacity="55%">mdi-arrow-up-box</v-icon>
                <p class="text-grey mt-4 text-center">
                  Start by drag and drop<br />OTP, IC, AML, LO, ACRA for biz, and<br />other
                  documents
                </p>
              </div>
            </v-col>
          </v-row>
        </v-col>

        <v-col md="6" class="dialog-card-text-half-content">
          <!-- Close button -->
          <div class="d-flex justify-end flex-shrink-0">
            <v-btn icon variant="text" size="small">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>

          <!-- Role section - outside scrollable area -->
          <div class="right-side-non-card-content">
            <div class="mb-4 flex-shrink-0">
              <v-label class="dialog-card-text-fields-label">Role</v-label>
              <div class="d-flex align-center">
                <v-select
                  variant="outlined"
                  rounded="lg"
                  density="compact"
                  hide-details
                  :items="['Client', 'Agent', 'Lawyer']"
                  style="max-width: 150px"
                ></v-select>
                <v-btn-toggle
                  v-model="roleType"
                  mandatory
                  rounded="xl"
                  density="compact"
                  class="ml-auto"
                  color="grey-darken-4"
                >
                  <v-btn value="individual" class="text-none">Individual</v-btn>
                  <v-btn value="commercial" class="text-none">Commercial</v-btn>
                </v-btn-toggle>
              </div>
            </div>
          </div>

          <!-- Scrollable content area -->
          <div class="right-content-scrollable flex-grow-1">
            <!-- Property section with border -->
            <div class="property-section rounded-xl pt-6 px-6 d-flex flex-column">
              <!-- Property Type on its own row -->
              <v-row dense class="mb-2">
                <v-col md="5">
                  <v-label class="dialog-card-text-fields-label mb-1">Property Type</v-label>
                  <v-select
                    v-model="form['propertyType']"
                    :items="['HDB Resale', 'Private', 'Commercial']"
                    variant="outlined"
                    rounded="lg"
                    density="compact"
                    hide-details
                  ></v-select>
                </v-col>
              </v-row>

              <!-- Other fields -->
              <v-row dense>
                <v-col
                  v-for="(field, index) in propertyFields"
                  :key="index"
                  :md="field.md"
                  class="mb-2"
                >
                  <v-label class="dialog-card-text-fields-label mb-1">{{ field.label }}</v-label>
                  <v-text-field
                    v-model="form[field.model]"
                    :type="field.type"
                    variant="outlined"
                    rounded="lg"
                    density="compact"
                    hide-details
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Go to Identity Check button -->
              <v-row dense class="mt-3 mb-4">
                <v-col cols="12">
                  <v-btn
                    block
                    rounded="xl"
                    color="grey-darken-3"
                    class="text-none"
                    style="letter-spacing: 0.4px"
                    height="45px"
                  >
                    Go to Identity Check
                  </v-btn>
                </v-col>
              </v-row>

              <!-- Divider and Submit button INSIDE the bordered section -->
              <v-divider class="mx-n6 mt-auto"></v-divider>
              <div class="submit-area">
                <span class="submit-btn" @click="submit">Submit</span>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { CaseData, ButtonConfig } from '@/common/types'

const props = defineProps<{
  isNew: boolean
  caseData: CaseData | null
  buttons: ButtonConfig[]
}>()

// Computed title - shows reference for existing case
const modalTitle = computed(() => {
  if (props.isNew) {
    return '' // Will show text field instead
  }
  return props.caseData?.reference || 'Case Details'
})

// Reference input for new cases
const newReferenceInput = reactive({
  value: '',
})

// Role type toggle (Individual/Commercial)
const roleType = ref('individual')

// Watch for changes to reset the input when opening a new case
watch(
  () => props.isNew,
  (isNew) => {
    if (isNew) {
      newReferenceInput.value = ''
    }
  },
)

// TODO: demo data to be removed
const propertyFields = [
  { type: 'text', label: 'Postcode', md: 4, model: 'postcode' },
  { type: 'text', label: 'Floor', md: 2, model: 'floor' },
  { type: 'text', label: 'Unit', md: 2, model: 'unit' },
  { type: 'text', label: 'Block', md: 3, model: 'block' },
  { type: 'text', label: 'Street', md: 6, model: 'street' },
  { type: 'text', label: 'Building Name', md: 5, model: 'buildingName' },
  { type: 'text', label: 'Property Price', md: 3, model: 'propertyPrice' },
  { type: 'date', label: 'Option Date', md: 4, model: 'optionDate' },
  { type: 'date', label: 'Option Expiry', md: 4, model: 'optionExpiry' },
  { type: 'date', label: 'Completion Date', md: 4, model: 'completionDate' },
  { type: 'text', label: 'No. of Weeks upon exercising', md: 2, model: 'weeksUponExercising' },
]

const form = reactive<Record<string, string>>({
  propertyType: '',
})

propertyFields.forEach((f) => {
  form[f.model] = '' // initialize reactive model
})

function submit() {
  console.log(form)
  // Include the reference for new cases
  if (props.isNew && newReferenceInput.value) {
    console.log('New case reference:', newReferenceInput.value)
  }
}
</script>

<style scoped>
.reference-input {
  max-width: 400px;
}

.document-drop-area {
  background-color: #f5f5f5;
  border: 2px dashed #e0e0e0;
  min-height: 475px;
  height: 100%;
  padding-top: 60px;
}

.property-section {
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.right-content-scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 0.9rem;
}

.submit-section {
  flex-shrink: 0;
  padding-top: 16px;
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

.right-side-non-card-content {
  padding: 0.9rem 0 0 0.9rem;
}

.team-fields-row :deep(.v-col) {
  flex-grow: 1;
}

/* Add gap between all fields */
.dialog-card-text-half-content :deep(.v-row) {
  gap: 10px;
}
</style>
