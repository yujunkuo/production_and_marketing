from django.shortcuts import render
import datetime
from production.models import *


def orderSystem(request):
    return render(request, "orderSystem.html")


def checkSystem(request):
    return render(request, "checkSystem.html")

def provideSystem(request):
    return render(request, "provideSystem")

def stockCheck(request):
    return render(request, "stockCheck.html")

def equipmentCheck(request):
    return render(request, "equipmentCheck.html")

def stockProvide(request):
    return render(request, "stockProvide.html")

def equipmentProvide(request):
    return render(request, "equipmentProvide.html")

dish_dict = {'拿鐵咖啡': {'牛奶': 1, '咖啡': 1}, '巧克力冰淇淋鬆餅': {'巧克力': 1, '冰淇淋': 1, '鬆餅粉': 1},
             '挪威燻鮭魚沙拉': {'鮭魚': 1, '萵苣': 2, '番茄': 3, '麵包丁': 2, '沙拉醬': 1}}

# Create your views here.
def join_member(x: str, y: str, z: int, w: str, r: datetime, t: bool, q: bool, o:int):
    '''name = request.Get.get()
    gender = request.Get.get()
    phone = request.Get.get()
    email = request.Get.get()
    bday = request.Get.get()
    pets = request.Get.get()
    student = request.Get.get()'''
    name = x
    gender = y
    phone = z
    email = w
    bday = r
    pets = t
    student = q
    id = o

    Member.objects.create(mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                          , Student=student, MemberID=id)
    '''if Member.objects.filter(mName__isnull = True):
        members=Member.objects.filter(mName__isnull = True)
        member_choose = members[0]
        member_choose.Name = name
        member_choose.Gender = gender
        member_choose.Phone = phone
        member_choose.Email = email
        member_choose.BDay = bday
        member_choose.Pets = pets
        member_choose.Students = student
        member_choose.save()
    else:
        Member.objects.create(mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                              , Student=student)'''
    new_member = Member.objects.get(MemberID=id)
    return new_member


def order(request):
    mid = request.Get.get('Member ID')
    dish = request.Get.get('Dish_Name')
    num = request.Get.get('Dish num')

    try:
        mid = Member.objects.get(MemberID=mid)
    except Member.DoesNotExit:
        Member.objects.create(MemberID=mid)

    Order.objects.create(oTime=time, MID=Member.objects.get(MemberID=mid),
                         dishName=Dish.objects.get(dName=dish), orderNum=num)

    for i in dish_dict[dish]:
        stock = i
        stock_db = Stock.objects.filter(sName=stock).orderby('Expired')
        used_num = dish_dict[dish][i]

        for j in len(stock_db):
            if not stock_db[j].sNum <= used_num:
                stock_db[j].sNum -= used_num
                stock_db[j].save()
                break
            else:
                used_num -= stock_db[j].sNum
                stock_db[j].sNum = 0
                stock_db[j].save()
        Stock.objects.filter(sNum=0).delete

    Made.objects.create(mDish=Dish.objects.get(dName=dish), mStock=Stock.objects.get(sName=stock), mNum=used_num)

    success_msg = 'Finish Ordering'
    return success_msg

def check_stock_all():
    result = Stock.objects.order_by('Expired')
    return result


def check_stock_expired(request):
    name = request.Get.get('Check Stock')
    result = Stock.objects.get(sName=name).order_by('Expired')
    return result


def check_equip_all():
    result = Equipment.objects.all()
    return result


def check_stock_need():
    result = Stock.objects.get(sNum__lt=20)
    return result


def check_equip_need():
    result = Equipment.objects.get(eNum__lt=10)
    return result


def provide_stock(x: str, y: int, z: datetime, w: int, p: int):
    # name = request.Get.get('Provide Stock Name')
    # firm = request.Get.get('Provide Stock Firm')
    # num = request.Get.get('Provide Stock Num')
    # expired = request.Get.get('Stock Expired Date')
    name = x
    firm = y
    expired = z
    num = w

    try:
        Firm.objects.get(FirmID=firm)
    except Firm.DoesNotExist:
        Firm.objects.create(FirmID=firm)

    Stock.objects.create(sName=name, sNum=num, Expired=expired)
    ProvideStock.objects.create(psFirm=Firm.objects.get(FirmID=firm), name=Stock.objects.get(sName=name),
                                psNum=num)

    SuccessMSG = 'Successfully Update Stock'
    return SuccessMSG


def provide_equip(request):
    name = request.Get.get('Provide Equipment Name')
    firm = request.Get.get('Provide Equipment Firm')
    num = request.Get.get('Provide Equipment Num')

    try:
        Firm.objects.get(FirmID=firm)
    except Firm.DoesNotExit:
        Firm.objects.create(FirmID=firm)

    try:
        Equipment.objects.get(eName=name)
    except Equipment.DoesNotExit:
        Equipment.objects.create(eName=name, eNum=0)

    equip = Equipment.objects.get(eName=name)
    origin_num = equip.eNum
    new_num = origin_num + num
    equip.eNum = new_num
    equip.save()

    ProvideEquip.objects.create(peFirm=Firm.objects.get(FirmID=firm), pEquip=Equipment.objects.get(eName=name)
                                , peNum=num)

    success_msg = 'Successfully Update Equipment'
    return success_msg


Dish_List = ['拿鐵咖啡', '香草拿鐵', '濃縮咖啡', '卡布奇諾', '焦糖瑪奇朵', '提拉米蘇拿鐵', '貝里斯奶酒咖啡', '特調風味鮮奶茶',
             '玫瑰奶茶', '牛奶糖歐蕾', '可可歐蕾', '抹茶阿法其朵', '蜂蜜檸檬', '蜂蜜奇異果', '精選啤酒', '蘋果優格冰沙', 'Oreo巧克力冰沙',
             '宇治抹茶冰沙', '香蕉巧克力冰沙', '青檸冰紅茶', '玫瑰四物茶', '富士蘋果冰茶', '伯爵紅茶', '烏龍鐵觀音', '日式玄米煎茶',
             '燻火腿芝士夾心焗烤土司', '夏威夷比薩芝士焗烤土司', '原味鬆餅','焦糖冰淇淋鬆餅', '巧克力冰淇淋鬆餅', '香蕉冰淇淋鬆餅',
             '藍莓貝果', '奶油貝果', '花生貝果', '焦糖北海道牛奶冰淇淋', '甜心草莓冰淇淋', '酥脆巧克力冰淇淋', '起士可頌', '鮪魚可頌',
             '起士火腿可頌', '黑胡椒牛肉可頌', '蔬菜雞肉可頌', '咖喱雞肉皮塔', '辣味牛肉皮塔', '法式鴨胸皮塔', '挪威燻鮭魚沙拉',
             '燻火腿沙拉', '一杯雞蛋沙拉（素）', '一杯鮪魚沙拉']

def prediction(request):
    name = request.Get.get('Dish name')
    curr = datetime.datetime.now()
    num_per_month = []
    predict_for_month = []

    for year in range(2019, curr.year + 1):
        if year != curr.year:
            for month in range(1, 13):
                if Order.oTime.year == year and Order.oTime.month == month:
                    dish_order = Order.objects.filter(dishName=name)
                    count = 0
                    for _order in dish_order:
                        count += _order.orderNum
                    num_per_month.append(count)
        else:
            for month in range(1, curr.month):
                if Order.oTime.year == year and Order.oTime.month == month:
                    dish_order = Order.objects.filter(dishName=name)
                    count = 0
                    for _order in dish_order:
                        count += _order.orderNum
                    num_per_month.append(count)
    predict_for_month.append(num_per_month[0])

    for i in range(len(num_per_month)-1):
        predict = predict_for_month[i] + 0.15*(predict_for_month[i+1] - predict_for_month[i])
        predict_for_month.append(predict)

    return name, predict[-1]


