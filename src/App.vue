<template>
  <v-app>
    <v-app-bar app class="app-bar-layout" flat>
      <div class="page-title">{{ pageTitle }}</div>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon style="margin-top: 8px;">mdi-bell</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-if="!isAuthRoute" app location="left" permanent disable-resize-watcher class="nav-drawer">
      <div class="app-bar-layout">
        <v-img
          src="/src/assets/images/logo.jpg"
          alt="Company Logo"
          class="logo-img"
        ></v-img>
      </div>
      <div class="menu-scroll">
 <v-list nav>
        <v-list-item title="Dashboard" to="/dashboard" prepend-icon="mdi-view-dashboard" />
        <v-list-item title="Cases" to="/cases" prepend-icon="mdi-file-document" />
        <v-list-item title="Template" to="/template" prepend-icon="mdi-file-document" />
        <v-list-item title="Insights" to="/insights" prepend-icon="mdi-chart-areaspline" />
        <v-list-item title="Workspace" to="/workspace" prepend-icon="mdi-view-grid" />
        <v-list-item title="Team Assignment" to="/teamassignment" prepend-icon="mdi-account-multiple" />
        <v-list-item title="Company" to="/company" prepend-icon="mdi-bell-outline" />
        <v-list-item title="Knowledge" to="/knowledge" prepend-icon="mdi-book-open-variant" />
        <v-list-item title="Links" to="/links" prepend-icon="mdi-link-variant" />
        <v-list-item title="Settings" to="/settings" prepend-icon="mdi-cog" />
      </v-list>
      </div>

      <v-spacer></v-spacer>
      <v-divider></v-divider>
      <v-list-item class="user-info">
        <v-list-item-avatar class="user-avatar">
          <v-icon size="30">mdi-account-circle</v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>John Doe</v-list-item-title>
          <v-list-item-subtitle>john@example.com</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-navigation-drawer>
    <v-main>
      <v-container fluid class="pa-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()

// Determines if the current route is a public/auth route (e.g., /login)
const isAuthRoute = computed(() => {
  // We assume any route with meta.public = true does not need the sidebar
  console.log('Route Meta:', route.meta)
  return route.meta.public === true
})

// Dynamic page title based on current route
const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard': 'Dashboard',
    '/cases': 'Cases',
    '/template': 'Template',
    '/insights': 'Insights',
    '/workspace': 'Workspace',
    '/ministryoflaw': 'Ministry of Law',
    '/company': 'Company',
    '/knowledge': 'Knowledge',
    '/links': 'Links',
    '/settings': 'Settings'
  }
  return titles[route.path] || ''
})
</script>
