<template>
  <v-row class="dialog-header align-center" dense>
    <!-- Left side: Title or Input -->
    <v-col :md="leftColWidth">
      <!-- Input mode (New Case) OR Editing mode -->
      <template v-if="showInput || isEditing">
        <v-label v-if="showInput" class="dialog-card-text-fields-label">{{ inputLabel }}</v-label>
        <v-text-field
          ref="titleInputRef"
          :model-value="isEditing ? editableTitle : inputValue"
          @update:model-value="handleInputChange"
          @blur="handleEditComplete"
          @keyup.enter="handleEditComplete"
          variant="outlined"
          density="compact"
          hide-details
          rounded="lg"
          class="header-input"
        ></v-text-field>
      </template>

      <!-- Title mode -->
      <template v-else>
        <span
          v-if="titleIcon === 'edit'"
          class="header-title header-title-editable"
          @click="startEditing"
        >
          {{ title }}
          <v-icon size="14" class="ml-1">mdi-pencil</v-icon>
        </span>
        <span v-else class="header-title">{{ title }}</span>

        <div v-if="subtitle" class="header-subtitle">{{ subtitle }}</div>
      </template>
    </v-col>

    <!-- Right side: Buttons -->
    <v-col v-if="buttons && buttons.length > 0" class="d-flex align-center justify-end header-buttons-col">
      <v-btn
        v-for="(button, index) in buttons"
        :key="index"
        :color="button.color || 'white'"
        rounded="lg"
        class="text-none header-btn"
        :prepend-icon="button.icon"
        @click="$emit('button-click', button.label)"
      >
        {{ button.label }}
      </v-btn>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import type { ButtonConfig } from '@/common/types'

const props = defineProps<{
  // Title options
  title?: string
  titleIcon?: 'edit' | null
  subtitle?: string

  // Input mode
  showInput?: boolean
  inputLabel?: string
  inputValue?: string

  // Buttons
  buttons?: ButtonConfig[]
}>()

const emit = defineEmits<{
  (e: 'update:inputValue', value: string): void
  (e: 'update:title', value: string): void
  (e: 'button-click', label: string): void
}>()

const isEditing = ref(false)
const editableTitle = ref('')
const titleInputRef = ref<HTMLInputElement | null>(null)

function startEditing() {
  if (props.titleIcon !== 'edit') return
  editableTitle.value = props.title || ''
  isEditing.value = true
  nextTick(() => {
    titleInputRef.value?.focus()
  })
}

function handleInputChange(value: string) {
  if (isEditing.value) {
    editableTitle.value = value
  } else {
    emit('update:inputValue', value)
  }
}

function handleEditComplete() {
  if (isEditing.value) {
    emit('update:title', editableTitle.value)
    isEditing.value = false
  }
}

const leftColWidth = computed(() => {
  if (!props.buttons || props.buttons.length === 0) return 12
  return 5
})
</script>

<style scoped>
.dialog-header {
  min-height: 48px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  display: inline-flex;
  align-items: center;
}

.header-title-editable {
  cursor: pointer;
}

.header-title-editable:hover {
  color: #1976d2;
}

.header-subtitle {
  font-size: 13px;
  color: #999;
  margin-top: 2px;
}

.header-input {
  max-width: 250px;
}

.header-buttons-col {
  gap: 12px;
}

.header-btn {
  box-shadow: none !important;
  border: 1px solid #d8d8d8 !important;
  letter-spacing: 0.1px !important;
}
</style>
