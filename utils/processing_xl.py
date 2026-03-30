import pandas as pd
import matplotlib.pyplot as plt
#Предпросмотр данных

df = pd.read_excel(r"C:\Users\Анастасия\OneDrive\Desktop\[SW.BAND] Hr data_monetary.xlsx")

columns = df.columns.tolist() # Название всех колонок в датасете (для удобства)

count_man = ((df['Gender'] == 'Male').sum()) # Кол-во мужчин всего (882)
count_woman = ((df['Gender'] == 'Female').sum()) # Кол-во женщин всего (588)

avg_age_man = df[df['Gender'] == 'Male']['Age'].mean() # Средний возраст мужчин (36)
avg_age_woman = df[df['Gender'] == 'Female']['Age'].mean() # Средний возраст женщин (37)

unique_users = df['EmployeeNumber'].nunique() # Уникальные значения

grouped = df.groupby('EmployeeNumber')['ProjectsClosed'].sum() # Сколько закрытых проектов у каждого сотрудника
avg_grouped = df['ProjectsClosed'].mean() # В среднем закрытых проектов на одного сотрудника
department = (df['Department'].unique()) # Отделы ['Sales', 'Research & Development', 'Human Resources']
sum_by_department = df.groupby('Department')['ProjectsClosed'].sum() # Kол-во закрытых проектов для каждого отдела
avg_by_department = df.groupby('Department')['ProjectsClosed'].mean() # Среднее кол-во закрытых проектов для каждого отдела


# id сотрудников, чьё ProjectsClosed выше среднего
id_employees = set()
avg = df['ProjectsClosed'].mean()
for i, j in df.groupby('EmployeeNumber')['ProjectsClosed']:
    for n in j:
        if n > avg:
            id_employees.add(i)
#print(sorted(id_employees))


# % > avg — процент сотрудников, которые закрыли проектов выше среднего
total_rows = len(df)
avg = df['ProjectsClosed'].mean()
above_avg = (df['ProjectsClosed'] > avg).sum()
res = above_avg / total_rows
#print(res)


# Распределение премии по сотрудникам (просмотр возможных процентов)
lst = []
for i in df['PerformanceRating']:
    for j in df['ProjectsClosed']:
        if i == 5 and j > 5:
            lst.append("20%")
        elif i == 4 and j > 3:
            lst.append("12%")
        else:
            lst.append("5%")


# Сотрудники, у которых >= 15 закрытых проектов
total_kpi = len(df)
lst_kpi = [] # >= 15 закрытых проектов (id)
for i, j in df.groupby('EmployeeNumber')['ProjectsClosed']:
    for n in j:
        if n >= 15:
            lst_kpi.append(i)
procent_kpi = f'{len(lst_kpi) / total_kpi:.2%}'


# Среднее кол-во проектов на сотрудника среди "успешных"
kpi_closed = (df['ProjectsClosed']).sum() # Всего закрытых проектов
set_kpi = set() # >= 15 закрытых проектов (id)
for i, j in df.groupby('EmployeeNumber')['ProjectsClosed']:
    for n in j:
        if n >= 15:
            set_kpi.add(i)
res_kpi = kpi_closed / len(set_kpi)


#==============ВИЗУАЛИЗАЦИЯ============

# Кол-во мужчин и женщин
categories = ['Мужчины', 'Женщины']
values = [count_man, count_woman]
plt.bar(categories, values, color=['skyblue', 'salmon'])
plt.title('Распределение сотрудников по полу')
plt.ylabel('Человек')
#plt.show()

# Средний возраст
categories_age = ['Мужчины', 'Женщины']
values_age = [avg_age_man, avg_age_woman]
plt.bar(categories_age, values_age, color=['skyblue', 'salmon'])
plt.title('Средний возраст сотрудников (мужчины/женщины')
plt.ylabel('Лет')
#plt.show()


# Закрытые проекты сотрудников
plt.boxplot(df['ProjectsClosed'])
plt.title('Разброс закрытых проектов по сотрудникам')
plt.ylabel('Закрытые проекты')
#plt.show()


# Закрытые проекты (по отделам)
grouped = df.groupby('Department')['ProjectsClosed'].sum()
categories = grouped.index.tolist()
values = grouped.values.tolist()
plt.bar(categories, values, color=['thistle', 'steelblue', 'seagreen'])
plt.title('Закрытые проекты по отделам')
plt.xlabel('Отделы')
plt.ylabel('Проектов')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()


# Процент сотрудников, закрывших >= 15 проектов
labels = ['>= 15 проектов', 'Остальные']
values = (len(lst_kpi), total_kpi - len(lst_kpi))
colors = ['#8DA47E', '#D3D3D3']
plt.pie(values, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90)
plt.title('Доля сотрудников, закрывших >= 15 проектов')
#plt.show()