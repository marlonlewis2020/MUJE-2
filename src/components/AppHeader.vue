<template>
  <!-- Navigation-->
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top" id="mainNav">
      <div class="container-fluid">
          <div class="brand">
              <a v-if="login" class="navbar-brand" href="/dashboard"><img class="head-img" src="../components/icons/woman_avatar.png" alt="camera image"> MUJE</a>
          </div>
          <a class="navbar-brand" href="#page-top"><img class="head-img" src="../components/icons/woman_avatar.png" alt="..." /></a>
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
              <div class="collapse navbar-collapse" id="navbarResponsive">
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
          <div class="masthead-subheading">Welcome To The MUJE Judging App!</div>
          <div class="masthead-heading text-uppercase">Let's Begin Scoring The Ladies</div>
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
    background-color: blue;
    margin-bottom: 30px;
  }
  .navbar-brand {
    font-family: 'Lobster', sans-serif;
  }

  .head-img {
    width:36px;
    padding-bottom: 10px;
    padding-right: 6px;
  }
  header {
    margin-bottom: 200px;
  }

  a {
    text-decoration-line: none;
    -moz-text-decoration-line: none;
  }

  ul.nav li a, ul.nav li a:visited {
    color: white !important;
  }

  li {
    width:80px;
    margin: 0 10px;
  }

  a:hover {
    font-weight: bold;
  }
</style>