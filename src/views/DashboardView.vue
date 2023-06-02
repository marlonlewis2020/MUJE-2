<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import TheContestants from '../components/TheContestants.vue';
  import UserForm from '../components/UserForm.vue';
  
  import moment from 'moment';
  moment().tz("America/Los_Angeles").format();
  let id:number  = Number(localStorage['id']);
  
  let ladies = ref([]);
  let year = ref(2023);
  let ladies_url:string = `/api/v1/contestants/${year.value}`;
  let lady = ref({});
  let score = ref(0);

  function score_interview(){
    let url:string = "api/v1/prelim/interview"
    fetch(url, {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        Authorization: `bearer ${localStorage['token']}`
      },
      body:JSON.stringify({
        'contestant_no': lady.value['contestant_no'],
        'score': score.value,
        'year':year.value
      })
    })
    .then((response)=>response.json())
    .then((result)=>{
      if (result.status =='success') {
        close();
      }
    })
  };
  
  onMounted(() => {

    fetch(ladies_url, {headers:{
      // Authorization: `bearer ${localStorage['token']}`
    }})
    .then((result) => result.json())
    .then((json_result) => {
      if (json_result.status=="success") {
        ladies.value = json_result.data;
      }
    });

  });

  function close() {
    $("[data-dismiss=modal]").trigger("click");
  }

  function viewContestant(num) {
    // 
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
      <div class="buttons">

        <button 
          v-if="id" 
          type="button" 
          value="New Order"
          class="admin text-center btn btn-primary" 
          data-toggle="modal" 
          data-target="#addJudgeModal">
          Add Judge
        </button>

        <button 
          v-if="id" 
          type="button" 
          value="New Customer" 
          class="admin text-center btn btn-dark" 
          data-toggle="modal" 
          data-target="#addContestantModal">
          Add Contestant
        </button>

        <button 
          v-if="id" 
          type="button" 
          value="New Customer" 
          class="admin text-center btn btn-dark" 
          data-toggle="modal" 
          data-target="#scoreContestantModal" hidden>
          Score Contestant
        </button>

        <div class="form-group">
          <br/>
          <form action="" method="POST">
            <label for="delivery_time"><small><strong>Year</strong></small></label>
            <select v-model="year" name="delivery_time" id="delivery_time" cols="30" rows="2" class="form-control av_period" maxlength="75" required>
              <option value=""></option>
              <option value="2023" selected>2023</option>
            </select>
            <button type="button" 
              @click="get_contestants"
              id="contestants_update" 
              class="btn-success" 
              style="margin:5px 30px;border-radius:5px;">Check</button>
          </form>
        </div>
        <br/>
      </div>

      <div class="row">
        <div class="dashboard-tables">

          <div class="row row-component">
            <TheContestants id="ladies" 
            v-if="ladies.length"
            :ladies="ladies"
            @score="score"
            @view="viewContestant" 
            @close="close"/>   
          </div>
    
          <!-- Add Judge Modal -->
          <div id="addtruckmodal" class="modal fade">
            <div class="modal-dialog">
                <UserForm @close="close" />
            </div>
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

  .buttons {
    position:fixed;
    float:left;
    margin-right:20px;
    width:120px;
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