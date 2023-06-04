<template>
  <h1>MUJE 2023</h1>
  <div class="container">
    <div class="row form-group">
      <h5>Select Section</h5>
      <div v-for="(sect, index) in sections"  
      :key="index">
        <input type="button"
        :name="sect" 
        :value="sect" 
        :id="String(index)" 
        class="form-control col-md-2 col-sm-6 btn btn-primary" 
        @click="set_section(index)">
      </div>
    </div>
    <div class="row cards">
      <h5>Contestants</h5>
        <div v-for="(lady, index) in ladies"
        :key="index"
        @click="view(index)" 
        data-toggle="modal" 
        data-target="#viewContestantModal" class="card">
          <img class="card-img-top" :src="lady['photo']" alt="Card image cap">
          <div class="card-body">
            <h5 class="card-title">{{ lady['contestant_no'] }}</h5>
            <p class="card-text">{{ lady['title'] }}</p>
            <a href="#" class="btn btn-primary">Score {{ section }}</a>
          </div>
        </div>
    </div>
  </div>
    
    <div class="modal-forms">
      <!-- View/Vote Contestant Modal -->
      <div id="viewContestantModal" class="modal fade">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class='modal-header'>
              <h5> Contestant No. {{ contestant['contestant_no'] }} </h5>
              <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="close" >x</button>
            </div>
            <div class=modal-body>
              <SingleContestant :lady="contestant" 
                :section="sections[section]"
                @close="close" />
            </div>
          </div>
        </div>
      </div>
    </div> 

</template>


<script setup lang="ts">
    import moment from 'moment-timezone';
    import { ref } from 'vue';
    import SingleContestant from '../components/SingleContestant.vue';
    import { clear, close, confirm_submit } from '../js/form-controls';

    const year = moment().tz("Jamaica").year();
    let contestant = ref({
      'year':0,
      'title':"",
      'contestant_no':0,
      'name':'',
      'photo':"",
      'muje_region':""
    });

    let rounds:string[] = [
      "prelim/interview",
      "prelim/swimsuit", 
      "prelim/ballroom", 
      "top5", 
      "top3"
    ]

    let sections = ["Interview","Swimwear", "Evening Wear", "Top-5 Q&A", "Top-3 Q&A"]; 
    let fields = ["interview", "swimsuit", "ballroom", "q_and_a", "q_and_a"];
    let section = ref(0);

    function set_section(num:number) {
      section.value = num;
    }

    function update_contestants() {
      //
    }

    function get_numbers(index:number) {
      let size = [50, 25, 25, 100, 100];
      let numbers = Array.from({length:size[index]}, (_,i) => ++i);
      return numbers;
    }

    const prop = defineProps(['ladies']);

    function view(index:number){
        contestant.value = prop.ladies[index];
    }

    function score(round:number, section:number, score:number) {
      let form = {
        "interview":score,
        "swimsuit":score,
        "ballroom":score,
        "q_and_a":score,
        "year":year,
        "contestant_no":contestant.value['contestant_no'],
      };
      let url:string = `/api/v1/${rounds[section]}`;

      fetch(url, {
        headers:{
          Authorization: `bearer ${localStorage['token']}`
        },
        method:"POST",
        body:JSON.stringify()
      })

    }

</script>


<style scoped>

  .cards {
    display:grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
    grid-gap: 5px;
    padding: 7px;
  }
</style>