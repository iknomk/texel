import {
    createRouter,
    createWebHistory
} from "vue-router";

import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import ProfileView from "../views/ProfileView.vue";


// Описание страниц приложения
const routes = [

    {
        path: "/",
        name: "home",
        component: HomeView
    },

    {
        path: "/login",
        name: "login",
        component: LoginView
    },

    {
        path: "/register",
        name: "register",
        component: RegisterView
    },

    {
        path: "/profile",
        name: "profile",
        component: ProfileView,
        meta: {
            requiresAuth: true
        }
    }

];


const router = createRouter({

    history: createWebHistory(),

    routes

});


// =========================
// ЗАЩИТА СТРАНИЦ
// =========================

router.beforeEach((to) => {

    const token =
        localStorage.getItem("token");

    // Если страница требует авторизации,
    // но токена нет — отправляем на login
    if (
        to.meta.requiresAuth &&
        !token
    ) {
        return "/login";
    }

});


export default router;