export interface CaseData {
  name: string
  reference: string
  systemReference: string // Auto-generated system reference
  address: string
  caseType: string
  client: string
  status?: string
  shortfall?: string
  createdAt: string // Hidden field for sorting (newest/oldest)
  roles: RoleItem[] // Array of role assignments (BDM, LIC, SIC, etc.)
}

export interface RoleItem {
  type: string // BDM, LIC, SIC
  name: string // Person's name
}

export interface ApiResponse {
  items: CaseData[]
  total: number
}

export interface ButtonConfig {
  label: string
  icon: string
  color: string
  outlined?: boolean
  height?: string
  width?: string
  rounded?: string
}
