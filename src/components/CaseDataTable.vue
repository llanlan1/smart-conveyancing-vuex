<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    item-value="name"
    :items-per-page-options="[5, 10, 25, 50, 100]"
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
          {{ props.item[header.key as keyof CarData] }}
        </td>
      </tr>
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { fakeApi } from '@/api/fakeApi'

// TODO: demo data to be removed
interface CarData {
  name: string
  horsepower: number
  fuel: string
  origin: string
  price: number
}

interface ApiResponse {
  items: CarData[]
  total: number
}

const itemsPerPage = ref(5)
const serverItems = ref<CarData[]>([])
const loading = ref(true)
const totalItems = ref(0)

// TODO: demo data to be removed
const headers = ref<Array<{ title: string; key: string; align: 'start' | 'end' | 'center' }>>([
  { title: 'Car Model', key: 'name', align: 'start' },
  { title: 'Horsepower', key: 'horsepower', align: 'end' },
  { title: 'Fuel Type', key: 'fuel', align: 'start' },
  { title: 'Origin', key: 'origin', align: 'start' },
  { title: 'Price ($)', key: 'price', align: 'end' },
])

// TODO: demo data to be removed
const fakeData = [
  { name: 'Ford Mustang', horsepower: 450, fuel: 'Gasoline', origin: 'USA', price: 55000 },
  { name: 'Tesla Model S', horsepower: 670, fuel: 'Electric', origin: 'USA', price: 79999 },
  { name: 'BMW M3', horsepower: 503, fuel: 'Gasoline', origin: 'Germany', price: 70000 },
  { name: 'Audi RS6', horsepower: 591, fuel: 'Gasoline', origin: 'Germany', price: 109000 },
  { name: 'Chevrolet Camaro', horsepower: 650, fuel: 'Gasoline', origin: 'USA', price: 62000 },
  { name: 'Porsche 911', horsepower: 379, fuel: 'Gasoline', origin: 'Germany', price: 101000 },
  { name: 'Jaguar F-Type', horsepower: 575, fuel: 'Gasoline', origin: 'UK', price: 61000 },
  { name: 'Mazda MX-5', horsepower: 181, fuel: 'Gasoline', origin: 'Japan', price: 26000 },
  { name: 'Nissan GT-R', horsepower: 565, fuel: 'Gasoline', origin: 'Japan', price: 113540 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
  { name: 'Mercedes-AMG GT', horsepower: 523, fuel: 'Gasoline', origin: 'Germany', price: 115900 },
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
const handleCellClick = (item: CarData, columnKey: string) => {
  console.log(`Cell clicked: ${columnKey} - `, item)
  // You can trigger other actions here, like opening a modal or editing data
  // For example: openModal(item)
}
</script>
