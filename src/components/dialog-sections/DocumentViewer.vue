<template>
  <div class="document-viewer">
    <!-- Document display area -->
    <div class="document-display rounded-xl">
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
            <v-icon>mdi-chevron-left</v-icon>
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
                <v-icon size="48" color="grey">mdi-file-document-outline</v-icon>
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
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>

          <!-- Add document button -->
          <v-btn
            icon
            variant="flat"
            color="grey-darken-3"
            size="small"
            class="add-doc-btn"
            @click="$emit('add-document')"
          >
            <v-icon>mdi-plus</v-icon>
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
            <v-btn icon variant="text" size="x-small">
              <v-icon>mdi-magnify-plus-outline</v-icon>
            </v-btn>
            <v-btn icon variant="text" size="x-small">
              <v-icon>mdi-magnify-minus-outline</v-icon>
            </v-btn>
          </div>
        </div>
      </template>

      <!-- Empty state: drag and drop -->
      <template v-else>
        <div class="drop-area d-flex flex-column align-center justify-center">
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
import { ref, computed } from 'vue'

interface Document {
  name: string
  type: string
  previewUrl?: string
}

const props = defineProps<{
  modelValue?: Document[]
}>()

defineEmits<{
  (e: 'update:modelValue', value: Document[]): void
  (e: 'add-document'): void
  (e: 'remove-document', index: number): void
}>()

const documents = ref<Document[]>(props.modelValue || [])
const currentIndex = ref(0)

const currentDocument = computed(() => documents.value[currentIndex.value])

// TODO: demo data to be removed
const documentTypes = ['OTP', 'IC', 'AML', 'LO', 'ACRA']

function prevDocument() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

function nextDocument() {
  if (currentIndex.value < documents.value.length - 1) {
    currentIndex.value++
  }
}

function updateDocumentType(type: string) {
  const doc = documents.value[currentIndex.value]
  if (doc) {
    doc.type = type
  }
}
</script>

<style scoped>
.document-viewer {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.document-display {
  background-color: #f5f5f5;
  border: 2px dashed #e0e0e0;
  min-height: 475px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.document-carousel {
  flex: 1;
  display: flex;
  align-items: center;
  position: relative;
  padding: 16px;
}

.nav-btn {
  position: absolute;
  z-index: 1;
}

.nav-prev {
  left: 8px;
}

.nav-next {
  right: 8px;
}

.add-doc-btn {
  position: absolute;
  top: 16px;
  right: 16px;
}

.document-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 48px;
}

.document-preview {
  max-width: 100%;
  max-height: 350px;
  overflow: hidden;
}

.preview-image {
  max-width: 100%;
  max-height: 350px;
  object-fit: contain;
}

.preview-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 280px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.document-info-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.doc-name-container {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
  flex-shrink: 1;
}

.doc-name {
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.doc-type-select {
  width: 120px;
  flex-shrink: 0;
}

.zoom-controls {
  margin-left: auto;
  display: flex;
  gap: 4px;
}

.drop-area {
  flex: 1;
  padding-top: 60px;
}
</style>
