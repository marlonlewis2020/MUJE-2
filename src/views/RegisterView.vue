<template>
    <main>
        <div class="container col-sm-6">
            <UserForm />
        </div>
    </main>
</template>

<script setup lang="ts">
    import UserForm from '../components/UserForm.vue'
</script>

<style>
    .modal-header, [data-dismiss="modal"] {
        display:none;
    }

    .btn {
        margin-top:35px;
        margin-bottom:35px;
        margin-left:35px;
        width:110px;
    }
</style>