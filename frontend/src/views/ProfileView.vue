<script setup>

import {
    ref,
    onMounted
} from "vue";

import {
    getCurrentUser
} from "../services/api";


const user = ref(null);

const error = ref("");

const loading = ref(true);


async function loadProfile() {

    try {

        user.value =
            await getCurrentUser();

    } catch (err) {

        error.value =
            err.message;

    } finally {

        loading.value = false;

    }

}


onMounted(() => {

    loadProfile();

});

</script>


<template>

    <div class="profile-page">

        <h1>
            Личный кабинет
        </h1>


        <div
            v-if="loading"
            class="loading"
        >
            Загрузка...
        </div>


        <div
            v-else-if="error"
            class="error-message"
        >
            {{ error }}
        </div>


        <div
            v-else-if="user"
            class="profile-card"
        >

            <div class="profile-row">

                <span>
                    ID:
                </span>

                <strong>
                    {{ user.id }}
                </strong>

            </div>


            <div class="profile-row">

                <span>
                    Username:
                </span>

                <strong>
                    {{ user.username }}
                </strong>

            </div>


            <div class="profile-row">

                <span>
                    Email:
                </span>

                <strong>
                    {{ user.email }}
                </strong>

            </div>

        </div>

    </div>

</template>