<script setup lang="ts">
  import TheContestants from '../components/TheContestants.vue';

  let id:number  = Number(localStorage['id']);
  let authorized:boolean  = localStorage['role'] == "admin" || localStorage['role'] == "chief" || localStorage['role'] == "judge";

</script>

<template>
  <main>
    <div class="container-fluid">

      <div v-if="id && authorized" class="component">
        <TheContestants />   
      </div>

    </div>
  </main>
</template>

<style scoped>

  .component {
    width:100%;
  }

</style>