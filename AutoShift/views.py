from django.shortcuts import render, HttpResponse
from django.views import View
from AutoShift import models
import time
import calendar
import json

# Create your views here.

# Commonly used variables
date_obj = {
    'date_list': [],
    'month': "",
    'day_from': "",
    'day_to': "",
    'day_before': "",
    'day_before2': "",
    'day_before3': ""
}

date_obj['month'] = time.localtime().tm_mon

staff_list = []


class Schedule(View):

    def get(self, request):
        curr_date = time.localtime()
        query_date_from = "-".join((str(curr_date.tm_year), str(curr_date.tm_mon),"01"))
        query_date_to = "-".join((str(curr_date.tm_year), str(curr_date.tm_mon),
                                  str(calendar.monthrange(curr_date.tm_year, curr_date.tm_mon)[1])))

        date_obj['month'] = query_date_from.split('-')[1]
        date_obj['day_from'] = query_date_from.split('-')[2]
        date_obj['day_to'] = query_date_to.split('-')[2]

        date_list = []

        for i in range(int(date_obj['day_from']), int(date_obj['day_to'])+1):
            day = str(i) if len(str(i)) == 2 else '0' + str(i)
            mon = date_obj['month']
            date = '2018-' + mon + '-' + day
            date_list.append(date)
        date_obj['date_list'] = date_list

        # 获取员工列表
        staff_list = []
        obj = models.Workhours.objects.all().order_by('workhours')
        for i in obj:
            staff_list.append({'name': i.employee.name,
                               'uid': i.employee.uid})

        # 获取每个员工的排班
        shift_list = []
        for i in staff_list:
            tmp_list = []
            for d in date_obj['date_list']:
                obj = models.Schedule.objects.filter(date=d, employee_id='%s' % i['uid']).first()
                if obj:
                    tmp_list.append(obj.shift.name)
                else:
                    tmp_list.append("")
            shift_list.append({ 'shifts': tmp_list,
                                'name': i['name'],
                                'id': i['uid']})

        return render(request, 'schedule.html', {'shift_list': shift_list, 'date_list': date_list})

    def post(self, request):
        curr_date = time.localtime()
        query_date_from = request.POST.get('date_from')
        query_date_to = request.POST.get('date_to')

        date_obj['month'] = query_date_from.split('-')[1]
        date_obj['day_from'] = query_date_from.split('-')[2]
        date_obj['day_to'] = query_date_to.split('-')[2]

        date_list = []

        for i in range(int(date_obj['day_from']), int(date_obj['day_to'])+1):
            day = str(i) if len(str(i)) == 2 else '0' + str(i)
            mon = date_obj['month']
            date = '2018-' + mon + '-' + day
            date_list.append(date)
        date_obj['date_list'] = date_list


        # 获取员工列表
        staff_list = []
        obj = models.Workhours.objects.all().order_by('workhours')
        for i in obj:
            staff_list.append({'name': i.employee.name,
                               'uid': i.employee.uid})

        # 获取每个员工的排班
        shift_list = []
        for i in staff_list:
            tmp_list = []
            for d in date_obj['date_list']:
                obj = models.Schedule.objects.filter(date=d, employee_id='%s' % i['uid']).first()
                if obj:
                    tmp_list.append(obj.shift.name)
                else:
                    tmp_list.append("")
            shift_list.append({ 'shifts': tmp_list,
                                'name': i['name'],
                                'id': i['uid']})

        return render(request, 'schedule.html', {'shift_list': shift_list, 'date_list': date_list})

class Arrange(View):

    def get(self, request):
        return render(request, 'arrange.html')

    def post(self, request):
        date_from = request.POST.get('date_from')
        date_obj["date_from"] = date_from
        date_to = request.POST.get('date_to')
        date_obj["date_to"] = date_to
        year = date_from.split('-')[0]
        month = date_from.split('-')[1]
        date_obj['month'] = month
        day_from = date_from.split('-')[2]
        day_to = date_to.split('-')[2]
        date_list = []

        for i in range(int(day_from), int(day_to)+1):
            day = str(i) if len(str(i)) == 2 else '0' + str(i)
            date = year + '-' + month + '-' + day
            date_list.append(date)
        date_obj['date_list'] = date_list
        # 获取排班对象
        shift_list = []
        obj = models.Shifts.objects.all().order_by('onduty')
        for i in obj:
            shift_list.append(i)

        # 组装排班字典
        arrange_list = []
        for s in shift_list:
            tmp_list = []
            for d in date_list:
                obj = models.Arrangement.objects.filter(date=d, shift_id=s.name).first()
                if obj:
                    tmp_list.append({"number": obj.number, "date": d})
                else:
                    tmp_list.append({"number": 0, "date": d})
            arrange_list.append({'shift': s.name, "shift_list": tmp_list})

        return render(request, 'arrange.html', {"date_list": date_list, "arrange_list": arrange_list})


class Staff(View):

    def get(self, request):
        # 获取月份列表
        month_list = []
        obj = models.Workhours.objects.all().values('month').distinct().order_by('month')
        for i in obj:
            month_list.append(i['month'])

        # 获取员工列表
        staff_list = models.Employees.objects.all().order_by('uid')


        # 获取员工每月工时列表
        workhour_list = []
        for s in staff_list:
            tmp_list = []
            for m in month_list:
                obj = models.Workhours.objects.filter(month=m, employee=s).first()
                if obj:
                    tmp_list.append(obj.workhours)
                else:
                    tmp_list.append('0')
            workhour_list.append({"staff": s,
                                  "hours": tmp_list})

        return render(request, 'staff.html', {"workhour_list": workhour_list, "month_list": month_list})


class Shift(View):

    def get(self, request):
        obj = models.Shifts.objects.all().order_by('onduty')

        return render(request, 'shift.html', {"shift_list": obj})


class Vacation(View):

    def get(self, request):
        obj = models.Vacation.objects.all().order_by('date')
        return render(request, 'vacation.html', {'vacation_list': obj})


# 排班创建&修改
def ajax_shift_mod(request):
    ret = {'status': True, 'error': None, 'data': None}
    shiftname = request.POST.get('shiftname')
    onduty = request.POST.get('onduty')
    offduty = request.POST.get('offduty')
    id = request.POST.get('id')
    onduty_time = float(onduty.split(':')[0]) + float(onduty.split(':')[1])/60
    offduty_time = float(offduty.split(':')[0]) + float(offduty.split(':')[1])/60
    hours = round(offduty_time - onduty_time - 1, 1)
    if len(id) != 0:
        data_new = {'id': id, 'name': shiftname, 'onduty': onduty,
                    'offduty': offduty, 'hours': hours}
        try:
            models.Shifts.objects.filter(id=id).update(**data_new)
        except:
            ret['status'] = False
            ret['error'] = 'Update DB Error!'
    else:
        try:
            models.Shifts.objects.create(name=shiftname, onduty=onduty, offduty=offduty,
                                         hours=hours)
        except:
            ret['status'] = False
            ret['error'] = 'DB Inserting Error!'
    return HttpResponse(json.dumps(ret))

# 排班删除
def ajax_shift_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    id = request.POST.get('id')
    try:
        models.Shifts.objects.filter(id=id).delete()
    except:
        ret['status'] = False
        ret['error'] = 'DB Deleting Error!'
    return HttpResponse(json.dumps(ret))

# 修改排班需求并触发排班
def ajax_arrange_submit(request):
    ret = {'status': True, 'error': None, 'data': None}
    arrange_list = json.loads(request.POST.get('all'))
    for i in arrange_list:
        shift = i['name'].split('_')[0]
        date = i['name'].split('_')[1]
        number = i['number']
        obj = models.Arrangement.objects.filter(date=date, shift_id=shift).first()
        if obj:
            models.Arrangement.objects.filter(date=date, shift_id=shift).update(number=number)
        else:
            models.Arrangement.objects.create(shift_id=shift, date=date, number=number)

    # 清空所选日期的排班表
    models.Schedule.objects.filter(date__gte=date_obj['date_list'][0],
                                   date__lte=date_obj['date_list'][-1]).delete()
    # 清空当月工时
    models.Workhours.objects.filter(month=date_obj['month']).delete()

    shiftArrange()
    return HttpResponse(json.dumps(ret))

# 请假创建&修改
def ajax_vacation_mod(request):
    ret = {'status': True, 'error': None, 'data': None}
    vacationdate = request.POST.get('vacationdate')
    uid = request.POST.get('uid')
    id = request.POST.get('id')
    if len(id) != 0:
        data_new = {'employee_id': uid, 'date': vacationdate}
        try:
            models.Vacation.objects.filter(id=id).update(**data_new)
        except:
            ret['status'] = False
            ret['error'] = 'Update DB Error!'
    else:
        try:
            models.Vacation.objects.create(date=vacationdate, employee_id=uid)
        except:
            ret['status'] = False
            ret['error'] = 'DB Inserting Error!'
    return HttpResponse(json.dumps(ret))

# 请假删除
def ajax_vacation_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    id = request.POST.get('id')
    try:
        models.Vacation.objects.filter(id=id).delete()
    except:
        ret['status'] = False
        ret['error'] = 'DB Deleting Error!'
    return HttpResponse(json.dumps(ret))

def shiftArrange():
    # 日期列表
    date_list = date_obj['date_list']

    # 员工列表
    staff_list = []
    obj = models.Employees.objects.all().order_by('uid')
    for i in obj:
        staff_list.append(i.uid)

    # 班次列表
    shift_list = []
    obj = models.Shifts.objects.all().order_by('onduty')
    for i in obj:
        shift_list.append({'name': i.name, 'onduty': i.onduty, 'offduty': i.offduty, 'hours': i.hours})

    # 排班的核心逻辑
    for day in date_list:

        # 获取前3天的日期, 给后面不能连续3天上班做判断用
        if day.split("-")[2] == "01":
            tmp = '01'
        else:
            tmp = str(int(day.split("-")[2]) - 1) if len(str(int(day.split("-")[2]) - 1)) == 2 \
                else "0" + str(int(day.split("-")[2]) - 1)
        day_before = day.split('-')[0] + '-' + day.split('-')[1] + '-' + tmp
        #date_obj["day_before"] = day.split('-')[0] + '-' + day.split('-')[1] + '-' + tmp

        if day.split("-")[2] == "01":
            day_before2 = day
            #date_obj["day_before2"] = day
        elif day.split("-")[2] == "02":
            day_before2 = day.split('-')[0] + '-' + day.split('-')[1] + '-01'
            #date_obj["day_before2"] = day.split('-')[0] + day.split('-')[1] + '01'
        else:
            tmp = str(int(day.split("-")[2]) - 2) if len(str(int(day.split("-")[2]) - 2)) == 2 \
                else "0" + str(int(day.split("-")[2]) - 2)
            day_before2 = day.split('-')[0] + '-' + day.split('-')[1] + '-' + tmp
            #date_obj["day_before2"] = day.split('-')[0] + day.split('-')[1] + tmp

        if day.split("-")[2] == "01":
            day_before3 = day
            #date_obj["day_before3"] = day
        elif day.split("-")[2] == "02":
            day_before3 = day.split('-')[0] + '-' + day.split('-')[1] + '-01'
            #date_obj["day_before3"] = day.split('-')[0] + day.split('-')[1] + '01'
        elif day.split("-")[2] == "03":
            day_before3 = day.split('-')[0] + '-' + day.split('-')[1] + '-01'
            #date_obj["day_before3"] = day.split('-')[0] + day.split('-')[1] + '01'
        else:
            tmp = str(int(day.split("-")[2]) - 3) if len(str(int(day.split("-")[2]) - 3)) == 2 \
                else "0" + str(int(day.split("-")[2]) - 3)
            day_before3 = day.split('-')[0] + '-' + day.split('-')[1] + '-' + tmp
            #date_obj["day_before3"] = day.split('-')[0] + day.split('-')[1] + tmp

        for shift in shift_list:
            # 先查询当前这个班次需要几个人
            count = 0
            required_num = models.Arrangement.objects.filter(date=day, shift_id=shift['name']).first()
            if required_num:
                count = int(required_num.number)
            else:
                continue

            new_staff_list = []
            for i in staff_list:
                obj = models.Workhours.objects.filter(employee_id=i).first()
                if not obj:
                    models.Workhours.objects.create(month=date_obj['month'], employee_id=i,
                                                    workhours=0)

            obj = models.Workhours.objects.filter(month=date_obj['month']).order_by('workhours')
            for i in obj:
                new_staff_list.append(i.employee_id)

            while count > 0 and new_staff_list:

                staff = new_staff_list[0]
                new_staff_list = new_staff_list[2:]
                # 查看是否该员工请假了
                vacation = models.Vacation.objects.filter(date=day, employee_id=staff).first()
                if vacation:
                    continue
                else:

                    # 查看昨天是否有排班
                    obj = models.Schedule.objects.filter(employee_id=staff, date=day_before).order_by('date').first()
                    curr_onduty = ""
                    last_offduty = ""
                    if obj:
                        last_offduty = obj.shift.offduty.split(':')
                        last_offduty = round((float(last_offduty[0]) + float(last_offduty[1])/60), 1)
                        curr_onduty = shift['onduty'].split(':')
                        curr_onduty = round((float(curr_onduty[0]) + float(curr_onduty[1]) / 60) + 24, 1)
                    # 上一次排班在8小时内则换人

                    if obj and (curr_onduty - last_offduty <= 8) and day.split('-')[2] != "01":
                        break

                    # 查看是否已经连续3天上班了
                    obj = models.Schedule.objects.filter(date__gte=day_before3, date__lte=day_before, employee_id=staff)
                    if len(obj) == 3:
                        break

                    obj = models.Schedule.objects.filter(date=day, employee_id=staff)
                    if obj:
                        obj.update(shift_id=shift['name'])
                    else:
                        models.Schedule.objects.create(date=day, employee_id=staff, shift_id=shift['name'])
                    obj = models.Workhours.objects.filter(month=date_obj['month'], employee_id=staff)
                    if obj:
                        workhours = round(float(obj[0].workhours) + float(shift['hours']), 2)
                        obj.update(workhours=workhours)
                    else:
                        workhours = round(float(shift['hours']), 2)
                        models.Workhours.objects.create(month=date_obj['month'], employee_id=staff,
                                                        workhours=workhours)
                    count -= 1

# 员工添加/编辑
def ajax_staff_mod(request):
    ret = {'status': True, 'error': None, 'data': None}
    uid = request.POST.get('staffuid')
    name = request.POST.get('staffname')
    id = request.POST.get('id')

    if len(id) != 0:
        data_new = {'name': name, 'uid': uid}
        try:
            models.Employees.objects.filter(id=id).update(**data_new)
        except:
            ret['status'] = False
            ret['error'] = 'Update DB Error!'
    else:
        try:
            models.Employees.objects.create(uid=uid, name=name)
        except:
            ret['status'] = False
            ret['error'] = 'DB Inserting Error!'
    return HttpResponse(json.dumps(ret))

# 请假删除
def ajax_staff_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    id = request.POST.get('id')
    try:
        models.Employees.objects.filter(id=id).delete()
    except:
        ret['status'] = False
        ret['error'] = 'DB Deleting Error!'
    return HttpResponse(json.dumps(ret))
