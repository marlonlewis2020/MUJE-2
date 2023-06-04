<template>
    <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title" id="modalLabel"> Add New User </h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="close" ></button>
      </div>
      <div class="modal-body">
          <form id="newUserForm" action="" method="post" enctype="multipart/form-data">
              <div class="form-group">
                  <div class="form-group admin">
                    <h5>Account Type</h5>

                    <div class="form-group" v-if="type=='admin'" :required="type=='admin'">
                      <label> User Role </label><span>*</span>
                      <select name="customer" id="select_customer" class="form-control">
                          <option></option>
                          <option 
                              v-for="(role, index) in roles" 
                              :value="role.toLowerCase()" 
                              :key='index' > {{ role }}
                          </option>
                      </select>
                    </div>

                    <div class="form-group" required>
                      <label for="region"> Region </label><span>*</span>
                      <select name="region" id="region">
                        <option value="East" selected>East</option>
                      </select>
                    </div>
                  </div>

                  <div class="form-group biography">
                    <h5>Biography</h5>
                    <div class="form-group">
                      <label for="name"> Full Name </label>
                      <input type="text" name="name" id="name">
                    </div>
                    <div class="form-group">
                      <label for="email"> E-mail </label>
                      <input type="email" name="email" id="email">
                    </div>
                  </div>
                  
                  <div class="form-group login">
                    <h5>Login Details</h5>
                    <div class="form-group" required>
                      <label for="username"> Username </label><span>*</span>
                      <input v-model="username" type="text" name="username" id="username" :class="{'is-invalid':username_error}" required>
                    </div>
                    <div class="form-group" required>
                      <label for="password"> Password </label><span>*</span>
                      <input v-model="password" type="password" name="password" id="password" :class="{'is-invalid':password_error}" required>
                    </div>
                    <div class="form-group" required>
                      <label for="confirm">Confirm Password</label><span>*</span>
                      <input v-model="confirm" type="password" name="confirm" id="confirm" :class="{'is-invalid':confirm_error}" required>
                    </div>
                  </div>
              </div>
          </form>
      </div>
      <div class="modal-footer">
          <button 
            type="button" 
            v-on:click="check_submit" 
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
    import { failed, confirmed, clear, close, confirm_submit } from '../js/form-controls';
    const type:string = localStorage['role'];

    let roles:string[] = ['Chief', 'Admin', 'Judge'];
    let username = ref("");
    let password = ref("");
    let confirm = ref("");

    let username_error = ref(false);
    let password_error = ref(false);
    let confirm_error = ref(false);

    const check_submit = (e:MouseEvent) => {
      $('input, select').attr('disabled', 'disabled');

      if (form_validated()) {
        confirm_submit(e, "Are you sure you want to add new user?");
      } else {
        $('input, select').removeAttr('disabled');
      }
    }

    function form_validated() {
      let validated = true;
      if (username.value=="") {
        validated = false;
        failed("Username cannot be empty.");
      }

      if (password.value=="") {
        validated = false;
        failed("Password cannot be empty.");
      }

      if (confirm.value==password.value) {
        validated = false;
        password.value = "";
        confirm.value = "";
        failed("Your passwords do not match! try again.");
      }
      return validated;
    }

    function submit() {
        let form = new FormData($('#newUserForm')[0]);
        let url = "/api/v1/auth/register";


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
            confirmed('User has been added successfully');
            close();
          } else {
            // notify of error
            failed('Oops! \n\n'+data.message);
            password.value = "";
            confirm.value = "";
          }
        })
    }
</script>

<style scoped>

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
    /* border-width: 0;
    border-color: rgb(182, 98, 98);
    border-radius: 5px;
    background-color: rgb(182, 98, 98);
    color: rgb(64, 64, 64); */
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