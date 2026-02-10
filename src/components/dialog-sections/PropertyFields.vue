<template>
  <div class="property-section rounded-xl pt-6 px-6 d-flex flex-column">
    <v-row dense class="mb-2">
      <v-col md="5">
        <v-label class="dialog-card-text-fields-label mb-1">Property Type</v-label>
        <v-select
          v-model="form.propertyType"
          :items="propertyTypeOptions"
          variant="outlined"
          rounded="lg"
          density="compact"
          hide-details
        ></v-select>
      </v-col>
      <v-col v-if="showEthnicQuota" md="7" class="d-flex align-center pt-6">
        <v-checkbox
          v-model="form.checkEthnicQuota"
          label="Check Ethnic Quota"
          hide-details
          density="compact"
          class="ma-0 pa-0"
        ></v-checkbox>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col
        v-for="(field, index) in propertyFields"
        :key="index"
        :md="field.md"
        class="mb-2"
      >
        <div class="d-flex align-center mb-1">
          <v-label class="dialog-card-text-fields-label">{{ field.label }}</v-label>
          <v-btn
            v-if="showCopyIcons && field.copyable"
            icon
            variant="text"
            size="x-small"
            class="ml-1"
          >
            <v-icon size="14">mdi-content-copy</v-icon>
          </v-btn>
        </div>
        <v-text-field
          v-model="form[field.model]"
          :type="field.type"
          :disabled="disabled"
          variant="outlined"
          rounded="lg"
          density="compact"
          hide-details
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row dense class="mt-3 mb-4">
      <v-col cols="12">
        <v-btn
          block
          rounded="xl"
          color="grey-darken-3"
          class="text-none"
          style="letter-spacing: 0.4px"
          height="45px"
          :disabled="identityCheckDisabled"
        >
          Go to Identity Check
        </v-btn>
      </v-col>
    </v-row>

    <v-divider class="mx-n6 mt-auto"></v-divider>
    <div class="submit-area">
      <span class="submit-btn" @click="handleSubmit">{{ submitLabel }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import type { PropertyFormData } from '@/common/types'

const props = defineProps<{
  modelValue?: Partial<PropertyFormData>
  disabled?: boolean
  showCopyIcons?: boolean
  showEthnicQuota?: boolean
  identityCheckDisabled?: boolean
  submitLabel?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: PropertyFormData): void
  (e: 'submit'): void
}>()

const submitLabel = computed(() => props.submitLabel || 'Submit')

const form = reactive<PropertyFormData>({
  propertyType: props.modelValue?.propertyType || '',
  checkEthnicQuota: props.modelValue?.checkEthnicQuota || false,
  postcode: props.modelValue?.postcode || '',
  floor: props.modelValue?.floor || '',
  unit: props.modelValue?.unit || '',
  block: props.modelValue?.block || '',
  street: props.modelValue?.street || '',
  buildingName: props.modelValue?.buildingName || '',
  propertyPrice: props.modelValue?.propertyPrice || '',
  optionDate: props.modelValue?.optionDate || '',
  optionExpiry: props.modelValue?.optionExpiry || '',
  completionDate: props.modelValue?.completionDate || '',
  weeksUponExercising: props.modelValue?.weeksUponExercising || ''
})

// TODO: demo data to be removed
const propertyTypeOptions = ['HDB Resale', 'Private', 'Commercial']

const propertyFields = [
  { type: 'text', label: 'Postcode', md: 4, model: 'postcode', copyable: true },
  { type: 'text', label: 'Floor', md: 2, model: 'floor', copyable: true },
  { type: 'text', label: 'Unit', md: 2, model: 'unit', copyable: true },
  { type: 'text', label: 'Block', md: 3, model: 'block', copyable: true },
  { type: 'text', label: 'Street', md: 6, model: 'street', copyable: true },
  { type: 'text', label: 'Building Name', md: 5, model: 'buildingName', copyable: false },
  { type: 'text', label: 'Property Price', md: 3, model: 'propertyPrice', copyable: false },
  { type: 'date', label: 'Option Date', md: 4, model: 'optionDate', copyable: false },
  { type: 'date', label: 'Option Expiry', md: 4, model: 'optionExpiry', copyable: false },
  { type: 'date', label: 'Completion Date', md: 4, model: 'completionDate', copyable: false },
  { type: 'text', label: 'No. of Weeks upon exercising', md: 2, model: 'weeksUponExercising', copyable: false },
]

function handleSubmit() {
  emit('submit')
  emit('update:modelValue', form)
}
</script>

<style scoped>
.property-section {
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  height: 100%;
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
</style>
