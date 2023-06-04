<script setup lang="ts">
    import { onMounted } from 'vue'
    import UserForm from '../components/UserForm.vue';
    import ContestantForm from '../components/ContestantForm.vue';
    import BOOTBOX from '../js/bootbox';
    // import Bootstrap from 'bootstrap-vue';

    let id:number  = Number(localStorage['id']);
    let round = Infinity;
    let sections = [];
    let update_table = false;
    let open = [];
    let closed = [];
    let results = [];

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
                sections.forEach((section) => {
                    if (section['active'] == 1 || section['active']) {
                        open.push(section);
                        // set round to the lowest round of all the active sections
                        if (section.round < round) {
                            round = section['round'];
                        }
                    } else {
                        closed.push(section);
                    }
                });
            }
        });
    }

    function close() {
        $("[data-dismiss=modal]").trigger("click");
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
    function get_top_10() {
        let url = '/api/v1/prelims/top10';
        update_results(url);
    }
    
    // get top 5
    function get_top_5() {
        let url = '/api/v1/prelims/top5';
        update_results(url);
    }

    // get top 3
    function get_top_3() {
        let url = '/api/v1/top5/top3';
        update_results(url);
    }

    // get winners
    function get_final_scores() {
        let url = "/api/v1/top3/scores";
        update_results(url);
    }

    function update_results(url:string) {
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
                results = data.data;
            }
        });
    }

</script>
<template>

    <div class="sections">
        <section class="section">
            <button type="button" 
                value="Add Judge"
                class="admin text-center btn btn-primary" 
                data-toggle="modal" 
                data-target="#addJudgeModal">
                Add Judge
            </button>
        </section>
        <section class="section">
            <button type="button" 
                value="Add Judge"
                class="admin text-center btn btn-primary" 
                data-toggle="modal" 
                data-target="#addContestantModal">
                Add Contestant
            </button>
        </section>
    </div>

    <!-- ANALYTICS -->
    <div class="control">
        <!-- Show sections -->
        <div class="rounds">
            <h4> Rounds </h4>
            <div class="prelim round sections">
                <h5> Round 1 - Prelims </h5>
                <span v-if="round>1">&nbsp;(CLOSED)&nbsp;</span>
                <span v-if="round==1">&nbsp;(OPEN)&nbsp;</span>
                <section class="interview section">
                    <!-- Show section options -->
                    <div class="options">
                        <div class="option">
                            <!-- close round -->
                            <button v-if="round==1" class="btn btn-warning" @click="close_round_confirm">Close Prelims</button>
                            <button v-else class="btn btn-warning"><small>Re-Open Prelims</small></button>
                            <!-- Get Top 10 -->
                            <button class="btn btn-primary" :disabled="round<2">Get Top 10</button>
                            <!-- Get Top 5 -->
                            <button class="btn btn-primary" :disabled="round<2">Get Top 5</button>
                        </div>
                    </div>
                    
                </section>
                
                <section class="swimsuit section">
                    <!-- Show section options -->
                    <div class="options">
                        <div class="option">
                            
                        </div>
                    </div>
                    
                </section>
                
                <section class="ballroom section">
                    <!-- Show section options -->
                    <div class="options">
                        <div class="option">
                            
                        </div>
                    </div>
                    
                </section>
            </div>
    
            <div class="top5 round sections">
                <h5> Round 2 - Top 5 </h5>
                <span v-if="round==2">&nbsp;(OPEN)&nbsp;</span>
                <span v-else>&nbsp;(CLOSED)&nbsp;</span>
                <section class="q_and_a section">
                    <!-- Show section options -->
                    <div class="options">
                        <div class="option">
                            <!-- close round -->
                            <button v-if="round==2" class="btn btn-warning"> Close Prelims </button>
                            <button v-else class="btn btn-warning"><small> Re-Open Prelims </small></button>
                            <!-- Get Top 3 -->
                            <button class="btn btn-primary" :disabled="round<3"> Get Top 3 </button>
                        </div>
                    </div>
                </section>
            </div>
    
            <div class="top3 round sections">
                <h5> Top 3 Round </h5>
                <span v-if="round==3">&nbsp;(OPEN)&nbsp;</span>
                <span v-else>&nbsp;(CLOSED)&nbsp;</span>
                <section class="section">
                    <!-- Show section options -->
                    <div class="options">
                        <div class="option">
                            <!-- close round -->
                            <button class="btn btn-warning"></button>
                            <!-- Get Final Scores -->
                            <button class="btn btn-primary" :disabled="round<4"></button>
                        </div>
                    </div>
    
                </section>
            </div>
        </div>

        <!-- Show Results -->
        <div v-if="round<Infinity" class="results">
            <!-- Show the results from the scoring buttons in each round. Updated by the buttons above -->
            <h5>Round {{ round }} Results</h5>
            <div class="results">
                <table class="table">
                    <thead>
                        <th></th>
                    </thead>
                    <tbody>
                        <tr v-for="(contestant, index) in results"
                            :key="index">
                            <td>{{ index+1 }}</td>
                            <td >{{ contestant.contestant_no }}</td>
                            <td >{{ contestant.name }}</td>
                            <td >{{ contestant.title }}</td>
                            <td >{{ contestant.score }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

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


</style>