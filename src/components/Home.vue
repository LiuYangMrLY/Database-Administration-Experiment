<template>
    <el-container class="home-container">
        <el-header>
            <img src="../assets/logo.png" alt="" height="60%">
            <div>
                <span>学生教务管理系统</span>
            </div>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <el-menu router :default-active="$route.path">
                    <el-menu-item index="/students">
                        <i class="el-icon-user"></i>
                        <span slot="title">学生表</span>
                    </el-menu-item>
                    <el-menu-item index="/courses">
                        <i class="el-icon-document"></i>
                        <span slot="title">课程表</span>
                    </el-menu-item>
                    <el-menu-item index="/sc">
                        <i class="el-icon-tickets"></i>
                        <span slot="title">选课表</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
    export default {

    }
</script>

<style lang="less" scoped>
    .home-container {
        height: 100%;
    }

    .el-header {
        background-color: white;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        padding-left: 20px;
        font-size: 20px;

        > div {
            display: flex;
            align-items: center;

            > span {
                margin-left: 15px;
            }
        }

        > img {
            padding-top: 8px;
        }
    }

    .el-aside {
        border-right: 1px solid #e6e6e6;
        .el-menu {
            border-right: none
        }
    }

    .el-main {
        background-color: white;
    }
</style>
