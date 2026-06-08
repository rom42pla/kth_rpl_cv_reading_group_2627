<template>
  <div class="container">
    <div class="col-md-8 mx-auto">
      <h1 class="mb-4">Schedule</h1>
      <p>
        Note that the schedule after the winter break is tentative and subject to change. <br />
        More sessions will be scheduled soon.
      </p>
      <template v-for="(session, index) in sessions" :key="index">
        <!-- Render break message -->
        <div v-if="session.type === 'break'" class="text-center my-4 text-muted">
          <hr />
          <span class="h2">
            {{ session.season === 'summer' ? '☀️ Summer break' : '❄️ Winter break' }}
          </span>
          <hr />
        </div>

        <!-- Render ScheduleSession -->
        <ScheduleSession
          v-else
          :session_number="getSessionNumber(index)"
          :date="session.date"
          :time="session.time"
          :title="session.title"
          :speaker="session.speaker"
          :paper_citation="session.paper_citation"
          :paper_link="session.paper_link"
          :arxiv_link="session.arxiv_link"
          :venue="session.venue || 'venue TBA'"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentSessionNumber = ref(1)

const sessions = ref([
  {
    date: '2026-06-11',
    time: '13:15',
    title: 'A Comprehensive Survey of Continual Learning: Theory, Method and Application',
    speaker: 'Romeo Lanzino',
    paper_citation:
      'L. Wang, X. Zhang, H. Su and J. Zhu, "A Comprehensive Survey of Continual Learning: Theory, Method and Application," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 46, no. 8, pp. 5362-5383, Aug. 2024, doi: 10.1109/TPAMI.2024.3367329.',
    paper_link: 'https://ieeexplore.ieee.org/document/10444954',
    arxiv_link: 'https://arxiv.org/abs/2302.00487',
    venue: 'Teknikringen 14, floor 3, room 304',
  },
  { type: 'break', season: 'summer' },
  { date: '2026-08-18', time: '13:00' },
  { date: '2026-09-01', time: '13:00' },
  { date: '2026-09-15', time: '13:00' },
  { date: '2026-09-29', time: '13:00' },
  { date: '2026-10-13', time: '13:00' },
  { date: '2026-10-27', time: '13:00' },
  { date: '2026-11-10', time: '13:00' },
  { date: '2026-11-24', time: '13:00' },
  { date: '2026-12-08', time: '13:00' },
  { type: 'break', season: 'winter' },
  { date: '2027-01-12', time: '13:00' },
  { date: '2027-01-26', time: '13:00' },
  { date: '2027-02-09', time: '13:00' },
  { date: '2027-02-23', time: '13:00' },
  { date: '2027-03-09', time: '13:00' },
  { date: '2027-03-23', time: '13:00' },
  { date: '2027-04-06', time: '13:00' },
  { date: '2027-04-20', time: '13:00' },
  { date: '2027-05-04', time: '13:00' },
  { date: '2027-05-18', time: '13:00' },
  { date: '2027-06-01', time: '13:00' },
  { date: '2027-06-15', time: '13:00' },
  { date: '2027-06-29', time: '13:00' },
])
const getSessionNumber = (index: number) => {
  // Count only non-break sessions before and including this index
  return sessions.value.slice(0, index + 1).filter((s) => s.type !== 'break').length
}
</script>

<style scoped>
/* Minimal custom overrides */
</style>
