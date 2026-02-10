<template>
  <div class="team-fields">
    <v-row dense class="mt-1">
      <v-col md="3" class="d-flex align-center pb-0">
        <v-label class="dialog-card-text-fields-label">BDM</v-label>
        <span class="text-caption mr-1 ml-auto">Save</span>
        <v-checkbox v-model="saveFlags.bdm" hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
      </v-col>
      <v-col md="4" class="d-flex align-center pb-0">
        <v-label class="dialog-card-text-fields-label">Lawyer-IC</v-label>
        <span class="text-caption mr-1 ml-auto">Save</span>
        <v-checkbox v-model="saveFlags.lawyerIc" hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
      </v-col>
      <v-col md="4" class="d-flex align-center pb-0">
        <v-label class="dialog-card-text-fields-label">Secretary-IC</v-label>
        <span class="text-caption mr-1 ml-auto">Save</span>
        <v-checkbox v-model="saveFlags.secretaryIc" hide-details density="compact" class="ma-0 pa-0"></v-checkbox>
      </v-col>
    </v-row>

    <v-row dense class="mb-4 team-fields-row">
      <v-col md="3">
        <v-select
          v-model="team.bdm"
          :items="bdmOptions"
          variant="outlined"
          rounded="lg"
          density="compact"
          hide-details
          placeholder="Select"
        ></v-select>
      </v-col>
      <v-col md="4">
        <v-select
          v-model="team.lawyerIc"
          :items="lawyerOptions"
          variant="outlined"
          rounded="lg"
          density="compact"
          hide-details
          placeholder="Select"
        ></v-select>
      </v-col>
      <v-col md="4">
        <v-select
          v-model="team.secretaryIc"
          :items="secretaryOptions"
          variant="outlined"
          rounded="lg"
          density="compact"
          hide-details
          placeholder="Select"
        ></v-select>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { TeamData } from '@/common/types'

const props = defineProps<{
  modelValue?: TeamData
  bdmOptions?: string[]
  lawyerOptions?: string[]
  secretaryOptions?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: TeamData): void
}>()

const team = reactive<TeamData>({
  bdm: props.modelValue?.bdm || '',
  lawyerIc: props.modelValue?.lawyerIc || '',
  secretaryIc: props.modelValue?.secretaryIc || ''
})

watch(team, (val) => {
  emit('update:modelValue', { ...val })
}, { deep: true })

const saveFlags = reactive({
  bdm: false,
  lawyerIc: false,
  secretaryIc: false
})

// TODO: demo data to be removed
const bdmOptions = props.bdmOptions || ['Jennifer', 'Alice', 'David']
const lawyerOptions = props.lawyerOptions || ['Alex', 'Bob', 'Emily']
const secretaryOptions = props.secretaryOptions || ['Mindy', 'Charlie', 'Fiona']
</script>

<style scoped>
.team-fields-row :deep(.v-col) {
  flex-grow: 1;
}
</style>
