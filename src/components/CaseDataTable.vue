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
          class="data-cell"
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
          <!-- Check if cell value is an array (roles column) -->
          <template v-else-if="Array.isArray(props.item[header.key as keyof CaseData])">
            <div class="roles-list">
              <div
                v-for="(role, i) in getVisibleRoles(props.item[header.key as keyof CaseData] as RoleItem[])"
                :key="i"
                class="role-row"
              >
                <strong>{{ role.type }}</strong> {{ role.name }}
              </div>
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
import type { CaseData, RoleItem, ApiResponse } from '@/common/types'

// Define which columns should open modal with reference title
const columnsWithReferenceTitle = ['reference', 'address', 'caseType', 'roles', 'shortfall']

// Only these roles are displayed in the Team column
const visibleRoles = ['BDM', 'LIC', 'SIC']

const getVisibleRoles = (roles: RoleItem[]) => {
  return roles.filter(r => visibleRoles.includes(r.type))
}

// Emit for parent component
const emit = defineEmits<{
  (e: 'open-case', caseData: CaseData, column: string): void
}>()


const itemsPerPage = ref(5)
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
  { title: 'Team', key: 'roles', align: 'start' },
  { title: 'Status', key: 'status', align: 'start' },
  { title: 'Shortfall', key: 'shortfall', align: 'start' },
  { title: 'Action', key: 'action', align: 'start' },
  { title: 'Select All', key: 'selectAll', align: 'center' },
])

// TODO: demo data to be removed
const fakeData: CaseData[] = [
  { name: 'HS(JL).65431', reference: 'HS(JL).65431', systemReference: 'SYS-001-2024', address: '123 ABC Avenue 6 #01-02 123456', caseType: 'Purchase Condo Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Alice Tan' }, { type: 'LIC', name: 'Bob Lee' }, { type: 'SIC', name: 'Charlie Ng' }], createdAt: '2024-01-05' },
  { name: 'HS(JL).65432', reference: 'HS(JL).65432', systemReference: 'SYS-002-2024', address: '456 DEF Street 8 #03-04 234567', caseType: 'Purchase Condo BUC', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'David Lim' }, { type: 'LIC', name: 'Emily Wong' }, { type: 'SIC', name: 'Fiona Chua' }], createdAt: '2024-02-10' },
  { name: 'HS(JL).65433', reference: 'HS(JL).65433', systemReference: 'SYS-003-2024', address: '789 GHI Road 10 #05-06 345678', caseType: 'Purchase Condo EC BUC', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Grace Ong' }, { type: 'LIC', name: 'Henry Koh' }, { type: 'SIC', name: 'Irene Teo' }], createdAt: '2024-03-15' },
  { name: 'HS(JL).65434', reference: 'HS(JL).65434', systemReference: 'SYS-004-2024', address: '101 JKL Lane 12 #07-08 456789', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'James Goh' }, { type: 'LIC', name: 'Karen Sim' }, { type: 'SIC', name: 'Larry Yeo' }], createdAt: '2024-04-20' },
  { name: 'HS(JL).65435', reference: 'HS(JL).65435', systemReference: 'SYS-005-2024', address: '202 MNO Drive 14 #09-10 567890', caseType: 'Purchase Landed BUC', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Alice Tan' }, { type: 'LIC', name: 'Nancy Ho' }, { type: 'SIC', name: 'Oscar Poh' }], createdAt: '2024-05-25' },
  { name: 'HS(JL).65436', reference: 'HS(JL).65436', systemReference: 'SYS-006-2024', address: '303 PQR Blvd 16 #11-12 678901', caseType: 'Purchase Commercial BUC', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'David Lim' }, { type: 'LIC', name: 'Bob Lee' }, { type: 'SIC', name: 'Rachel Ang' }], createdAt: '2024-06-30' },
  { name: 'HS(JL).65437', reference: 'HS(JL).65437', systemReference: 'SYS-007-2024', address: '404 STU Court 18 #13-14 789012', caseType: 'Purchase Commercial Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Grace Ong' }, { type: 'LIC', name: 'Emily Wong' }, { type: 'SIC', name: 'Charlie Ng' }], createdAt: '2024-07-05' },
  { name: 'HS(JL).65438', reference: 'HS(JL).65438', systemReference: 'SYS-008-2024', address: '505 VWX Place 20 #15-16 890123', caseType: 'Purchase Condo Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'James Goh' }, { type: 'LIC', name: 'Henry Koh' }, { type: 'SIC', name: 'Fiona Chua' }], createdAt: '2024-08-10' },
  { name: 'HS(JL).65439', reference: 'HS(JL).65439', systemReference: 'SYS-009-2024', address: '606 YZA Circle 22 #17-18 901234', caseType: 'Sales Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Alice Tan' }, { type: 'LIC', name: 'Karen Sim' }, { type: 'SIC', name: 'Irene Teo' }], createdAt: '2024-09-15' },
  { name: 'HS(JL).65440', reference: 'HS(JL).65440', systemReference: 'SYS-010-2024', address: '707 BCD Way 24 #19-20 012345', caseType: 'Purchase Commercial Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'David Lim' }, { type: 'LIC', name: 'Nancy Ho' }, { type: 'SIC', name: 'Larry Yeo' }], createdAt: '2024-10-20' },
  { name: 'HS(JL).65441', reference: 'HS(JL).65441', systemReference: 'SYS-011-2024', address: '808 EFG Terrace 26 #21-22 123456', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'Grace Ong' }, { type: 'LIC', name: 'Bob Lee' }, { type: 'SIC', name: 'Oscar Poh' }], createdAt: '2024-11-25' },
  { name: 'HS(JL).65442', reference: 'HS(JL).65442', systemReference: 'SYS-012-2024', address: '909 HIJ Gardens 28 #23-24 234567', caseType: 'Purchase Landed Resale', client: 'Tan Yu Jing Alice S1234567Z', roles: [{ type: 'BDM', name: 'James Goh' }, { type: 'LIC', name: 'Emily Wong' }, { type: 'SIC', name: 'Rachel Ang' }], createdAt: '2024-12-30' },
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

<style scoped lang="scss">
@use '@/styles/CaseDataTable.scss';
</style>
