<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    item-value="name"
    :items-per-page-options="[10, 25, 50, 100]"
    :sort-by="defaultSort"
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
          <!-- Special handling for reference column - show 2 links -->
          <template v-if="header.key === 'reference'">
            <div class="reference-links">
              <a
                href="#"
                class="reference-link user-ref"
                @click.stop.prevent="handleReferenceClick(props.item, 'user')"
              >
                {{ props.item.reference }}
              </a>
              <a
                href="#"
                class="reference-link system-ref"
                @click.stop.prevent="handleReferenceClick(props.item, 'system')"
              >
                {{ props.item.systemReference }}
              </a>
            </div>
          </template>
          <!-- Check if cell value is an array -->
          <template v-else-if="Array.isArray(props.item[header.key as keyof CaseData])">
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

// Define which columns should open modal with reference title
const columnsWithReferenceTitle = ['reference', 'address', 'caseType', 'team', 'shortfall']

// Emit for parent component
const emit = defineEmits<{
  (e: 'open-case', caseData: CaseData, column: string): void
}>()

// TODO: demo data to be removed
interface RoleItem {
  type: string // BDM, LIC, SIC
  name: string // Person's name
}

interface CaseData {
  name: string
  reference: string
  systemReference: string // Auto-generated system reference
  address: string
  caseType: string
  client: string
  team: string
  status?: string
  shortfall?: string
  createdAt: string // Hidden field for sorting (newest/oldest)
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

// Default sort: newest first (descending by createdAt)
const defaultSort = ref([{ key: 'createdAt', order: 'desc' as const }])

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
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', systemReference: 'SYS-001-2024', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Purchase Condo Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-01-05' },
  { name: 'HS(JL).65432', reference: 'HS(JL).65432', systemReference: 'SYS-002-2024', address: '456 DEF Street 8 #03-04 234567', caseType: 'Purchase Condo BUC', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-02-10' },
  { name: 'HS(JL).65433', reference: 'HS(JL).65433', systemReference: 'SYS-003-2024', address: '789 GHI Road 10 #05-06 345678', caseType: 'Purchase Condo EC BUC', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-03-15' },
  { name: 'HS(JL).65434', reference: 'HS(JL).65434', systemReference: 'SYS-004-2024', address: '101 JKL Lane 12 #07-08 456789', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-04-20' },
  { name: 'HS(JL).65435', reference: 'HS(JL).65435', systemReference: 'SYS-005-2024', address: '202 MNO Drive 14 #09-10 567890', caseType: 'Purchase Landed BUC', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-05-25' },
  { name: 'HS(JL).65436', reference: 'HS(JL).65436', systemReference: 'SYS-006-2024', address: '303 PQR Blvd 16 #11-12 678901', caseType: 'Purchase Commercial BUC', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-06-30' },
  { name: 'HS(JL).65437', reference: 'HS(JL).65437', systemReference: 'SYS-007-2024', address: '404 STU Court 18 #13-14 789012', caseType: 'Purchase Commercial Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-07-05' },
  { name: 'HS(JL).65438', reference: 'HS(JL).65438', systemReference: 'SYS-008-2024', address: '505 VWX Place 20 #15-16 890123', caseType: 'Purchase Condo Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-08-10' },
  { name: 'HS(JL).65439', reference: 'HS(JL).65439', systemReference: 'SYS-009-2024', address: '606 YZA Circle 22 #17-18 901234', caseType: 'Sales Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-09-15' },
  { name: 'HS(JL).65440', reference: 'HS(JL).65440', systemReference: 'SYS-010-2024', address: '707 BCD Way 24 #19-20 012345', caseType: 'Purchase Commercial Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-10-20' },
  { name: 'HS(JL).65441', reference: 'HS(JL).65441', systemReference: 'SYS-011-2024', address: '808 EFG Terrace 26 #21-22 123456', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-11-25' },
  { name: 'HS(JL).65442', reference: 'HS(JL).65442', systemReference: 'SYS-012-2024', address: '909 HIJ Gardens 28 #23-24 234567', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', team: 'BDM SIC LIC', createdAt: '2024-12-30' },
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
  // Skip if clicking on reference column (handled by handleReferenceClick)
  if (columnKey === 'reference') return

  console.log(`Cell clicked: ${columnKey} - `, item)

  // Check if this column should open modal with reference title
  if (columnsWithReferenceTitle.includes(columnKey)) {
    emit('open-case', item, columnKey)
  }
}

// Function to handle reference link clicks
const handleReferenceClick = (item: CaseData, refType: 'user' | 'system') => {
  console.log(`Reference clicked: ${refType} - `, item)
  emit('open-case', item, 'reference')
}
</script>

<style scoped>
.reference-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.reference-link {
  text-decoration: none;
  color: #1976d2;
  font-size: 13px;
  line-height: 1.4;
}

.reference-link:hover {
  text-decoration: underline;
}

.user-ref {
  font-weight: 600;
}

.system-ref {
  color: #666;
  font-size: 12px;
}
</style>
