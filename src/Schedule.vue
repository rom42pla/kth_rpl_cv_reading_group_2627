```vue
<template>
  <div class="container">
    <div class="col-md-8 mx-auto">
      <h1 class="mb-4">Schedule</h1>
      <p>
        Note that the schedule is always subject to change. <br />
        More sessions will be scheduled soon.
      </p>

      <div class="accordion" id="scheduleAccordion">
        <!-- Past seminars -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              :class="{ collapsed: !openPast }"
              type="button"
              @click="toggle('past')"
            >
              Past seminars ({{ pastSessions.length }})
            </button>
          </h2>
          <div class="accordion-collapse" :class="openPast ? 'collapse show' : 'collapse'">
            <div class="accordion-body">
              <template v-for="(session, index) in pagedPastSessions" :key="'past-' + index">
                <ScheduleSession
                  :session_number="session.session_number"
                  :date="session.date"
                  :time="session.time"
                  :venue="session.venue"
                  :topic="session.topic"
                  :presenter="session.presenter"
                  :paper_authors="session.paper_authors"
                  :paper_title="session.paper_title"
                  :paper_venue="session.paper_venue"
                  :paper_year="session.paper_year"
                  :slides_link="session.slides_link"
                  :paper_link="session.paper_link"
                  :arxiv_link="session.arxiv_link"
                />
              </template>
              <p v-if="!pastSessions.length" class="text-muted">No past seminars yet.</p>
              <nav v-if="pastTotalPages > 1" class="mt-3">
                <ul class="pagination pagination-sm justify-content-center">
                  <li class="page-item" :class="{ disabled: pastPage === 1 }">
                    <button class="page-link" @click="pastPage--">‹</button>
                  </li>
                  <li
                    v-for="(p, index) in visiblePastPages"
                    :key="`${p}-${index}`"
                    class="page-item"
                    :class="{ active: pastPage === p, disabled: p === '...' }"
                  >
                    <button v-if="p !== '...'" class="page-link" @click="pastPage = Number(p)">
                      {{ p }}
                    </button>
                    <span v-else class="page-link">...</span>
                  </li>
                  <li class="page-item" :class="{ disabled: pastPage === pastTotalPages }">
                    <button class="page-link" @click="pastPage++">›</button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>

        <!-- Next seminar (always open) -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              :class="{ collapsed: !openNext }"
              type="button"
              @click="toggle('next')"
            >
              Next seminar
            </button>
          </h2>
          <div class="accordion-collapse" :class="openNext ? 'collapse show' : 'collapse'">
            <div class="accordion-body">
              <div v-if="loading" class="d-flex flex-column gap-2">
                <div class="text-muted lead">Retrieving data...</div>
              </div>
              <template v-else>
                <ScheduleSession
                  v-if="nextSession"
                  :session_number="nextSession.session_number"
                  :date="nextSession.date"
                  :time="nextSession.time"
                  :venue="nextSession.venue"
                  :topic="nextSession.topic"
                  :presenter="nextSession.presenter"
                  :paper_authors="nextSession.paper_authors"
                  :paper_title="nextSession.paper_title"
                  :paper_venue="nextSession.paper_venue"
                  :paper_year="nextSession.paper_year"
                  :slides_link="nextSession.slides_link"
                  :paper_link="nextSession.paper_link"
                  :arxiv_link="nextSession.arxiv_link"
                />
                <p v-else class="text-muted">No upcoming seminar scheduled.</p>
              </template>
            </div>
          </div>
        </div>

        <!-- Scheduled seminars -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              :class="{ collapsed: !openScheduled }"
              type="button"
              @click="toggle('scheduled')"
            >
              Scheduled seminars ({{ scheduledSessions.length }})
            </button>
          </h2>
          <div class="accordion-collapse" :class="openScheduled ? 'collapse show' : 'collapse'">
            <div class="accordion-body">
              <template
                v-for="(session, index) in pagedScheduledSessions"
                :key="'scheduled-' + index"
              >
                <ScheduleSession
                  :session_number="session.session_number"
                  :date="session.date"
                  :time="session.time"
                  :topic="session.topic"
                  :venue="session.venue"
                  :presenter="session.presenter"
                  :paper_authors="session.paper_authors"
                  :paper_title="session.paper_title"
                  :paper_venue="session.paper_venue"
                  :paper_year="session.paper_year"
                  :slides_link="session.slides_link"
                  :paper_link="session.paper_link"
                  :arxiv_link="session.arxiv_link"
                />
              </template>
              <p v-if="!scheduledSessions.length" class="text-muted">
                No further seminars scheduled.
              </p>
              <nav v-if="scheduledTotalPages > 1" class="mt-3">
                <ul class="pagination pagination-sm justify-content-center">
                  <li class="page-item" :class="{ disabled: scheduledPage === 1 }">
                    <button class="page-link" @click="scheduledPage--">‹</button>
                  </li>
                  <li
                    v-for="p in scheduledTotalPages"
                    :key="p"
                    class="page-item"
                    :class="{ active: scheduledPage === p }"
                  >
                    <button class="page-link" @click="scheduledPage = p">{{ p }}</button>
                  </li>
                  <li
                    class="page-item"
                    :class="{ disabled: scheduledPage === scheduledTotalPages }"
                  >
                    <button class="page-link" @click="scheduledPage++">›</button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Papa from 'papaparse'

const loading = ref(true)
const openPast = ref(false)
const openNext = ref(true)
const openScheduled = ref(false)

const PAGE_SIZE = 4
const pastPage = ref(1)
const scheduledPage = ref(1)

const toggle = (panel: 'past' | 'next' | 'scheduled') => {
  openPast.value = panel === 'past' ? !openPast.value : false
  openNext.value = panel === 'next' ? !openNext.value : false
  openScheduled.value = panel === 'scheduled' ? !openScheduled.value : false
}

interface Session {
  session_number: number
  date: string
  time: string | null
  venue: string | null
  topic: string | null
  presenter: string | null
  paper_authors: string | null
  paper_title: string | null
  paper_venue: string | null
  paper_year: string | null
  slides_link: string | null
  paper_link: string | null
  arxiv_link: string | null
}

const sessions = ref<Session[]>([])

const now = new Date()
now.setHours(now.getHours() - 2)

const pastSessions = computed(() => sessions.value.filter((s) => new Date(s.date) < now))

const nextSession = computed(() => sessions.value.find((s) => new Date(s.date) >= now) ?? null)

const scheduledSessions = computed(() =>
  sessions.value.filter((s) => new Date(s.date) >= now && s !== nextSession.value),
)

const pastTotalPages = computed(() => Math.ceil(pastSessions.value.length / PAGE_SIZE))
const scheduledTotalPages = computed(() => Math.ceil(scheduledSessions.value.length / PAGE_SIZE))

const pagedPastSessions = computed(() => {
  const start = (pastPage.value - 1) * PAGE_SIZE
  return pastSessions.value.slice(start, start + PAGE_SIZE)
})

const pagedScheduledSessions = computed(() => {
  const start = (scheduledPage.value - 1) * PAGE_SIZE
  return scheduledSessions.value.slice(start, start + PAGE_SIZE)
})

const or = (val: string) => val?.trim() || null

const visiblePastPages = computed(() => {
  const total = pastTotalPages.value
  const current = pastPage.value
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  if (current <= 3) {
    return [1, 2, 3, 4, '...', total]
  }

  if (current >= total - 2) {
    return [1, '...', total - 3, total - 2, total - 1, total]
  }

  return [1, '...', current - 1, current, current + 1, '...', total]
})

const visibleScheduledPages = computed(() => {
  const total = scheduledTotalPages.value
  const current = scheduledPage.value

  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  if (current <= 3) {
    return [1, 2, 3, 4, '...', total]
  }

  if (current >= total - 2) {
    return [1, '...', total - 3, total - 2, total - 1, total]
  }

  return [1, '...', current - 1, current, current + 1, '...', total]
})

onMounted(async () => {
  const response = await fetch(
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vT3L0usWznwB4gJtVAOtQnQx_X7mOrTZ0DInv_8PNg45xvO60FExh42rYybwwKNdebYoFDcWtS4c4gN/pub?gid=1236605236&single=true&output=csv',
  )
  const text = await response.text()
  const { data: parsed } = Papa.parse(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim(),
  })

  const mapped = (parsed as any[]).map((row, index) => {
    const date = or(row.date) ?? ''
    const isPast = new Date(date) < now
    return {
      session_number: index + 1,
      date,
      time: or(row.time) ?? (isPast ? 'unknown' : 'TBA'),
      venue: or(row.venue) ?? (isPast ? 'unknown' : 'TBA'),
      topic: or(row.topic),
      presenter: or(row.presenter) ?? (isPast ? 'unknown' : 'TBA'),
      paper_authors: or(row.paper_authors),
      paper_title: or(row.paper_title) ?? 'Paper title TBA',
      paper_venue: or(row.paper_venue),
      paper_year: or(row.paper_year),
      slides_link: or(row.slides_link),
      paper_link: or(row.paper_link),
      arxiv_link: or(row.arxiv_link),
    }
  })

  const past = mapped
    .filter((s) => new Date(s.date) < now)
    .sort((a, b) => b.date.localeCompare(a.date))
  const future = mapped
    .filter((s) => new Date(s.date) >= now)
    .sort((a, b) => a.date.localeCompare(b.date))

  sessions.value = [...past, ...future]
  loading.value = false
})
</script>
```
