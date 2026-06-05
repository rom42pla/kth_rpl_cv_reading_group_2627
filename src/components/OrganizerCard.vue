<template>
  <div class="card">
    <div class="card-body">
      <h6 class="card-title mb-0">{{ name }}</h6>
      <small class="text-muted">{{ role }}</small
      ><br />
      <small>
        <a :href="'mailto:' + email">{{ email }}</a>
      </small>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  role: String,
  email: String,
})
</script>
