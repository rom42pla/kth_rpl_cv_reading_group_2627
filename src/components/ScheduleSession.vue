<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="text-muted">Session #{{ session_number }}</h5>
      <h6 class="text-muted">{{ formattedDate }}, {{ time }} @ {{ venue }}</h6>
      <h5 class="card-title">{{ title }}</h5>
      <p v-if="paper_citation" class="card-text text-muted" style="font-size: 0.8rem">
        <em>{{ paper_citation }}</em>
      </p>
      <a v-if="paper_link" :href="paper_link" class="btn btn-primary me-2" target="_blank"
        >Read paper</a
      >
      <a
        v-if="arxiv_link"
        :href="arxiv_link"
        class="btn btn-danger"
        style="background-color: #b31b1b; color: white"
        target="_blank"
        >Read paper on arXiv</a
      >
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  date: String,
  time: String,
  title: { type: String, default: 'Title TBA' },
  venue: { type: String, default: 'venue TBA' },
  paper_citation: { type: String, default: null },
  paper_link: { type: String, default: null },
  arxiv_link: { type: String, default: null },
  session_number: { type: Number, default: null },
})

const formattedDate = computed(() => {
  return new Date(props.date).toLocaleDateString('en-GB', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})
</script>
