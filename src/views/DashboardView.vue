<script setup lang="ts">
  import TheContestants from '../components/TheContestants.vue';

  let id:number  = Number(localStorage['id']);
  let type:number  = Number(localStorage['role']);

</script>

<template>
  <main>
    <div class="container-fluid">

      <div class="component">
        <TheContestants id="ladies"/>   
      </div>

    </div>
  </main>
</template>

<style scoped>

  .component {
    width:100%;
  }

</style>