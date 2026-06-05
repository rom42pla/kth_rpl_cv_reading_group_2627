<template>
  <div class="card mb-3">
    <div class="card-body">
      <h6 class="text-muted">{{ formattedDate }} · {{ time }}</h6>
      <h5 class="card-title">{{ title }}</h5>
      <p class="card-text"><b>Speaker</b> · {{ speaker }}</p>
      <p v-if="paper_citation" class="card-text text-muted" style="font-size: 0.8rem">
        <em>{{ paper_citation }}</em>
      </p>
      <a v-if="paper_link" :href="paper_link" class="btn btn-primary" target="_blank">Read paper</a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  date: String,
  time: String,
  title: { type: String, default: 'TBA' },
  speaker: { type: String, default: 'TBA' },
  paper_citation: { type: String, default: null },
  paper_link: { type: String, default: null },
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
