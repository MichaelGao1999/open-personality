import { createRouter, createWebHashHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionnairePage from '../views/QuestionnairePage.vue'
import ReportPage from '../views/ReportPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/questionnaire', name: 'Questionnaire', component: QuestionnairePage },
  { path: '/report/:token?', name: 'Report', component: ReportPage },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
