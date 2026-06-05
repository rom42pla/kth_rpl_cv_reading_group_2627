<template>
  <div class="container py-5">
    <h2 class="mb-4">Registration stats</h2>

    <div class="row justify-content-center g-4">
      <!-- Pie chart -->
      <div class="col-12 col-md-8 col-lg-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-center">Role</h5>
            <Pie v-if="roleData" :data="roleData" :options="chartOptions" />
          </div>
        </div>
      </div>

      <!-- Bar chart -->
      <div class="col-12 col-md-8 col-lg-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-center">Fields of study</h5>
            <Bar v-if="fieldData" :data="fieldData" :options="barOptions" />
          </div>
        </div>
      </div>

      <!-- Suggestions bar chart -->
      <div class="col-12 col-md-8 col-lg-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-center">Possible new topics suggestions</h5>
            <Bar v-if="suggestionData" :data="suggestionData" :options="barOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Pie, Bar } from 'vue-chartjs'
import Papa from 'papaparse'

const roleData = ref(null)
const fieldData = ref(null)
const suggestionData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: true,
  indexAxis: 'y',
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      ticks: {
        autoSkip: false,
      },
    },
  },
}

onMounted(async () => {
  const response = await fetch(import.meta.env.BASE_URL + 'forms/registration.csv')
  const text = await response.text()
  const { data } = Papa.parse(text, { header: true, skipEmptyLines: true })

  // Role pie chart
  const roleCounts = data.reduce((acc, row) => {
    const role = row['role'] || 'Unknown'
    acc[role] = (acc[role] || 0) + 1
    return acc
  }, {})

  roleData.value = {
    labels: Object.keys(roleCounts),
    datasets: [
      {
        data: Object.values(roleCounts),
        backgroundColor: ['#000061', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948'],
      },
    ],
  }

  // Field bar chart
  const fieldCounts = data.reduce((acc, row) => {
    const fields = (row['field'] || '').split(',')
    fields.forEach((f) => {
      const normalized = f.trim().toLowerCase().replace(/\s+/g, ' ')
      if (normalized) acc[normalized] = (acc[normalized] || 0) + 1
    })
    return acc
  }, {})

  // Sort by frequency descending
  const sorted = Object.entries(fieldCounts).sort((a, b) => b[1] - a[1])

  fieldData.value = {
    labels: sorted.map(([k]) => k),
    datasets: [
      {
        data: sorted.map(([, v]) => v),
        backgroundColor: '#000061',
      },
    ],
  }

  // Suggestions bar chart
  const suggestionCounts = data.reduce((acc, row) => {
    const suggestions = (row['suggestions'] || '').split(',')
    suggestions.forEach((s) => {
      const normalized = s.trim().toLowerCase().replace(/\s+/g, ' ')
      if (normalized) acc[normalized] = (acc[normalized] || 0) + 1
    })
    return acc
  }, {})

  const sortedSuggestions = Object.entries(suggestionCounts).sort((a, b) => b[1] - a[1])

  suggestionData.value = {
    labels: sortedSuggestions.map(([k]) => k),
    datasets: [
      {
        data: sortedSuggestions.map(([, v]) => v),
        backgroundColor: '#000061',
      },
    ],
  }
})
</script>
