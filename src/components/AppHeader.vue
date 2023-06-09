<template>
  <!-- Navigation-->
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top" id="mainNav">
      <div class="container-fluid">
          <div class="brand">
              <a v-if="login" href="/dashboard"><img class="navbar-brand head-img" src="./icons/miss-universe.png" alt="miss universe image"> MUJE</a>
          </div>
          <a href="#page-top"><img class="navbar-brand head-img" src="./icons/miss-universe.png" alt="female image" /></a>
          <div class="menu float-end">
              <button
                  class="navbar-toggler"
                  type="button"
                  data-toggle="collapse"
                  data-target="#navbarSupportedContent"
                  aria-controls="navbarSupportedContent"
                  aria-expanded="false"
                  aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                  <ul class="navbar-nav text-uppercase ms-auto py-4 py-lg-0">
                      <li class="nav-item" v-if="!login">
                          <RouterLink v-bind:id='id' class="text-white nav-link" to="/">Home</RouterLink>
                      </li>
                      <li class="nav-item" v-if="!login" >
                          <RouterLink class="text-white nav-link" to="/login">Login</RouterLink>
                      </li>
                      
                      <li class="nav-item" v-if="!login" >
                          <RouterLink class="text-white nav-link" to="/register">Register</RouterLink>
                      </li>
                      <li class="nav-item" v-if="login">
                          <RouterLink class="text-white nav-link" to="/cpanel">Control Panel</RouterLink>
                      </li>
                      <li class="nav-item" v-if="login && admin">
                          <RouterLink class="text-white nav-link" to="/dashboard">Dashboard</RouterLink>
                      </li>
                      <li class="nav-item" v-if="login" >
                          <a class="text-white nav-link" @click="logout">Logout</a>
                      </li>
                  </ul>
              </div>
          </div>
      </div>
  </nav>
  <!-- Masthead-->
  <header class="masthead">
      <div class="container">
          <div class="masthead-subheading">The MUJE Judging App!</div>
      </div>
  </header>
</template>

<script setup lang="ts">
  import { RouterLink } from "vue-router";
  let login:boolean = localStorage['token']? true : false;
  let id: number = localStorage['id'] ?? 0;
  let type: string = localStorage['role'];
  let admin:boolean = type=="chief" || type=="admin";

  function logout() {
    const url: string = "/api/v1/auth/logout"; 
    fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `bearer ${localStorage['token']}`
        }
    })
    .then((data)=>{
        // update the token and id in localStorage
        localStorage.clear();
        window.location.assign("/");
    });
  }
</script>

<style scoped>
  /* Add any component specific styles here */
  @import url('https://fonts.googleapis.com/css2?family=Lobster');

  .navbar {
    background-color: rgb(67, 9, 122);
    margin-bottom: 30px;
  }
  .navbar-brand {
    font-family: 'Lobster', sans-serif;
  }

  .head-img {
    width:64px;
  }
  header {
    margin-top: 100px;
    margin-bottom: 50px;
  }

  a {
    text-decoration-line: none;
    -moz-text-decoration-line: none;
  }

  ul.nav li a, ul.nav li a:visited {
    color: white !important;
  }

  li, .nav-item {
    width:150px;
    margin: 0 10px;
  }

  li, .nav-item:hover {
    color:goldenrod;
  }

  a:hover {
    font-weight: bold;
  }
</style>