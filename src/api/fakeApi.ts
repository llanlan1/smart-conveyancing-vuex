interface PaginationOptions {
  page: number
  itemsPerPage: number
  sortBy: Array<{ key: string; order: 'asc' | 'desc' }>
}

export async function fakeApi(data: unknown[], { page, itemsPerPage, sortBy }: PaginationOptions) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const start = (page - 1) * itemsPerPage
      const end = start + itemsPerPage
      const items = (data as Record<string, unknown>[]).slice()

      // Sorting logic
      if (sortBy.length && sortBy[0]) {
        const sortKey = sortBy[0].key
        const sortOrder = sortBy[0].order
        items.sort((a, b) => {
          const aValue = a[sortKey as string]
          const bValue = b[sortKey as string]
          return sortOrder === 'desc'
            ? (bValue as number) - (aValue as number)
            : (aValue as number) - (bValue as number)
        })
      }

      // Paginate the items
      const paginated = items.slice(start, end)

      // Resolve with the paginated data and the total count
      resolve({ items: paginated, total: items.length })
    }, 500) // Simulate a delay like an API request
  })
}
