<template>
  <h1>MUJE {{ year }}</h1>
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
        @click="update(index)">
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
                @set_score="score_contestant"
                @close="close" />
            </div>
          </div>
        </div>
      </div>
    </div> 

</template>


<script setup lang="ts">
    import moment from 'moment-timezone';
    import { ref, onMounted } from 'vue';
    import SingleContestant from '../components/SingleContestant.vue';
    import { clear, close, confirm_submit } from '../js/form-controls';

    const prop = defineProps(['ladies']);

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
    let section = 0;

    let round = Infinity;

    let open:any[] = [];
    let closed:any[] = [];

    let ladies = ref([]);
    let ladies_url:string[] = [`/api/v1/contestants/${year}`, '/api/v1/prelims/top5', '/api/v1/top5/top3'];
    
    onMounted(() => {
      get_sections();
      get_contestants();
    });

    let url_round = 0;

    function get_contestants() {
      fetch(ladies_url[url_round], {headers:{
        Authorization: `bearer ${localStorage['token']}`
      }})
      .then((result) => result.json())
      .then((data) => {
        if (data.status=="success") {
          ladies.value = data.data;
        }
      });
    }

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

    function set_section(num:number) {
      section = num;
      update_ladies(num);
    }

    function update(section:number) {
      set_section(section);
    }

    function update_ladies(section_num:number) {
      if (section_num <3) {
        url_round = 0;
      } else if (section_num == 3) {
        url_round = 1;
      } else {
        url_round = 2;
      }
      get_contestants();
    }

    function get_numbers(index:number) {
      let size = [50, 25, 25, 100, 100];
      let numbers = Array.from({length:size[index]}, (_,i) => ++i);
      return numbers;
    }

    function view(index:number){
        contestant.value = prop.ladies[index];
    }

    function score_contestant(score:number) {
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
        body:JSON.stringify(form)
      });

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