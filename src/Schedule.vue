<template>
  <div class="container">
    <div class="col-md-8 mx-auto">
      <h1 class="mb-4">Schedule</h1>
      <p>
        Note that the schedule after the winter break is tentative and subject to change. <br />
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
              <template v-for="(session, index) in pastSessions" :key="'past-' + index">
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
              <template v-for="(session, index) in scheduledSessions" :key="'scheduled-' + index">
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

const openPast = ref(false)
const openNext = ref(true)
const openScheduled = ref(false)

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

const today = new Date()
today.setHours(0, 0, 0, 0)

const pastSessions = computed(() => sessions.value.filter((s) => new Date(s.date) < today))

const nextSession = computed(() => sessions.value.find((s) => new Date(s.date) >= today) ?? null)

const scheduledSessions = computed(() =>
  sessions.value.filter((s) => new Date(s.date) >= today && s !== nextSession.value),
)

const or = (val: string) => val?.trim() || null

onMounted(async () => {
  const response = await fetch(import.meta.env.BASE_URL + 'seminars.csv')
  const text = await response.text()
  const { data: parsed } = Papa.parse(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim(),
  })

  sessions.value = (parsed as any[]).map((row, index) => {
    const date = or(row.date) ?? ''
    const isPast = new Date(date) < today
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
})
</script>
