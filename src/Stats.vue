<template>
  <div class="container">
    <div class="col-md-8 mx-auto">
      <h1 class="mb-4">Registration stats</h1>
      <div class="row justify-content-center g-4">
        <!-- Role pie chart -->
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Role</h5>
              <Pie v-if="roleData" :data="roleData" :options="chartOptions" />
            </div>
          </div>
        </div>
        <!-- Department pie chart -->
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Department</h5>
              <Pie v-if="departmentData" :data="departmentData" :options="chartOptions" />
            </div>
          </div>
        </div>
        <!-- Steering committee pie chart -->
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Will join Steering Committee</h5>
              <Pie v-if="steeringData" :data="steeringData" :options="chartOptions" />
            </div>
          </div>
        </div>
        <!-- Fields of study bar chart -->
        <div class="col-12 col-md-8 col-lg-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Fields of study</h5>
              <Bar v-if="fieldData" :data="fieldData" :options="barOptions" />
            </div>
          </div>
        </div>
        <!-- Suggestions bar chart -->
        <div class="col-12 col-md-8 col-lg-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Possible new topics suggestions</h5>
              <Bar v-if="suggestionData" :data="suggestionData" :options="barOptions" />
            </div>
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
const departmentData = ref(null)
const steeringData = ref(null)
const fieldData = ref(null)
const suggestionData = ref(null)

const PIE_COLORS = [
  '#000061',
  '#f28e2b',
  '#e15759',
  '#76b7b2',
  '#59a14f',
  '#edc948',
  '#af7aa1',
  '#ff9da7',
  '#9c755f',
  '#bab0ac',
]

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

function makePieData(data, field) {
  const counts = data.reduce((acc, row) => {
    const val = row[field] || 'Unknown'
    acc[val] = (acc[val] || 0) + 1
    return acc
  }, {})
  return {
    labels: Object.keys(counts),
    datasets: [
      {
        data: Object.values(counts),
        backgroundColor: PIE_COLORS,
      },
    ],
  }
}

onMounted(async () => {
  const response = await fetch(import.meta.env.BASE_URL + 'forms/registration.csv')
  const text = await response.text()
  const { data } = Papa.parse(text, { header: true, skipEmptyLines: true })

  roleData.value = makePieData(data, 'role')
  departmentData.value = makePieData(data, 'department')
  steeringData.value = makePieData(data, 'will_steering_committee')

  // Field bar chart
  const fieldCounts = data.reduce((acc, row) => {
    const fields = (row['field'] || '').split(',')
    fields.forEach((f) => {
      const normalized = f.trim().toLowerCase().replace(/\s+/g, ' ')
      if (normalized) acc[normalized] = (acc[normalized] || 0) + 1
    })
    return acc
  }, {})
  const sorted = Object.entries(fieldCounts).sort((a, b) => b[1] - a[1])
  fieldData.value = {
    labels: sorted.map(([k]) => k),
    datasets: [{ data: sorted.map(([, v]) => v), backgroundColor: '#000061' }],
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
    datasets: [{ data: sortedSuggestions.map(([, v]) => v), backgroundColor: '#000061' }],
  }
})
</script>
