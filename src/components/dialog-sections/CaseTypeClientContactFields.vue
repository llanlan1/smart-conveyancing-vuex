<template>
  <v-row dense class="mt-6 align-end">
    <v-col md="3" class="d-flex align-center pb-0">
      <v-label class="dialog-card-text-fields-label mb-2">Case Type</v-label>
    </v-col>
    <v-col md="3" class="d-flex align-center pb-0">
      <v-label class="dialog-card-text-fields-label">Phone</v-label>
      <span class="text-caption ml-auto mr-1">Client</span>
      <v-checkbox
        :model-value="phoneClient"
        @update:model-value="$emit('update:phoneClient', $event)"
        hide-details
        density="compact"
        class="ma-0 pa-0"
      ></v-checkbox>
    </v-col>
    <v-col md="5" class="d-flex align-center pb-0">
      <v-label class="dialog-card-text-fields-label">Email Address</v-label>
      <span class="text-caption ml-auto mr-1">Client</span>
      <v-checkbox
        :model-value="emailClient"
        @update:model-value="$emit('update:emailClient', $event)"
        hide-details
        density="compact"
        class="ma-0 pa-0"
      ></v-checkbox>
    </v-col>
  </v-row>

  <v-row dense class="mt-1">
    <v-col md="3">
      <v-select
        :model-value="caseType"
        @update:model-value="$emit('update:caseType', $event)"
        :items="caseTypeOptions"
        variant="outlined"
        rounded="lg"
        density="compact"
        hide-details
      ></v-select>
    </v-col>
    <v-col md="3">
      <v-text-field
        :model-value="phone"
        @update:model-value="$emit('update:phone', $event)"
        variant="outlined"
        rounded="lg"
        density="compact"
        hide-details
        placeholder="87654321"
      ></v-text-field>
    </v-col>
    <v-col md="5">
      <v-text-field
        :model-value="email"
        @update:model-value="$emit('update:email', $event)"
        variant="outlined"
        rounded="lg"
        density="compact"
        hide-details
        :placeholder="emailPlaceholder"
      ></v-text-field>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
defineProps<{
  caseType: string
  phone: string
  email: string
  phoneClient: boolean
  emailClient: boolean
  caseTypeOptions: string[]
  emailPlaceholder?: string
}>()

defineEmits<{
  (e: 'update:caseType', value: string): void
  (e: 'update:phone', value: string): void
  (e: 'update:email', value: string): void
  (e: 'update:phoneClient', value: boolean): void
  (e: 'update:emailClient', value: boolean): void
}>()
</script>
