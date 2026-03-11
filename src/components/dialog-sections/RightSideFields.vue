<template>
  <div class="form-fields-section rounded-xl pt-6 px-6 d-flex flex-column">
    <v-row>
      <template v-for="(field, index) in fields" :key="field.model || `divider-${index}`">
        <!-- Divider -->
        <v-col v-if="field.type === 'divider'" cols="12" class="my-2 px-0">
          <v-divider></v-divider>
        </v-col>

        <!-- Checkbox -->
        <v-col v-else-if="field.type === 'checkbox'" :md="field.md" class="d-flex align-center pt-6">
          <v-checkbox
            v-model="form[field.model!]"
            :label="field.label"
            hide-details
            density="compact"
            class="ma-0 pa-0"
          ></v-checkbox>
        </v-col>

        <!-- Select -->
        <v-col v-else-if="field.type === 'select'" :md="field.md" class="mb-2">
          <div class="d-flex align-center mb-1">
            <v-label class="dialog-card-text-fields-label">{{ field.label }}</v-label>
            <v-btn v-if="field.copyable" icon variant="text" size="x-small" class="ml-1">
              <v-icon size="14">mdi-content-copy</v-icon>
            </v-btn>
          </div>
          <v-select
            v-model="(form[field.model!] as string)"
            :items="field.items"
            variant="outlined"
            rounded="lg"
            density="compact"
            hide-details
            :disabled="disabled || field.disabled"
          ></v-select>
        </v-col>

        <!-- Text / Date -->
        <v-col v-else :md="field.md" class="mb-2">
          <div class="d-flex align-center mb-1">
            <v-label class="dialog-card-text-fields-label">{{ field.label }}</v-label>
            <v-btn v-if="field.copyable" icon variant="text" size="x-small" class="ml-1">
              <v-icon size="14">mdi-content-copy</v-icon>
            </v-btn>
          </div>
          <v-text-field
            v-model="form[field.model!]"
            :type="field.type === 'date' ? 'date' : 'text'"
            variant="outlined"
            rounded="lg"
            density="compact"
            hide-details
            :disabled="disabled || field.disabled"
            :placeholder="field.placeholder"
          ></v-text-field>
        </v-col>
      </template>
    </v-row>

    <slot></slot>

    <v-divider class="mx-n6 mt-auto"></v-divider>
    <div class="submit-area">
      <span class="submit-btn" @click="handleSubmit">{{ computedSubmitLabel }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'

export interface FormFieldConfig {
  type: 'text' | 'select' | 'date' | 'checkbox' | 'divider'
  label?: string
  model?: string
  md?: number
  items?: string[]
  copyable?: boolean
  placeholder?: string
  disabled?: boolean
  defaultValue?: string | boolean
}

const props = defineProps<{
  fields: FormFieldConfig[]
  modelValue?: Record<string, unknown>
  disabled?: boolean
  submitLabel?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Record<string, unknown>): void
  (e: 'submit'): void
}>()

const form = reactive<Record<string, unknown>>({})

for (const field of props.fields) {
  if (field.type !== 'divider' && field.model) {
    form[field.model] = props.modelValue?.[field.model]
      ?? field.defaultValue
      ?? (field.type === 'checkbox' ? false : '')
  }
}

const computedSubmitLabel = computed(() => props.submitLabel || 'Submit')

watch(form, () => {
  emit('update:modelValue', { ...form })
}, { deep: true })

function handleSubmit() {
  emit('submit')
}
</script>
