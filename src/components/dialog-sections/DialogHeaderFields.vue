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
          v-if="titleIcon === 'edit' && title"
          class="header-title header-title-editable"
          @click="startEditing"
        >
          {{ title }}
          <v-icon size="14" class="ml-1">mdi-pencil</v-icon>
        </span>
        <span v-else-if="title" class="header-title">{{ title }}</span>

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

<style scoped lang="scss">
@use '@/styles/DialogHeaderFields.scss';
</style>
