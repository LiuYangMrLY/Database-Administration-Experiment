import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from "../components/Home";
import Welcome from "../components/Welcome";
import Students from "../components/Students";
import Courses from "../components/Courses";
import SC from "../components/SC"

Vue.use(VueRouter)

const routes = [
    {path: '/', redirect: '/home'},
    {
        path: '/home', component: Home, redirect: '/welcome', children: [
            {
                path: '/welcome', component: Welcome
            }, {
                path: '/students', component: Students
            }, {
                path: '/courses', component: Courses
            }, {
                path: '/sc', component: SC
            }
        ]
    }
]

const router = new VueRouter({
    routes
})

export default router
