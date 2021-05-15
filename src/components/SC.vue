<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>选课表</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row :gutter="20" class="searchRow">
            <el-col :span="12">
                <el-input placeholder="请输入内容" v-model="searchContent" class="input-with-select">
                    <el-select v-model="select" slot="prepend" placeholder="请选择">
                        <el-option label="学号" value="1"></el-option>
                        <el-option label="学生姓名" value="2"></el-option>
                        <el-option label="课程号" value="3"></el-option>
                        <el-option label="课程名" value="4"></el-option>
                    </el-select>
                    <el-button slot="append" icon="el-icon-search" @click="searchSC"></el-button>

                </el-input>
            </el-col>
            <el-col :span="6">
                <el-button type="primary" @click="showAddDialog">添加信息</el-button>
            </el-col>
        </el-row>

        <el-table :data="tableData" style="width: 100%">
            <el-table-column
                    prop="sno"
                    label="学号"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="sname"
                    label="学生姓名"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="cno"
                    label="课程号"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="cname"
                    label="课程名"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="grade"
                    label="成绩"
                    width="">
            </el-table-column>

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="showEditDialog(scope.$index, scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="showDeleteDialog(scope.$index, scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog title="添加选课信息" :visible.sync="addDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="70px">
                <el-form-item label="学号">
                    <el-input v-model="tempDialogForm.sno"></el-input>
                </el-form-item>
                <el-form-item label="课程号">
                    <el-input v-model="tempDialogForm.cno"></el-input>
                </el-form-item>
                <el-form-item label="成绩">
                    <el-input v-model="tempDialogForm.grade"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addSCInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="修改选课信息" :visible.sync="editDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="70px">
                <el-form-item label="学号">
                    <el-input v-model="tempDialogForm.sno" disabled></el-input>
                </el-form-item>
                <el-form-item label="学生姓名">
                    <el-input v-model="tempDialogForm.sname" disabled></el-input>
                </el-form-item>
                <el-form-item label="课程号">
                    <el-input v-model="tempDialogForm.cno" disabled></el-input>
                </el-form-item>
                <el-form-item label="课程名">
                    <el-input v-model="tempDialogForm.cname" disabled></el-input>
                </el-form-item>
                <el-form-item label="成绩">
                    <el-input v-model="tempDialogForm.grade"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editSCInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="删除选课信息" :visible.sync="deleteDialogVisible" width="50%" class="deleteDialog">
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">学号</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.sno}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">学生姓名</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.sname}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">课程号</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.cno}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">课程名</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.cname}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">成绩</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.grade}}</el-col>
            </el-row>

            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">取 消</el-button>
                <el-button type="danger" @click="deleteSCInfo">删 除</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                searchContent: '',
                select: '1',

                tableData: [],

                tempDialogForm: {
                    index: null,
                    sno: null,
                    sname: null,
                    cno: null,
                    cname: null,
                    grade: null,
                },
                addDialogVisible: false,
                editDialogVisible: false,
                deleteDialogVisible: false,
            }
        },
        methods: {
            refresh() {
                this.tableData = []
                this.$http.get('administration/get_sc')
                    .then(res => {
                        this.tableData = res.data['data']['sc']
                    })
            },

            showAddDialog() {
                this.tempDialogForm.sno = null
                this.tempDialogForm.sname = null
                this.tempDialogForm.cno = null
                this.tempDialogForm.cname = null
                this.tempDialogForm.grade = null

                this.addDialogVisible = true
            },
            showEditDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.sno = row.sno
                this.tempDialogForm.sname = row.sname
                this.tempDialogForm.cno = row.cno
                this.tempDialogForm.cname = row.cname
                this.tempDialogForm.grade = row.grade

                this.editDialogVisible = true
            },
            showDeleteDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.sno = row.sno
                this.tempDialogForm.sname = row.sname
                this.tempDialogForm.cno = row.cno
                this.tempDialogForm.cname = row.cname
                this.tempDialogForm.grade = row.grade

                this.deleteDialogVisible = true
            },

            addSCInfo() {
                this.$http.post('administration/add_sc',
                    JSON.stringify({
                        'sno': this.tempDialogForm.sno,
                        'cno': this.tempDialogForm.cno,
                        'grade': this.tempDialogForm.grade
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.addDialogVisible = false
                            this.refresh()
                        }
                    })
            },
            editSCInfo() {
                this.$http.post('administration/edit_sc',
                    JSON.stringify({
                        'sno': this.tempDialogForm.sno,
                        'cno': this.tempDialogForm.cno,
                        'grade': this.tempDialogForm.grade
                    })
                ).then(res => {
                    if (res.data['code'] === undefined) {
                        this.$message.error('error')
                    } else if (res.data['code'] !== 200) {
                        this.$message.error(res.data['message'])
                    } else {
                        this.$message.success(res.data['message'])
                        this.editDialogVisible = false
                        this.refresh()
                    }
                })
            },
            deleteSCInfo() {
                this.$http.post('administration/delete_sc',
                    JSON.stringify({
                        'sno': this.tempDialogForm.sno,
                        'cno': this.tempDialogForm.cno
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.deleteDialogVisible = false
                            this.refresh()
                        }
                    })
            },

            searchSC() {
                if (this.searchContent === null || this.searchContent === '') {
                    this.$message.error('请输入搜索内容')
                    return
                }

                this.$http.get('administration/search_sc', {
                    params: {
                        't': this.select,
                        'c': this.searchContent
                    }
                })
                    .then(res => {
                        this.tableData = res.data['data']['sc']
                    })
            },
        },
        created() {
            this.refresh()
        },
    }
</script>

<style lang="less" scoped>
    .el-breadcrumb {
        padding-bottom: 15px;
    }

    .el-select {
        width: 130px;
    }

    .searchRow {
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .deleteDialog .el-row {
        padding-left: 50px;
        height: 40px;
        line-height: 40px;
        border-bottom: 1px solid #e6e6e6;

        .deleteDialogContent {
            padding-left: 10px;
            height: 40px;
            width: 300px;
            text-align: center;
        }
    }
</style>
