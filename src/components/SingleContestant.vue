<template>
    <div v-if="preview" class="preview">
        <img id="preview-img" :src="`./src/components/images/${lady['photo']}`" alt="image preview" class="preview-img"/>
    </div>
    <form id="addPostForm" action="" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="score">Score</label>
            <select v-model="score" name="score" id="score" cols="30" rows="2" class="form-control" maxlength="75">
                <option v-for="mark, index in numbers" :key="index" :value="mark">{{ mark }}</option>
            </select>
        </div>
        <input id="save" type="button" value="SAVE" @click="set_score" class="form-control btn btn-primary">
    </form>
</template>

<script setup lang="ts">

    import { ref } from 'vue';

    let preview:boolean = true;
    const prop = defineProps(['lady', 'numbers']);
    const emit = defineEmits<{
        (event:'scored', val:number):void
    }>();
    let score = ref(0);

    function set_score() {
        emit("scored", score.value);
        score.value = 0;
    }

</script>

<style scoped>
    
    .preview, #preview-img {
        width:100%;
    }
        
    #save {
        margin-top:30px;
        justify-content: center;
        align-items: center;
    }

</style>