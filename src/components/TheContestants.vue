<template>
  <h1>MUJE {{ year }}</h1>
  <div class="container">
    <div class="row section_buttons">
      <input v-for="(sect, index) in sections"  
        class="bg-warning form-control button btn btn-primary" 
        :key="index" type="button"
        :name="sect" 
        :value="sect" 
        :id="String(index)" 
        @click="update(index)">
    </div>
    <h5>{{ sections[section] }} Contestants</h5>
    <div class="row cards">
        <div v-for="(lady, index) in ladies"
        :key="index"
        data-toggle="modal" 
        data-target="#viewContestantModal" 
        class="card">
          <img class="card-img-top" :src="`./images/${lady['photo']}`" alt="Card image cap">
          <div class="card-body">
            <h5 class="card-title">{{ lady['contestant_no'] }}</h5>
            <p class="card-text">{{ lady['title'] }}</p>
            <!-- Only allow girl to be reated if the section is opened -->
            <input type="button" value="Score" class="btn btn-primary" @click="view(index)" :disabled="is_open(index)">
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
              <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="close" ></button>
            </div>
            <div class=modal-body>
              <SingleContestant :lady="contestant"
                :numbers="get_numbers(section)"
                @scored="score_contestant" />
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

    const year = moment().tz("Jamaica").year() ;

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

    let sections = ["Interview","Swimwear", "Evening Wear", "Top-5 Q&A", "Top-3 Q&A"]; // Section Names
    let fields = ["interview", "swimsuit", "ballroom", "q_and_a", "q_and_a"]; // 
    let section = ref(0);

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

    function is_open(i:number) {
      open.forEach((sect:string) => {
        if (sect == fields[i]) {
          return true;
        }
      })
      return false
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
                open.push(section['section']);
                // set round to the lowest round of all the active sections
                if (Number(section['round']) < round) {
                  round = Number(section['round']);
                }
              } else {
                closed.push(section['section']);
              }
          });
        }
      });
    }

    function update(section:number) {
      set_section(section);
    }

    function set_section(num:number) {
      section.value = num;
      update_ladies(num);
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

    function get_contestants() {
      ladies.value = [];
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

    function get_numbers(index:number) {
      let size = [35, 35, 35, 10, 10];
      let numbers = Array.from({length:size[index]}, (_,i) => ++i);
      return numbers;
    }

    function view(index:number){
        contestant.value = ladies.value[index];
    }

    function score_contestant(score:number) {
      close();
      let formData = new FormData();
      formData.append('interview', String(score));
      formData.append('swimsuit', String(score));
      formData.append('ballroom', String(score));
      formData.append('q_and_a', String(score));
      formData.append('year', String(year));
      formData.append('contestant_no', String(contestant.value['contestant_no']));
      let url:string = `/api/v1/${rounds[section.value]}`;

      fetch(url, {
        headers:{
          Authorization: `bearer ${localStorage['token']}`,
          // "Content-Type": 'multipart/form-data'
        },
        method:"POST",
        body:formData
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

  .section_buttons {
    display:flex;
    flex-direction:row;
    justify-content:space-evenly;
    margin-bottom:30px;
  }

  .button {
    width:fit-content;
    border:none;
    box-shadow: 2px 2px gray;
  }
  .button:hover {
    color:blue;
    box-shadow: 1px 1px gray;
  }
</style>