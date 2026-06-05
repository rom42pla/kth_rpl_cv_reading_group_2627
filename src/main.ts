import { createApp, ref, onMounted } from 'vue'
import { createWebHistory, createRouter } from 'vue-router'
import {
  Chart,
  ArcElement,
  Tooltip,
  Legend,
  PieController,
  BarController,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js'
Chart.register(
  ArcElement,
  Tooltip,
  Legend,
  PieController,
  BarController,
  CategoryScale,
  LinearScale,
  BarElement,
)

// pages
import App from './App.vue'
import Home from './Home.vue'
import FAQs from './FAQs.vue'
import Schedule from './Schedule.vue'
import Stats from './Stats.vue'
// components
import Navbar from './components/Navbar.vue'
import OrganizerCard from './components/OrganizerCard.vue'
import ScheduleSession from './components/ScheduleSession.vue'

import 'bootstrap/dist/css/bootstrap.min.css'

const routes = [
  { path: '/', component: Home },
  { path: '/faqs', component: FAQs },
  { path: '/schedule', component: Schedule },
  { path: '/stats', component: Stats },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
// adding components
app.component('Navbar', Navbar)
app.component('ScheduleSession', ScheduleSession)
app.component('OrganizerCard', OrganizerCard)
// adding libraries
app.use(router)
// mounting the webpage
app.mount('#app')
