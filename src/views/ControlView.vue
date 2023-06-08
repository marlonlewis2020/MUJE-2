<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import UserForm from '../components/UserForm.vue';
    import ContestantForm from '../components/ContestantForm.vue';
    import { clear, close, confirm_submit, BOOTBOX } from '../js/form-controls';
    // import Bootstrap from 'bootstrap-vue';

    let id:number  = Number(localStorage['id']);
    let result_title = ref("");
    let round = ref(Infinity);
    let sections = [];
    let update_table = false;
    let open = [];
    let closed = [];
    let results = ref([]);

    onMounted(()=>{
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
                sections = data.data;
                sections.forEach((section:any) => {
                    if (section['active'] == 1 || section['active']) {
                        open.push(section);
                        // set round to the lowest round of all the active sections
                        if (section.round < round) {
                            round.value = section['round'];
                        }
                    } else {
                        closed.push(section);
                    }
                });
            }
        });
    }

    function close_round_confirm() {
        let text:string = `Are you sure you want to close round ${round}?`;
        let func:string = "close_round";
        let params:[] = [];

        BOOTBOX.confirm(text, func, params);
        update_table = false;
    }

    function open_round_confirm(r:number) {
        let text:string = `Are you sure you want to re-open round ${r}?`;
        let func:string = "open_round";
        let params:number[] = [r];

        BOOTBOX.confirm(text, func, params);
    }

    function close_round() {
        let url = `/api/v1/round/${round}/close`
        // update db
        fetch(url,{
            headers:{
                Authorization: `bearer ${localStorage['token']}`
            },
            method:'POST'
        })
        .then((response)=>response.json())
        .then((data)=>{
          if (data.status=="success"){
            // increment round count by 1, if round <= 3
            round++;
            update_table = false;
            // notify of success
            confirmed(`Round ${round} has been closed.`);
            // update sections
            get_sections()
          } else {
            // notify of error
            failed(data.message);
          }
        })
    }

    function open_round(r:number) {
        let url = `/api/v1/round/${r}/open`
        // update db
        fetch(url,{
            headers:{
                Authorization: `bearer ${localStorage['token']}`
            },
            method:'POST'
        })
        .then((response)=>response.json())
        .then((data)=>{
          if (data.status=="success"){
            // notify of success
            confirmed(`Round ${r} has been re-opened.`);
            // increment round
            get_sections();
          } else {
            // notify of error
            failed("Oops... \n\n"+data.message);
          }
        })
    }

    // get top 10
    function best_in_swimsuit() {
        let url = '/api/v1/prelims/best_swimsuit';
        update_results(url);
        result_title.value = "Best In Swim Wear";
    }

    // get top 10
    function best_in_evening() {
        let url = '/api/v1/prelims/best_evening';
        update_results(url);
        result_title.value = "Best In Evening Gown";
    }

    // get top 10
    function get_top_10() {
        let url = '/api/v1/prelims/top10';
        update_results(url);
        result_title.value = "Top 10 Finalists";
    }

    // get top 5
    function get_top_5() {
        let url = '/api/v1/prelims/top5';
        update_results(url);
        result_title.value = "Top 5 Finalists";
    }

    // get top 3
    function get_top_3() {
        let url = '/api/v1/top5/top3';
        update_results(url);
        result_title.value = "Top 3 Finalists";
    }

    // get winners
    function get_final_scores() {
        let url = "/api/v1/top3/scores";
        update_results(url);
        result_title.value = "Top 3 Final Scores";
    }

    function update_results(url:string) {
        results.value = [];
        result_title.value = "";
        fetch(url, {
            headers: {
                Authorization: `bearer ${localStorage['token']}`
            },
            method:"GET"
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.status=="success") {
                update_table = true;
                results.value = data.data;
            }
        });
    }

</script>
<template> 

    <!-- ANALYTICS -->
    <div class="container ">
        <!-- Show sections -->
        <div class="row control_panel">
            <div class="controls sections">

                <section class="switches section">
                    <!-- Show section options -->
                    <div class="switch_buttons">
                        <div class="buttons">
                            <!-- close round -->
                            <section class="rounds prelims">
                                <button class="button btn btn-danger" @click="close_round_confirm">Close PrelimsVoting</button>
                                <button class="button btn btn-warning"><small>Open Prelims Voting </small></button>
                            </section>
                            
                            <!-- close round -->
                            <section class="rounds top5">
                                <button class="button btn btn-danger"> Close Top 5 Voting </button>
                                <button class="button btn btn-warning"><small> Open Top 5 Voting</small></button>
                            </section>
                            
                            <!-- close round -->
                            <section class="rounds top3">
                                <button class="button btn btn-danger"> Close Top 3 Voting </button>
                                <button class="button btn btn-warning"><small> Open Top 3 Voting</small></button>
                            </section>
                        </div>
                    </div>
                </section>

                <section class="table_results">
                    <!-- Show Results -->
                    <!-- Show the results from the scoring buttons in each round. Updated by the buttons above -->
                    <h5> {{ result_title }} </h5>
                    <div class="results">
                        <table class="table">
                            <thead class="table-stripe">
                                <th v-if="result_title == 'Top 3 Final Scores'">Position</th>
                                <th>Contestant No.</th>
                                <th>Name</th>
                                <th>Title</th>
                                <th>Score</th>
                            </thead>
                            <tbody>
                                <tr v-for="(contestant, index) in results"
                                    :key="index">
                                    <td v-if="result_title == 'Top 3 Final Scores'">{{ index+1 }}</td>
                                    <td >{{ contestant['contestant_no'] }}</td>
                                    <td >{{ contestant['name'] }}</td>
                                    <td >{{ contestant['title'] }}</td>
                                    <td >{{ contestant['score'] }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                </section>

                <section class="results section">
                    <div class="res_buttons">
                        <div class="buttons">
                            <!-- Get Best in Swim Wear -->
                            <button class="button btn btn-primary" @click="best_in_swimsuit" :disabled="round<2">Best in Swim Wear</button>
                            <!-- Get Best in Evening Gown -->
                            <button class="button btn btn-primary" @click="best_in_evening" :disabled="round<2">Best in Evening Gown</button>
                            
                            <!-- Get Top 10 -->
                            <button class="button btn btn-primary" @click="get_top_10" :disabled="round<2">Get Top 10</button>
                            <!-- Get Top 5 -->
                            <button class="button btn btn-primary" @click="get_top_5" :disabled="round<2">Get Top 5</button>
                            <!-- Get Top 3 -->
                            <button class="button btn btn-primary" @click="get_top_3" :disabled="round<3"> Get Top 3 </button>
                            <!-- Get Winner -->
                            <button class="button btn btn-primary" @click="get_final_scores" :disabled="round<3"> Get Final Scores </button>
                        </div>
                    </div>
                </section>
            </div>
        </div>

        <div class="add_buttons row text-center">
            <section class="adds section col-sm-6">
                <button type="button" 
                    value="Add Judge"
                    class="admin text-center btn btn-primary" 
                    data-toggle="modal" 
                    data-target="#addJudgeModal">
                    Add Judge
                </button>
            </section>
            <section class="adds section col-sm-6">
                <button type="button" 
                    value="Add Judge"
                    class="admin text-center btn btn-primary" 
                    data-toggle="modal" 
                    data-target="#addContestantModal">
                    Add Contestant
                </button>
            </section>
        </div>

        <div class="row">

        </div>

    </div>


    <!-- MODALS -->
    <div id="addJudgeModal" class="modal fade">
        <div class="modal-dialog">
            <UserForm @close="close" />
        </div>
    </div>
    <div id="addContestantModal" class="modal fade">
        <div class="modal-dialog">
            <ContestantForm @close="close" />
        </div>
    </div>
    
</template>

<style>

    .buttons {
        position:fixed;
        float:left;
        margin-right:20px;
        width:120px;
    }

    .rounds {
        margin-bottom:20px;
    }

    .controls {
        display:grid;
        grid-template-columns: 1fr 4fr 1fr;
    }

    .control {
        margin-top:5px;
    }

    .add_buttons {
        display: flex;
        flex-direction: row;
        justify-content:center;

    }

    .button {
        margin-top: 10px;
    }

    .adds {
        width:fit-content;
        margin-right:10px;
        bottom:5px;
    }

</style>