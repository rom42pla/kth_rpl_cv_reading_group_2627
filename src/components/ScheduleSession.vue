<template>
  <div class="py-3 border-bottom">
    <div class="container">
      <div class="row">
        <div class="col col-12 col-lg-4 text-muted small mb-1">📅 {{ formattedDate }}</div>
        <div class="col col-12 col-lg-2 text-muted small mb-1">🕐 {{ time }}</div>
        <div class="col col-12 col-lg-6 text-muted small mb-1">📍 {{ venue }}</div>
      </div>
      <!-- paper details -->
      <div class="row">
        <div class="col lead mb-1">
          {{ paper_title }}
        </div>
      </div>
      <div class="row">
        <div v-if="paper_authors" class="col col-12 col-lg-6 text-muted small mb-1">
          {{ paper_authors }}
        </div>
        <div v-if="paper_venue" class="col col-12 col-lg-4 text-muted small mb-1">
          {{ paper_venue }}, {{ paper_year }}
        </div>
      </div>
      <!-- presenter and topic -->
      <div class="row">
        <div v-if="presenter" class="col col-12 col-lg-6 mb-1 small">
          Presented by {{ presenter }}
        </div>
        <div v-if="topic" class="col col-12 col-lg-6 mb-1 small">{{ topic }} topic</div>
      </div>
    </div>
    <!-- buttons -->
    <div class="row mx-0">
      <div class="col mb-1">
        <a v-if="paper_link" :href="paper_link" class="btn btn-sm btn-primary me-2" target="_blank">
          Read paper
        </a>
        <a
          v-if="arxiv_link"
          :href="arxiv_link"
          class="btn btn-sm me-2"
          style="background-color: #b31b1b; color: white"
          target="_blank"
        >
          Read paper on arXiv
        </a>
        <a
          v-if="slides_link"
          :href="slides_link"
          class="btn btn-sm btn-secondary me-2"
          target="_blank"
        >
          Read slides
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  date: String,
  time: { type: String, default: 'time TBA' },
  paper_title: { type: String, default: 'Title TBA' },
  venue: { type: String, default: 'venue TBA' },
  topic: { type: String, default: null },
  presenter: { type: String, default: null },
  paper_authors: { type: String, default: null },
  paper_citation: { type: String, default: null },
  paper_link: { type: String, default: null },
  paper_venue: { type: String, default: null },
  paper_year: { type: String, default: null },
  slides_link: { type: String, default: null },
  arxiv_link: { type: String, default: null },
  session_number: { type: Number, default: null },
})

const formattedDate = computed(() => {
  if (!props.date) return 'Date TBA'
  return new Date(props.date).toLocaleDateString('en-GB', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})
</script>
