<template>
    <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title" id="modalLabel"> Add New Contestant </h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" ></button>
      </div>
      <div class="modal-body">
          <form id="newContestantForm" action="" method="post" enctype="multipart/form-data">
              <div class="form-group">
                  <div class="form-group contestant">
                    <h5> Contestant Information </h5>
                    <div class="section1">
                      <div class="form-group">
                        <label for="year"> Year </label>
                        <select 
                        :v-model="year"
                          name="year" 
                          id="year" 
                          class="form-control">
                            <option></option>
                            <option 
                                v-for="(yr, index) in years" 
                                :value="yr" 
                                :key='index' > {{ yr }}
                            </option>
                        </select>
                      </div>
                      <div class="form-group">
                        <label for="contestant_no"> Contestant No. </label>
                        <select name="contestant_no" id="contestant_no" class="form-control">
                            <option 
                                v-for="(number, index) in numbers_15" 
                                :value="number" 
                                :key='index' > {{ number }}
                            </option>
                        </select>
                      </div>
                    </div>

                    <div class="section2">
                      <div class="form-group">
                        <label for="title"> Sponsor </label><span><small>(i.e. Company Name)</small></span>
                        <input class="form-control" type="text" name="title" id="title">
                      </div>
                      
                      <div class="form-group">
                        <label for="name"> Full Name </label>
                        <input class="form-control" type="text" name="name" id="name">
                      </div>
                    </div>


                    <div class="form-group">
                      <label for="photo"> Photo </label>
                      <input @change="loadPreview" accept="image/*" type="file" name="photo" id="photo" class="form-control">
                      <section class="preview">
                        <div v-if="preview" class="preview">
                          <img id="preview-image" :src="`${photo}`" alt="image preview"/>
                        </div>
                      </section>
                    </div>

                  </div>
              </div>
          </form>
      </div>

      <div class="modal-footer">
          <button type="button" 
            v-on:click="submit" 
            class="btn btn-primary">
              <img id="save" src="../components/icons/save.png" alt="save" class="text-white" />  
              Save
          </button>
          <button 
            type="button" 
            class="btn btn-info"
            @click="clear" >
              Clear
          </button>
          <button 
            type="button" 
            class="btn btn-secondary"
            @click="close" 
            data-dismiss="modal">
              Close
          </button>
      </div>
    </div>
</template>

<script setup lang='ts'>

    import { ref } from 'vue';
    import Swal from 'sweetalert2';
    import { clear, close, confirm_submit, confirmed, failed } from '../js/form-controls';

    let numbers_15 = Array.from({ length: 15 }, (_, i) => i + 1);
    let years = [2023];
    let year = ref(2023);

    let photo = ref("");
    let preview = ref(false);


    function loadPreview() {
      // @ts-ignore
      photo.value = URL.createObjectURL(document.querySelector('#photo').files[0]);
      preview.value=true;
    }

    function submit() {
        // @ts-ignore
        let form = new FormData($('#newContestantForm')[0]);
        let url = `/api/v1/contestants/${year.value}`;

        fetch(url, {
          headers:{
            Authorization: `bearer ${localStorage['token']}`
          },
          method:'POST',
          body:form
        })
        .then((response)=>response.json())
        .then((data)=>{
          if (data.status=="success"){
            // notify of success
            close();
            $('img#preview-image')[0].src="";
            confirmed('Contestant has been added successfully!');
          } else {
            // notify of error
            failed('Oops! \n\n'+data.message);
          }
        })
    }

</script>

<style scoped>

  .section1,.section2 {
    display:flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .section2 div, .section2 div {
    width:50%;
  }

  .section2 {
    margin-top:20px;
    margin-bottom:20px;
  }

  input[type="text"] {
    width:90%;
  }

  #preview-image {
    width:100%;
  }

  .modal-header {
    background-color:rgb(89, 89, 152);
    color:aliceblue;
  }
  input[type="file"] {
    width: 110px;
    border: none;
    background-color: none;
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

  .new_post {
    position:sticky;
    top:70px;
    float:right;
    margin-right:20px;
    width:250px;
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