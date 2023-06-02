<template>
    <div class="table">
        <h1>Orders</h1>
        <div v-for="(contestant, index) in ladies"
        :key="index"
        @click="view(index)" 
        data-toggle="modal" 
        data-target="#viewordermodal" class="card">
        <img class="card-img-top" :src="contestant['photo']" alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">{{ contestant['contestant_no'] }}</h5>
          <h6 class="card-title">{{ contestant['name'] }}</h6>
          <p class="card-text">{{ contestant['title'] }}</p>
          <a href="#" class="btn btn-primary">Score {{ section }}</a>
        </div>
        </div>
    </div>
    
    <div class="modal-forms">
      <!-- Add Order Modal -->
      <div id="viewordermodal" class="modal fade">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class='modal-header'>
              <h5> View Order </h5>
              <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="close" >x</button>
            </div>
            <div class=modal-body>
              <SingleContestant :lady="lady" 
                @close="close" />
            </div>
          </div>
        </div>
      </div>
    </div> 

</template>


<script setup lang="ts">
    import { ref } from 'vue';
    import moment from 'moment-timezone';
    import SingleContestant from '../components/SingleContestant.vue';

    let lady = ref({});
    let section = "";

    const prop = defineProps(['ladies']);
    const emit = defineEmits<{
        (event:'view', id:number): void;
        (event:'score', id:number, status:string): void;
        (event:'close'): void;
    }>();

    function view(index:number){
        lady.value = prop.ladies[index];
    }

    function close() {
      $("[data-dismiss=modal]").trigger("click");
    }

    function close_section(section) {
      // 
    }
</script>


<style scoped>

  .modal-header {
      background-color:rgb(89, 89, 152);
      color:aliceblue;
  }

  .btn-close {
      border-width: 0;
      border-color: rgb(182, 98, 98);
      border-radius: 5px;
      background-color: rgb(182, 98, 98);
      color: rgb(64, 64, 64);
      font-weight: 600;
      font-family: monospace;
      margin-top:2px;
      margin-right:2px
  }

  input[type="file"] {
    width: 110px;
    border: none;
    background-color: none;
  }

  .active {
    margin-top:6px;
  }

  li:hover{
    cursor:pointer;
  }

  .action_button {
    width:75px;
    margin-bottom:10px;
  }

  .table {
    width:fit-content;
  }

  thead {
    background-color:rgb(89, 89, 152);
    color:aliceblue;
  }

  .btn-close {
    border-width: 0;
    border-color: rgb(182, 98, 98);
    border-radius: 5px;
    background-color: rgb(182, 98, 98);
    color: rgb(64, 64, 64);
    font-weight: 600;
    font-family: monospace;
    margin-top:2px;
    margin-right:2px
  }

  .btn-close:hover {
    font-weight:800;
    border-color: brown;
    background-color: red;
    color:white;
    box-shadow: 1px 1px 3px black;
  }

  #save {
    width: 16px;
    margin-right:6px;
    margin-bottom:4px;
  }
</style>