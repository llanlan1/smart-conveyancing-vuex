import { createRouter, createWebHistory } from 'vue-router'

// Define your routes
// The structure here mirrors the structure of your sidebar menu.
const routes = [
  // --- Main Menu Routes ---
  {
    path: '/',
    redirect: '/dashboard', // Redirects the root path to the Dashboard
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
    meta: { requiresAuth: true, title: 'Dashboard' },
  },
  {
    path: '/cases',
    name: 'Cases',
    component: () => import('@/pages/CasesPage.vue'), // This is the view you see in the screenshot
    meta: { requiresAuth: true, title: 'Cases Management' },
  },
  {
    path: '/appointment',
    name: 'Appointment',
    // Lazy loading for better performance, loads the component only when needed
    component: () => import('@/pages/AppointmentPage.vue'),
    meta: { requiresAuth: true, title: 'Appointments' },
  },
  {
    path: '/template',
    name: 'Template',
    component: () => import('@/pages/TemplatePage.vue'),
    meta: { requiresAuth: true, title: 'Document Templates' },
  },
  // --- Database Menu Routes (Example of nested routing) ---
  {
    path: '/database',
    name: 'Database',
    // Could use a wrapper component here if all database views share a sub-layout
    // component: DatabaseLayout,
    children: [
      {
        path: 'client', // Full path is /database/client
        name: 'ClientDatabase',
        component: () => import('@/pages/ClientPage.vue'),
        meta: { requiresAuth: true, title: 'Client' },
      },
      {
        path: 'agency', // Full path is /database/agency
        name: 'AgencyDatabase',
        component: () => import('@/pages/AgencyPage.vue'),
        meta: { requiresAuth: true, title: 'Agency' },
      },
      // ... other database routes
    ],
  },

  // --- Catch-all 404 Route ---
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: { title: '404 Not Found' },
  },
]

// 3. Create the router instance
const router = createRouter({
  // Use HTML5 history mode (clean URLs without #)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  // Ensure the app always scrolls to the top when navigating
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 4. Global Navigation Guards (for production-grade security)
// This guard checks for the `requiresAuth: true` meta field.
router.beforeEach((to, from, next) => {
  // 1. Update the document title
  document.title = to.meta.title ? `${to.meta.title} | Convey` : 'Convey App'

  // 2. Authentication Check (assuming you have a simple auth store)
  const isAuthenticated = true // Replace with actual check (e.g., from Pinia store)

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If auth is required and user is not logged in, redirect to login page
    next({ name: 'Login' }) // You would need to define a 'Login' route
  } else {
    // Continue navigation
    next()
  }
})

export default router
