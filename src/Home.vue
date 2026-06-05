<template>
  <div class="container py-5">
    <!-- Hero -->
    <div class="row mb-5">
      <div class="col-md-8 mx-auto text-center">
        <h1 class="display-5 fw-bold">Computer Vision<br />Reading Group</h1>
        <p class="lead">2026/27</p>
        <p class="text-muted mb-1">Robotics, Perception & Learning (RPL) Department @ KTH</p>
      </div>
    </div>

    <!-- Format -->
    <div class="row mb-5">
      <div class="col-md-8 mx-auto">
        <h4 class="mb-3">Format</h4>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            Bi-weekly sessions, usually Tuesdays at 13:00 but always keep an eye on the
            <RouterLink to="/schedule">schedule</RouterLink>
          </li>
          <li class="list-group-item">One or two papers per session</li>
          <li class="list-group-item">Rotating presenter, open discussion</li>
          <li class="list-group-item">
            Usually at Fantum but always keep an eye on the
            <RouterLink to="/schedule"> schedule</RouterLink>
          </li>
        </ul>
      </div>
    </div>

    <div class="row mb-3">
      <div class="col-md-8 mx-auto">
        <h4>Organizers</h4>
      </div>
    </div>

    <div class="row g-3 justify-content-center mb-3">
      <div class="col-12 col-lg-3">
        <OrganizerCard name="Romeo Lanzino" role="Coordinator, postdoc" email="lanzino@kth.se" />
      </div>
      <div class="col-12 col-lg-3">
        <OrganizerCard
          name="Chen Ling"
          role="Coordination assistant, PhD student"
          email="chenlin@kth.se"
        />
      </div>
    </div>

    <div class="row g-3 justify-content-center">
      <div class="col-12 col-lg-3">
        <OrganizerCard name="Hossein Azizpour" role="Examiner, faculty" email="azizpour@kth.se" />
      </div>
      <div class="col-12 col-lg-3">
        <OrganizerCard name="Mårten Björkman" role="Faculty" email="celle@kth.se" />
      </div>
      <div class="col-12 col-lg-3">
        <OrganizerCard name="Atsuto Maki" role="Faculty" email="atsuto@kth.se" />
      </div>
    </div>
  </div>
</template>

<script setup></script>
