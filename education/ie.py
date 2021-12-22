import datetime
import pandas
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
from math import ceil, floor


students_count = 120
group_size = 40


def calculate(group_size):
    groups_count = ceil(students_count / group_size)
    lecturer_week_classes = 10
    student_week_classes = 16
    lecturer_max_lessons = 3
    lecturer_distribution_rate = 1.5
    classes_per_day_limit = 5.5
    study_days = 6

    data_frame = pandas.read_excel('hours1.ods')
    subject_count = len(data_frame.index)
    study_hours_total = sum([ceil(subject['hours']/2) for subject in data_frame.to_dict(orient='index').values()])
    weeks_to_study = study_hours_total/(study_days*classes_per_day_limit)
    months_to_study = weeks_to_study/4
    semesters_to_study = round(months_to_study/4)
    print(semesters_to_study)
    months_to_pay = semesters_to_study*6

    lecturers_count_by_lessons = lecturer_distribution_rate * \
        subject_count / lecturer_max_lessons
    lecturers_count_by_schedule = groups_count * \
        student_week_classes / lecturer_week_classes

    lecturers_count = ceil(max(lecturers_count_by_lessons, lecturers_count_by_schedule))

    classes_per_week_total = groups_count*student_week_classes
    lecture_classes_ratio = 0.4
    practice_classes_ratio = 0.6
    lecture_classes_total = lecture_classes_ratio*classes_per_week_total
    practice_classes_total = practice_classes_ratio*classes_per_week_total
    lecture_classes_per_day_total = lecture_classes_total/study_days
    practice_classes_per_day_total = practice_classes_total/study_days
    lecture_classes_simuliatenesly = lecture_classes_per_day_total/classes_per_day_limit
    practice_classes_simuliatenesly = practice_classes_per_day_total/classes_per_day_limit
    lecture_rooms = ceil(lecture_classes_simuliatenesly)
    practice_rooms = ceil(practice_classes_simuliatenesly)
    practice_area_per_person = 3
    lecture_area_per_person = 2
    free_space_ratio = 1.2
    practice_rooms_area = ceil(practice_rooms*group_size*practice_area_per_person*free_space_ratio)
    max_lecture_room_capacity = 40
    lecture_rooms_area = ceil(lecture_rooms*floor(max_lecture_room_capacity/groups_count)*group_size*lecture_area_per_person*free_space_ratio)
    classes_area = practice_rooms_area+lecture_rooms_area

    service_rooms = 20
    toilets = 10*2
    wardrobe = 15
    lecturers_area = 4*lecturers_count
    total_area = classes_area + service_rooms + toilets + wardrobe + lecturers_area
    total_area = ceil(total_area * 1.1)




    class SubscriptionService:
        def __init__(self, name: str, payment: int, period: relativedelta):
            self.name = name
            self.period = period
            self.payment = payment
            self.inflation_rate = 1.057

        def get_periods(self):
            years = self.period.years
            months = years*12+self.period.months
            if self.period.months != 0: years=years+1
            return months, years

        def summary_payment_for(self):
            total = 0
            price = self.payment
            months, years = self.get_periods()
            for i in range(years):
                if months - 12 > 0:
                    total = total + price*12
                    price = price * self.inflation_rate
                    months = months - 12
                else:
                    total = total + price*months
            return total

    class Employee(SubscriptionService):
        def __init__(self, name: str, payment: int, period: relativedelta):
            super().__init__(name, payment, period)
            self.tax_rate = 30.1/100

        def summary_payment_for(self):
            total = 0
            payment_rate = 1 - self.tax_rate
            price = self.payment/payment_rate        
            months, years = self.get_periods()
            for i in range(years):
                if months - 12 > 0:
                    total = total + price*12
                    months = months - 12
                else:
                    total = total + price*months
            return total


    users_count = lecturers_count + students_count
    payment_per_user = 180
    summary_teams_payment = users_count * payment_per_user

    general_expences = []
    offline_expences = []
    online_expences = []

    general_expences.append(SubscriptionService(
        name='microsoft teams and office', 
        payment=summary_teams_payment, 
        period=relativedelta(months=months_to_pay)))
    general_expences.append(SubscriptionService(
        name='internet',
        payment=15000, 
        period=relativedelta(months=months_to_pay)))
    general_expences.append(SubscriptionService(
        name='1c',
        payment=1800, 
        period=relativedelta(months=months_to_pay)))
    general_expences.append(SubscriptionService(
        name='Chancellery',
        payment=5000, 
        period=relativedelta(months=months_to_pay)))

    general_expences.extend([Employee(
        name='Administrator',
        payment=50000, 
        period=relativedelta(months=months_to_pay)) for i in range(2)])
    general_expences.extend([Employee(
        name='Methodist',
        payment=44000, 
        period=relativedelta(months=months_to_pay)) for i in range(2)])
    general_expences.extend([Employee(
        name='Lector',
        payment=44000, 
        period=relativedelta(months=months_to_pay)) for i in range(lecturers_count)])



    offline_expences.append(SubscriptionService(
        name='Office rent',
        payment=600*total_area, 
        period=relativedelta(months=months_to_pay)))
    offline_expences.append(SubscriptionService(
        name='Equipment and rooms upgrades',
        payment=15*total_area, 
        period=relativedelta(months=months_to_pay)))
    offline_expences.append(SubscriptionService(
        name='Site and digital services',
        payment=10000, 
        period=relativedelta(months=months_to_pay)))
    offline_expences.extend([Employee(
        name='Cleaning',
        payment=25000, 
        period=relativedelta(months=months_to_pay)) for i in range(2)])
    offline_expences.extend([Employee(
        name='Wardrober',
        payment=13000, 
        period=relativedelta(months=months_to_pay))])


    online_expences.append(SubscriptionService(
        name='Site and digital services',
        payment=25000, 
        period=relativedelta(months=months_to_pay)))

    online_expences.extend(general_expences)
    offline_expences.extend(general_expences)

    total_online = 0
    for expence in online_expences:
        total_online =  total_online + expence.summary_payment_for()

    total_offline = 0
    for expence in offline_expences:
        total_offline = total_offline + expence.summary_payment_for()

    total_offline_per_student = total_offline/students_count
    total_online_per_student = total_online/students_count

    offline_payment = total_offline_per_student/semesters_to_study
    online_payment = total_online_per_student/semesters_to_study
    return offline_payment, online_payment

group_sizes = np.arange(3, 40, 1)
res = [calculate(size) for size in group_sizes]
offline_prices = [elem[0] for elem in res]
online_prices = [elem[1] for elem in res]
plt.plot(group_sizes, offline_prices, 'g')
plt.plot(group_sizes, online_prices, 'b')
plt.show()
