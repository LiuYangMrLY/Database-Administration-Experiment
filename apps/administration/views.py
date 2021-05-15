import math
import json
import re

from django.http import JsonResponse

from apps.utils.Database import connection


def get_students(request):
    content = {'code': 200, 'message': '成功'}
    current_page = int(request.GET.get('current_page', 1))

    with connection.cursor() as cursor:
        SELECT_COUNT_FROM_STUDENT_TABLE_SQL = '''
        SELECT COUNT(*) FROM Student;
        '''
        cursor.execute(SELECT_COUNT_FROM_STUDENT_TABLE_SQL)
        total_students = cursor.fetchone()[0]
        total_page = math.ceil(total_students / 10)
        if current_page > total_page:
            current_page = total_page

        content['data'] = {
            'students': [],
            'current_page': current_page,
            'total_page': total_page
        }

        SELECT_STUDENTS_FROM_STUDENT_TABLE_SQL = '''
        SELECT * FROM Student LIMIT %s, %s;
        '''
        cursor.execute(SELECT_STUDENTS_FROM_STUDENT_TABLE_SQL, ((current_page - 1) * 10, 10,))
        for one in cursor:
            content['data']['students'].append({
                'no': one[0],
                'name': one[1],
                'gender': one[2],
                'age': one[3],
                'department': one[4]
            })

    return JsonResponse(content)


def add_student(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')
    if not sno:
        content['code'] = 400
        content['message'] = '缺少学号'
        return JsonResponse(content)
    if len(sno) != 11:
        content['code'] = 400
        content['message'] = '学号长度为 11 位'
        return JsonResponse(content)
    if re.search(r'[^0-9]', sno):
        content['code'] = 400
        content['message'] = '学号仅含数字'
        return JsonResponse(content)
    with connection.cursor() as cursor:
        SELECT_STUDENT_FROM_STUDENT_TABLE_SQL = '''
        SELECT sno
        FROM Student
        WHERE sno=%s;
        '''
        cursor.execute(SELECT_STUDENT_FROM_STUDENT_TABLE_SQL, (sno,))
        if cursor.fetchone():
            content['code'] = 400
            content['message'] = '学号重复'
            return JsonResponse(content)

    name = request_data.get('name')
    if not name:
        content['code'] = 400
        content['message'] = '缺少姓名'
        return JsonResponse(content)
    if not len(name) <= 20:
        content['code'] = 400
        content['message'] = '姓名不超过 20 位'
        return JsonResponse(content)

    gender = request_data.get('gender')
    if not gender:
        content['code'] = 400
        content['message'] = '缺少性别'
        return JsonResponse(content)
    if gender not in ('男', '女'):
        content['code'] = 400
        content['message'] = '性别只能为男或女'
        return JsonResponse(content)

    age = str(request_data.get('age'))
    if not age:
        content['code'] = 400
        content['message'] = '缺少年龄'
        return JsonResponse(content)
    if re.search(r'[^0-9]', age):
        content['code'] = 400
        content['message'] = '年龄只能为数字'
        return JsonResponse(content)
    age = int(age)
    if not 0 <= age <= 150:
        content['code'] = 400
        content['message'] = '年龄范围错误'
        return JsonResponse(content)

    department = request_data.get('department')
    if not department:
        content['code'] = 400
        content['message'] = '缺少系'
        return JsonResponse(content)

    with connection.cursor() as cursor:
        INSERT_STUDENT_INTO_STUDENT_TABLE_SQL = '''
        INSERT INTO Student (sno, name, gender, age, department)
        VALUES (%s, %s, %s, %s, %s);
        '''
        cursor.execute(INSERT_STUDENT_INTO_STUDENT_TABLE_SQL, (sno, name, gender, age, department))
        connection.commit()

    return JsonResponse(content)


def delete_student(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')

    with connection.cursor() as cursor:
        DELETE_STUDENT_FROM_STUDENT_TABLE_SQL = '''
        DELETE FROM Student
        WHERE sno=%s;
        '''
        cursor.execute(DELETE_STUDENT_FROM_STUDENT_TABLE_SQL, (sno,))
        connection.commit()

    return JsonResponse(content)


def edit_student(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')

    name = request_data.get('name')
    if not name:
        content['code'] = 400
        content['message'] = '缺少姓名'
        return JsonResponse(content)
    if not len(name) <= 20:
        content['code'] = 400
        content['message'] = '姓名不超过 20 位'
        return JsonResponse(content)

    gender = request_data.get('gender')
    if not gender:
        content['code'] = 400
        content['message'] = '缺少性别'
        return JsonResponse(content)
    if gender not in ('男', '女'):
        content['code'] = 400
        content['message'] = '性别只能为男或女'
        return JsonResponse(content)

    age = str(request_data.get('age'))
    if not age:
        content['code'] = 400
        content['message'] = '缺少年龄'
        return JsonResponse(content)
    if re.search(r'[^0-9]', age):
        content['code'] = 400
        content['message'] = '年龄只能为数字'
        return JsonResponse(content)
    age = int(age)
    if not 0 <= age <= 150:
        content['code'] = 400
        content['message'] = '年龄范围错误'
        return JsonResponse(content)

    department = request_data.get('department')
    if not department:
        content['code'] = 400
        content['message'] = '缺少系'
        return JsonResponse(content)

    with connection.cursor() as cursor:
        UPDATE_STUDENT_IN_STUDENT_TABLE_SQL = '''
        UPDATE Student
        SET name=%s, gender=%s, age=%s, department=%s
        WHERE sno=%s;
        '''
        cursor.execute(UPDATE_STUDENT_IN_STUDENT_TABLE_SQL, (name, gender, age, department, sno,))
        connection.commit()

    return JsonResponse(content)


def search_student(request):
    content = {'code': 200, 'message': '成功'}

    t = request.GET.get('t')
    c = request.GET.get('c')

    SELECT_STUDENT_BY_SNO_FROM_STUDENT_TABLE_SQL = '''
    SELECT * FROM Student
    WHERE sno=%s;
    '''
    SELECT_STUDENT_BY_NAME_FROM_STUDENT_TABLE_SQL = '''
    SELECT * FROM Student
    WHERE name=%s;
    '''
    SELECT_STUDENT_BY_DEPARTMENT_FROM_STUDENT_TABLE_SQL = '''
    SELECT * FROM Student
    WHERE department=%s;
    '''

    TYPE_TO_SQL_MAPPING = {'1': SELECT_STUDENT_BY_SNO_FROM_STUDENT_TABLE_SQL,
                           '2': SELECT_STUDENT_BY_NAME_FROM_STUDENT_TABLE_SQL,
                           '3': SELECT_STUDENT_BY_DEPARTMENT_FROM_STUDENT_TABLE_SQL
                           }
    sql = TYPE_TO_SQL_MAPPING[t]

    with connection.cursor() as cursor:
        content['data'] = {
            'students': []
        }

        cursor.execute(sql, (c,))
        for one in cursor:
            content['data']['students'].append({
                'no': one[0],
                'name': one[1],
                'gender': one[2],
                'age': one[3],
                'department': one[4]
            })

    return JsonResponse(content)


def get_courses(request):
    content = {'code': 200, 'message': '成功'}

    with connection.cursor() as cursor:
        content['data'] = {
            'courses': []
        }

        SELECT_ALL_COURSES_FROM_COURSE_TABLE_SQL = '''
        SELECT A.cno, A.name, B.name, A.credit, A.cpno
        FROM Course A LEFT OUTER JOIN Course B
        ON (A.cpno=B.cno);
        '''

        cursor.execute(SELECT_ALL_COURSES_FROM_COURSE_TABLE_SQL)
        for one in cursor:
            content['data']['courses'].append({
                'cno': one[0],
                'name': one[1],
                'cpno_name': one[2],
                'credit': one[3],
                'cpno': one[4]
            })

    return JsonResponse(content)


def add_course(request):
    content = {'code': 200, 'message': '成功'}

    request_data = json.loads(request.body)

    cno = request_data.get('cno')
    if not cno:
        content['code'] = 400
        content['message'] = '缺少课程号'
        return JsonResponse(content)
    if len(cno) != 5:
        content['code'] = 400
        content['message'] = '课程号长度为 5 位'
        return JsonResponse(content)
    if re.search(r'[^0-9]', cno):
        content['code'] = 400
        content['message'] = '课程号仅含数字'
        return JsonResponse(content)
    with connection.cursor() as cursor:
        SELECT_COURSE_FROM_COURSE_TABLE_SQL = '''
        SELECT cno
        FROM Course
        WHERE cno=%s;
        '''
        cursor.execute(SELECT_COURSE_FROM_COURSE_TABLE_SQL, (cno,))
        if cursor.fetchone():
            content['code'] = 400
            content['message'] = '课程号重复'

    name = request_data.get('name')
    if not name:
        content['code'] = 400
        content['message'] = '缺少课程名'
        return JsonResponse(content)
    if not len(name) <= 20:
        content['code'] = 400
        content['message'] = '课程名不超过 20 位'
        return JsonResponse(content)

    cpno = request_data.get('cpno')

    credit = request_data.get('credit')
    try:
        credit = int(credit)
    except:
        content['code'] = 400
        content['message'] = '学分仅为正整数'
        return JsonResponse(content)
    if not credit >= 0:
        content['code'] = 400
        content['message'] = '学分仅为正整数'
        return JsonResponse(content)

    with connection.cursor() as cursor:
        INSERT_COURSE_INTO_COURSE_TABLE_SQL = '''
        INSERT INTO Course (cno, name, cpno, credit)
        VALUES (%s, %s, %s, %s);
        '''
        cursor.execute(INSERT_COURSE_INTO_COURSE_TABLE_SQL, (cno, name, cpno, credit))
        connection.commit()

    return JsonResponse(content)


def delete_course(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    cno = request_data.get('cno')

    with connection.cursor() as cursor:
        SELECT_COURSE_BY_CPNO_FROM_COURSE_TABLE_SQL = '''
        SELECT cno, name
        FROM Course
        WHERE cpno=%s;
        '''
        cursor.execute(SELECT_COURSE_BY_CPNO_FROM_COURSE_TABLE_SQL, (cno,))
        course = cursor.fetchone()
        if course:
            content['code'] = 400
            content['message'] = '无法删除: {} {} 以本课程为先修课'.format(course[0], course[1])
            return JsonResponse(content)

    with connection.cursor() as cursor:
        DELETE_STUDENT_FROM_STUDENT_TABLE_SQL = '''
        DELETE FROM Course
        WHERE cno=%s;
        '''
        cursor.execute(DELETE_STUDENT_FROM_STUDENT_TABLE_SQL, (cno,))
        connection.commit()

    return JsonResponse(content)


def edit_course(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    cno = request_data.get('cno')

    name = request_data.get('name')
    if not name:
        content['code'] = 400
        content['message'] = '缺少课程名'
        return JsonResponse(content)
    if not len(name) <= 20:
        content['code'] = 400
        content['message'] = '课程名不超过 20 位'
        return JsonResponse(content)

    cpno = request_data.get('cpno')

    credit = request_data.get('credit')
    try:
        credit = int(credit)
    except:
        content['code'] = 400
        content['message'] = '学分仅为正整数'
        return JsonResponse(content)
    if not credit >= 0:
        content['code'] = 400
        content['message'] = '学分仅为正整数'
        return JsonResponse(content)

    with connection.cursor() as cursor:
        UPDATE_COURSE_IN_COURSE_TABLE_SQL = '''
        UPDATE Course
        SET name=%s, cpno=%s, credit=%s
        WHERE cno=%s;
        '''
        cursor.execute(UPDATE_COURSE_IN_COURSE_TABLE_SQL, (name, cpno, credit, cno))
        connection.commit()

    return JsonResponse(content)


def search_course(request):
    content = {'code': 200, 'message': '成功'}

    t = request.GET.get('t')
    c = request.GET.get('c')

    SELECT_COURSE_BY_CNO_FROM_COURSE_TABLE_SQL = '''
    SELECT A.cno, A.name, B.name, A.credit, A.cpno
    FROM Course A LEFT OUTER JOIN Course B
    ON (A.cpno=B.cno)
    WHERE A.cno=%s;
    '''
    SELECT_COURSE_BY_NAME_FROM_COURSE_TABLE_SQL = '''
    SELECT A.cno, A.name, B.name, A.credit, A.cpno
    FROM Course A LEFT OUTER JOIN Course B
    ON (A.cpno=B.cno)
    WHERE A.name=%s;
    '''

    TYPE_TO_SQL_MAPPING = {'1': SELECT_COURSE_BY_CNO_FROM_COURSE_TABLE_SQL,
                           '2': SELECT_COURSE_BY_NAME_FROM_COURSE_TABLE_SQL,
                           }
    sql = TYPE_TO_SQL_MAPPING[t]

    with connection.cursor() as cursor:
        content['data'] = {
            'courses': []
        }

        cursor.execute(sql, (c,))
        for one in cursor:
            content['data']['courses'].append({
                'cno': one[0],
                'name': one[1],
                'cpno_name': one[2],
                'credit': one[3],
                'cpno': one[4]
            })

    return JsonResponse(content)


def get_sc(request):
    content = {'code': 200, 'message': '成功'}

    with connection.cursor() as cursor:
        content['data'] = {
            'sc': []
        }

        SELECT_ALL_SC_FROM_SC_TABLE_SQL = '''
        SELECT Student.sno, Student.name, Course.cno, Course.name, SC.grade
        FROM Student, Course, SC
        WHERE Student.sno=SC.sno AND Course.cno=SC.cno;
        '''

        cursor.execute(SELECT_ALL_SC_FROM_SC_TABLE_SQL)
        for one in cursor:
            content['data']['sc'].append({
                'sno': one[0],
                'sname': one[1],
                'cno': one[2],
                'cname': one[3],
                'grade': one[4]
            })

    return JsonResponse(content)


def add_sc(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')
    with connection.cursor() as cursor:
        SELECT_SNO_FROM_STUDENT_TABLE_SQL = '''
        SELECT sno
        FROM Student
        WHERE sno=%s;
        '''
        cursor.execute(SELECT_SNO_FROM_STUDENT_TABLE_SQL, (sno,))
        if not cursor.fetchone():
            content['code'] = 400
            content['message'] = '学号不存在'
            return JsonResponse(content)

    cno = request_data.get('cno')
    with connection.cursor() as cursor:
        SELECT_CNO_FROM_COURSE_TABLE_SQL = '''
        SELECT cno
        FROM Course
        WHERE cno=%s;
        '''
        cursor.execute(SELECT_CNO_FROM_COURSE_TABLE_SQL, (cno,))
        if not cursor.fetchone():
            content['code'] = 400
            content['message'] = '课程号不存在'
            return JsonResponse(content)

    grade = request_data.get('grade')
    if grade:
        try:
            grade = int(grade)
        except:
            content['code'] = 400
            content['message'] = '分数必须为整数'
            return JsonResponse(content)
        if not 0 <= grade <= 100:
            content['code'] = 400
            content['message'] = '分数必须为 0 ~ 100'
            return JsonResponse(content)
    else:
        grade = None

    with connection.cursor() as cursor:
        INSERT_SC_INTO_SC_TABLE_SQL = '''
        INSERT INTO SC
        VALUES (%s, %s, %s);
        '''
        cursor.execute(INSERT_SC_INTO_SC_TABLE_SQL, (sno, cno, grade))
        connection.commit()

    return JsonResponse(content)


def edit_sc(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')
    cno = request_data.get('cno')

    grade = request_data.get('grade')
    if grade:
        try:
            grade = int(grade)
        except:
            content['code'] = 400
            content['message'] = '分数必须为整数'
            return JsonResponse(content)
        if not 0 <= grade <= 100:
            content['code'] = 400
            content['message'] = '分数必须为 0 ~ 100'
            return JsonResponse(content)
    else:
        grade = None

    with connection.cursor() as cursor:
        UPDATE_GRADE_ON_SC_TABLE_SQL = '''
        UPDATE SC
        SET grade=%s
        WHERE sno=%s AND cno=%s;
        '''
        cursor.execute(UPDATE_GRADE_ON_SC_TABLE_SQL, (grade, sno, cno))
        connection.commit()

    return JsonResponse(content)


def delete_sc(request):
    request_data = json.loads(request.body)
    content = {'code': 200, 'message': '成功'}

    sno = request_data.get('sno')
    cno = request_data.get('cno')

    with connection.cursor() as cursor:
        DELETE_SC_FROM_SC_TABLE_SQL = '''
        DELETE FROM SC
        WHERE sno=%s AND cno=%s;
        '''

        cursor.execute(DELETE_SC_FROM_SC_TABLE_SQL, (sno, cno,))
        connection.commit()

    return JsonResponse(content)


def search_sc(request):
    content = {'code': 200, 'message': '成功'}

    t = request.GET.get('t')
    c = request.GET.get('c')

    SELECT_SC_BY_SNO_FROM_SC_TABLE_SQL = '''
    SELECT Student.sno, Student.name, Course.cno, Course.name, SC.grade
    FROM Student, Course, SC
    WHERE Student.sno=SC.sno AND Course.cno=SC.cno AND Student.sno=%s;
    '''
    SELECT_SC_BY_SNAME_FROM_SC_TABLE_SQL = '''
    SELECT Student.sno, Student.name, Course.cno, Course.name, SC.grade
    FROM Student, Course, SC
    WHERE Student.sno=SC.sno AND Course.cno=SC.cno AND Student.name=%s;
    '''
    SELECT_SC_BY_CNO_FROM_SC_TABLE_SQL = '''
    SELECT Student.sno, Student.name, Course.cno, Course.name, SC.grade
    FROM Student, Course, SC
    WHERE Student.sno=SC.sno AND Course.cno=SC.cno AND Course.cno=%s;
    '''
    SELECT_SC_BY_CNAME_FROM_SC_TABLE_SQL = '''
    SELECT Student.sno, Student.name, Course.cno, Course.name, SC.grade
    FROM Student, Course, SC
    WHERE Student.sno=SC.sno AND Course.cno=SC.cno AND Course.name=%s;
    '''

    TYPE_TO_SQL_MAPPING = {'1': SELECT_SC_BY_SNO_FROM_SC_TABLE_SQL,
                           '2': SELECT_SC_BY_SNAME_FROM_SC_TABLE_SQL,
                           '3': SELECT_SC_BY_CNO_FROM_SC_TABLE_SQL,
                           '4': SELECT_SC_BY_CNAME_FROM_SC_TABLE_SQL,
                           }
    sql = TYPE_TO_SQL_MAPPING[t]

    with connection.cursor() as cursor:
        content['data'] = {
            'sc': []
        }

        cursor.execute(sql, (c,))
        for one in cursor:
            content['data']['sc'].append({
                'sno': one[0],
                'sname': one[1],
                'cno': one[2],
                'cname': one[3],
                'grade': one[4]
            })

    return JsonResponse(content)
