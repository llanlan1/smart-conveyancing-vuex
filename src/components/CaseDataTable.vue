<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    item-value="name"
    :items-per-page-options="[10, 25, 50, 100]"
    @update:options="loadItems"
    fixed-header
    fixed-footer
    class="card-table"
  >
    <template v-slot:item="props">
      <tr>
        <!-- Loop through the headers to render each cell (td) dynamically -->
        <td
          v-for="(header, index) in headers"
          :key="index"
          @click="handleCellClick(props.item, header.key)"
          style="cursor: pointer"
        >
          <!-- Check if cell value is an array -->
          <template v-if="Array.isArray(props.item[header.key as keyof CaseData])">
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <v-chip
                v-for="(item, i) in (props.item[header.key as keyof CaseData] as RoleItem[])"
                :key="i"
                size="small"
              >
                <strong>{{ item.type }}</strong> - {{ item.name }}
              </v-chip>
            </div>
          </template>
          <!-- Otherwise display as normal text -->
          <template v-else>
            {{ props.item[header.key as keyof CaseData] }}
          </template>
        </td>
      </tr>
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { fakeApi } from '@/api/fakeApi'

// TODO: demo data to be removed
interface RoleItem {
  type: string // BDM, LIC, SIC
  name: string // Person's name
}

interface CaseData {
  name: string
  horsepower: number
  fuel: string
  origin: string
  price: number
  roles?: RoleItem[] // Optional array for cells with multiple elements
}

interface ApiResponse {
  items: CaseData[]
  total: number
}

const itemsPerPage = ref(10)
const serverItems = ref<CaseData[]>([])
const loading = ref(true)
const totalItems = ref(0)

// TODO: demo data to be removed
const headers = ref<Array<{ title: string; key: string; align: 'start' | 'end' | 'center' }>>([
  { title: 'Reference', key: 'reference', align: 'start' },
  { title: 'Address', key: 'address', align: 'start' },
  { title: 'Case Type', key: 'caseType', align: 'start' },
  { title: 'Client', key: 'client', align: 'start' },
  { title: 'Team', key: 'team', align: 'start' },
  { title: 'Status', key: 'status', align: 'start' },
  { title: 'Shortfall', key: 'shortfall', align: 'start' },
  { title: 'Action', key: 'action', align: 'start' },
  { title: 'Select All', key: 'selectAll', align: 'center' },
])

// TODO: demo data to be removed
const fakeData = [
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Sales HDB Flat', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC' },

]

const loadItems = ({
  page,
  itemsPerPage,
  sortBy,
}: {
  page: number
  itemsPerPage: number
  sortBy: { key: string; order: string }[]
}) => {
  loading.value = true
  fakeApi(fakeData, {
    page,
    itemsPerPage,
    sortBy: sortBy as Array<{ key: string; order: 'asc' | 'desc' }>,
  }).then((response: unknown) => {
    const data = response as ApiResponse
    serverItems.value = data.items
    totalItems.value = data.total
    loading.value = false
  })
}

// Function to handle cell clicks
const handleCellClick = (item: CaseData, columnKey: string) => {
  console.log(`Cell clicked: ${columnKey} - `, item)
  // You can trigger other actions here, like opening a modal or editing data
  // For example: openModal(item)
}
</script>
