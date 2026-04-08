<template>
  <div
    class="document-viewer"
    @dragenter.prevent="dragCounter++; isDragging = true"
    @dragleave.prevent="dragCounter--; isDragging = dragCounter > 0"
    @dragover.prevent
    @drop.prevent="handleDrop"
  >
    <input
      ref="fileInput"
      type="file"
      multiple
      accept="image/*,.pdf"
      style="display: none"
      @change="handleFileSelect"
    />
    <!-- Document display area -->
    <div class="document-display rounded-xl" :class="{ 'drag-over': isDragging }">
      <template v-if="documents.length > 0">
        <!-- Document carousel -->
        <div class="document-carousel">
          <v-btn
            icon
            variant="text"
            size="small"
            class="nav-btn nav-prev"
            :disabled="currentIndex === 0"
            @click="prevDocument"
          >
            <v-icon size="46">mdi-chevron-left</v-icon>
          </v-btn>

          <div class="document-content">
            <div class="document-preview">
              <img
                v-if="currentDocument?.previewUrl"
                :src="currentDocument.previewUrl"
                :alt="currentDocument.name"
                class="preview-image"
              />
              <div v-else class="preview-placeholder">
                <v-icon size="46" color="grey">mdi-file-document-outline</v-icon>
              </div>

              <!-- Parse status overlay -->
              <div
                v-if="currentDocument?.parseStatus && currentDocument.parseStatus !== 'idle'"
                class="parse-status-overlay"
                :class="currentDocument.parseStatus"
              >
                <div class="parse-status-content">
                  <v-progress-circular
                    v-if="currentDocument.parseStatus === 'processing'"
                    indeterminate
                    color="white"
                    size="32"
                    width="3"
                  />
                  <v-icon v-else-if="currentDocument.parseStatus === 'done'" color="white" size="32">
                    mdi-check-circle
                  </v-icon>
                  <v-icon v-else-if="currentDocument.parseStatus === 'error'" color="white" size="32">
                    mdi-alert-circle
                  </v-icon>
                  <span class="parse-status-text">{{ parseStatusText }}</span>
                </div>
              </div>
            </div>
          </div>

          <v-btn
            icon
            variant="text"
            size="small"
            class="nav-btn nav-next"
            :disabled="currentIndex === documents.length - 1"
            @click="nextDocument"
          >
            <v-icon size="48">mdi-chevron-right</v-icon>
          </v-btn>

          <!-- Add document button -->
          <v-btn
            icon
            variant="flat"
            color="grey-darken-3"
            size="x-large"
            class="add-doc-btn"
            @click="openFilePicker"
          >
            <v-icon size="38">mdi-plus</v-icon>
          </v-btn>
        </div>

        <!-- Document info bar -->
        <div class="document-info-bar">
          <div class="doc-name-container">
            <span class="doc-name">{{ currentDocument?.name }}</span>
            <v-btn icon variant="text" size="x-small" @click="$emit('remove-document', currentIndex)">
              <v-icon size="16">mdi-close</v-icon>
            </v-btn>
          </div>
          <v-select
            :model-value="currentDocument?.type"
            @update:model-value="updateDocumentType"
            :items="documentTypes"
            variant="outlined"
            rounded="lg"
            density="compact"
            hide-details
            class="doc-type-select"
          ></v-select>
          <div class="zoom-controls">
            <v-btn icon variant="text" size="x-medium">
              <v-icon>mdi-magnify-plus-outline</v-icon>
            </v-btn>
            <v-btn icon variant="text" size="x-medium">
              <v-icon>mdi-magnify-minus-outline</v-icon>
            </v-btn>
          </div>
        </div>
      </template>

      <!-- Empty state: drag and drop -->
      <template v-else>
        <div class="drop-area d-flex flex-column align-center justify-center" style="cursor: pointer" @click="openFilePicker">
          <v-icon size="95" color="grey-lighten-1" style="opacity: 55%">mdi-arrow-up-box</v-icon>
          <p class="text-grey mt-4 text-center">
            Start by drag and drop<br />
            OTP, IC, AML, LO, ACRA for biz, and<br />
            other documents
          </p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Document, ParsedFields } from '@/common/types'

const props = defineProps<{
  modelValue?: Document[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Document[]): void
  (e: 'remove-document', index: number): void
  (e: 'fields-parsed', payload: { index: number; detectedType: string; fields: ParsedFields }): void
}>()

const documents = ref<Document[]>(props.modelValue || [])
const currentIndex = ref(0)
const isDragging = ref(false)
const dragCounter = ref(0)
const fileInput = ref<HTMLInputElement | null>(null)

const currentDocument = computed(() => documents.value[currentIndex.value])

// TODO: demo data to be removed
const documentTypes = ['OTP', 'IC—Front', 'IC—Back', 'IC—Both Sides', 'Passport', 'WhatsApp Screenshot', 'AML', 'LO', 'ACRA', 'Others']

const VALID_TYPES = new Set(documentTypes)

const parseStatusText = computed(() => {
  switch (currentDocument.value?.parseStatus) {
    case 'processing': return 'Parsing...'
    case 'done': return 'Parsed'
    case 'error': return 'Parse failed'
    default: return ''
  }
})

watch(() => props.modelValue, (val) => {
  documents.value = val || []
}, { deep: true })

function prevDocument() {
  if (currentIndex.value > 0) currentIndex.value--
}

function nextDocument() {
  if (currentIndex.value < documents.value.length - 1) currentIndex.value++
}

function updateDocumentType(type: string) {
  const doc = documents.value[currentIndex.value]
  if (doc) doc.type = type
}

function openFilePicker() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files) {
    addFiles(input.files)
    input.value = ''
  }
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  dragCounter.value = 0
  if (event.dataTransfer?.files) addFiles(event.dataTransfer.files)
}

function addFiles(files: FileList) {
  const startIndex = documents.value.length
  const newDocs: Document[] = Array.from(files).map((file) => {
    const isImage = file.type.startsWith('image/')
    return {
      name: file.name,
      type: '',
      previewUrl: isImage ? URL.createObjectURL(file) : undefined,
      file,
      parseStatus: 'processing' as const,
    }
  })
  documents.value = [...documents.value, ...newDocs]
  currentIndex.value = documents.value.length - 1
  emit('update:modelValue', [...documents.value])

  for (let i = 0; i < newDocs.length; i++) {
    parseDocument(startIndex + i)
  }
}

async function parseDocument(index: number) {
  const doc = documents.value[index]
  if (!doc?.file) return

  const formData = new FormData()
  formData.append('file', doc.file)

  try {
    const apiBase = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    const res = await fetch(`${apiBase}/parse-document`, {
      method: 'POST',
      body: formData,
    })

    if (!res.ok) throw new Error(`HTTP ${res.status}`)

    const result = await res.json()

    doc.type = VALID_TYPES.has(result.detected_type) ? result.detected_type : 'Others'
    doc.parseStatus = 'done'
    doc.parsedFields = result.fields

    emit('update:modelValue', [...documents.value])
    emit('fields-parsed', { index, detectedType: doc.type, fields: result.fields })
  } catch {
    doc.parseStatus = 'error'
    emit('update:modelValue', [...documents.value])
  }
}
</script>

<style scoped lang="scss">
@use '@/styles/DocumentUploadArea.scss';
</style>
