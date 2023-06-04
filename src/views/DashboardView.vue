<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import TheContestants from '../components/TheContestants.vue';
  import moment from 'moment-timezone';

  let id:number  = Number(localStorage['id']);
  
  let year = moment().tz("Jamaica").year();
  let ladies = ref([]);
  let ladies_url:string = `/api/v1/contestants/${year}`;
  let round = Infinity;
  let sections = ["Interview","Swimwear", "Evening Wear", "Top-5 Q&A", "Top-3 Q&A"]; 
  let section = ref(0);

  let open:any[] = [];
  let closed:any[] = [];

  let update_table = false;
  let results = [];

  onMounted(() => {

    fetch(ladies_url, {headers:{
      Authorization: `bearer ${localStorage['token']}`
    }})
    .then((result) => result.json())
    .then((json_result) => {
      if (json_result.status=="success") {
        ladies.value = json_result.data;
      }
    });

    get_sections();

  });

  function get_sections() {
      // get sections that are active
      const url = "/api/v1/sections";
      fetch(url, {
          headers:{
              Authorization: `bearer ${localStorage['token']}`
          }
      })
      .then((response) => response.json())
      .then((data) => {
          if (data.status=="success") {
              // update section status
              let sections = data.data;
              sections.forEach((section:Record<string,number|string>) => {
                  if (section['active'] == 1 || section['active']) {
                      open.push(section);
                      // set round to the lowest round of all the active sections
                      if (Number(section['round']) < round) {
                          round = Number(section['round']);
                      }
                  } else {
                      closed.push(section);
                  }
              });
          }
      });
  }

  function get_contestants() {
      fetch(ladies_url, {headers:{
      // Authorization: `bearer ${localStorage['token']}`
      }})
      .then((result) => result.json())
      .then((json_result) => {
      if (json_result.status=="success") {
          ladies.value = json_result.data;
      }
      });
  }

</script>

<template>
  <main>
    <div class="container-fluid">
      
      <div class="row">
        <div class="dashboard-tables">

          <div class="row row-component">
            <TheContestants id="ladies" 
            v-if="ladies.length"
            :ladies="ladies"/>   
          </div>

        </div> 

      </div>
    </div>
  </main>
</template>

<style scoped>

  .av_trucks {
    max-height: 100px;
    overflow-y: auto;
  }

  #schedule {
    margin-bottom:30px;
  }

  #av_truck_date {
    width:120px;
  }

  .dashboard-tables {
    /* margin-top:30px; */
    margin-left:180px;
    display:flex;
    flex-direction:column;
  }

  .row-component, .placeholder {
    width:100%;
  }

  .placeholder {
    margin-bottom:30px;
    margin-left:180px;
  }

  

  .admin {
    width:100%;
    margin-bottom:6px;
  }

  @media (max-width:900px) {
    .new_post {
      position:absolute;
      justify-content: center;
      width:85%;
      max-width:400px;
      top: 150px;
      left: auto;
      right:auto;
      float:none;
      margin-left:15px;
    }
  }

</style>