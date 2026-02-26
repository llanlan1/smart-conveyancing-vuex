<template>
  <div class="case-header-info">
    <v-row dense align="center" justify="space-between">
      <v-col cols="auto">
        <div class="info-item">
          <v-label class="info-label">
            {{ refLabel }}
            <v-btn icon variant="text" size="x-small" class="ml-1">
              <v-icon size="14">mdi-content-copy</v-icon>
            </v-btn>
          </v-label>
          <div class="info-value">
            <div v-for="(line, i) in referenceNumber.split('\n')" :key="i">{{ line }}</div>
          </div>
        </div>
      </v-col>
      <v-col cols="auto">
        <div class="info-item">
          <v-label class="info-label">
            Property
            <v-btn icon variant="text" size="x-small" class="ml-1">
              <v-icon size="14">mdi-content-copy</v-icon>
            </v-btn>
          </v-label>
          <div class="info-value property-value">
            <div>{{ propertyLine1 }}</div>
            <div>{{ propertyLine2 }}</div>
            <div>{{ propertyLine3 }}</div>
          </div>
        </div>
      </v-col>
      <v-col cols="auto">
        <div class="info-item">
          <v-label class="info-label">Case Type</v-label>
          <div class="info-value case-type-value">
            <div>{{ caseTypeLine1 }}</div>
            <div>{{ caseTypeLine2 }}</div>
            <div>{{ caseTypeLine3 }}</div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  referenceNumber: string
  address: string
  caseType: string
  refLabel?: string
}>()

const refLabel = computed(() => props.refLabel || 'Ref. Number')

// Parse address into 3 lines (street, unit, postal)
const propertyLine1 = computed(() => {
  const parts = props.address.split(' ')
  return parts.slice(0, 4).join(' ')
})

const propertyLine2 = computed(() => {
  const match = props.address.match(/#\d+-\d+/)
  return match ? match[0] : ''
})

const propertyLine3 = computed(() => {
  const match = props.address.match(/\d{6}$/)
  return match ? match[0] : ''
})

// Parse case type into lines
const caseTypeLine1 = computed(() => {
  const parts = props.caseType.split(' ')
  return parts[0] || ''
})

const caseTypeLine2 = computed(() => {
  const parts = props.caseType.split(' ')
  return parts[1] || ''
})

const caseTypeLine3 = computed(() => {
  const parts = props.caseType.split(' ')
  return parts.slice(2).join(' ') || ''
})
</script>

<style scoped>
.case-header-info {
  padding: 8px 0;
}

.info-item {
  min-width: 100px;
}

.info-label {
  font-size: 12px;
  color: #666;
  display: flex;
  align-items: center;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
}

.property-value,
.case-type-value {
  font-size: 12px;
  font-weight: 400;
  color: #333;
}
</style>
