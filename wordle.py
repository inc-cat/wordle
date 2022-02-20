import os
import csv
import datetime
from fpdf import FPDF
from matplotlib import pyplot
from PyPDF2 import PdfFileMerger


# wordle + info .csv is loaded and the information is put into a list within
# the scores variable. . errors are also caught if file isn't present or correct
try:
    with open('wordle.csv') as source_file:
        source_material = csv.reader(source_file)
        data = list(source_material)
        try:
            scores = list(map(int ,data[0]))
        except ValueError:
            print('Error! \nNumbers only accepted in wordle.csv')
            exit()

except FileNotFoundError:
    print('Error! \nwordle.csv required in the directory.')
    exit()

try:
    with open('info.csv') as date_source:
        date_read = csv.reader(date_source)
        d_skip = list(date_read)
except FileNotFoundError:
    print('info.csv required in the directory.')

# number of games taken from the scores list to be used
sample_size = len(scores)

# getting averaes for 7 times and ever play up until that point by getting
# the mean, an extra if else function to differenceiate ints and floats
seven_average = []

for get_seven in range(sample_size):
    if get_seven == 0:
        seven_average.append(scores[0])
    elif 0 < get_seven < 7:
        under_seven = scores[0:get_seven + 1]
        if (sum(under_seven) / (get_seven + 1)) % 1 ==0:
            seven_average.append(int(sum(under_seven) / (get_seven + 1)))
        else:
            seven_average.append(sum(under_seven) / (get_seven + 1))
    else:
        seven_plus = scores[get_seven - 6:get_seven + 1]
        if (sum(seven_plus) / 7) % 1 ==0:
            seven_average.append(int(sum(seven_plus) / 7))
        else:
            seven_average.append(sum(seven_plus) / 7)

all_average = []
for get_all in range(sample_size):
    current_num = scores[0:get_all + 1]
    limited_sample = len(current_num)

    if sum(current_num) / limited_sample %1 ==0:
        all_average.append(int(sum(current_num) / limited_sample))
    else:
        all_average.append(sum(current_num) / limited_sample)

# taking the data from the info csv to create the dates using the datetime
# module. as the csv file has everything as a string, it is split and
# converted to int before being added to datetime.date
date_cycle = []
try:
    # values from the csv first line for t
    first_year = int(d_skip[0][0][0:4])
    first_month = int(d_skip[0][0][4:6])
    first_day = int(d_skip[0][0][6:8])

    first_date = datetime.date(first_year, first_month, first_day)

# skip dates taken from the third line of info.csv

    skip_dates = []
    for build_skips in d_skip[1]:
        skip_year = int(build_skips[0:4])
        skip_month = int(build_skips[4:6])
        skip_day = int(build_skips[6:8])
        skip_dates.append(datetime.date(skip_year, skip_month, skip_day))
except ValueError:
    print('Error! \nIncorrect date input, YYYYMMDD only.')

skip_amount = len(skip_dates)

# adding all dates to list corresponding to score
# overscore is to account for skips which will be deleted
overscore = len(scores) + skip_amount
for line_cycles in range(overscore):
    next_day = datetime.timedelta(line_cycles)
    date_cycle.append(first_date + next_day)



# deleting indexes of skips in reverse order
del_index = []
try:
    for index_del in skip_dates:
        del_index.append(date_cycle.index(index_del))
except ValueError:
    print('Error! \nIncorrect date input')

del_index.sort(reverse=True)

for remove_skips in del_index:
    del date_cycle[remove_skips]


last_date = date_cycle[-1]

x_axis = [i for i in range(sample_size)]
y_average = seven_average
y_score = scores

pyplot.text(0, -7, 'test!')
pyplot.xlabel('Day number')
pyplot.ylabel('Score')
pyplot.plot(x_axis, y_average, color='#000000', marker='o',
    label='7 streak average')
pyplot.plot(x_axis, all_average, color='#123456', linestyle='dashed',
    marker = 'o', label='Complete average')
pyplot.bar(x_axis, y_score, color='#097969', label='Score')
pyplot.title('Wordle')
pyplot.legend()


pyplot.savefig('page1.pdf')

# pyplot.show()
pyplot.close()

# calculating percentages for each guess. . . (partially unused)

guess_count = []
x_guess = []
guess_percent = []
for attempt_count in range(1,7):
    guess_count.append(scores.count(attempt_count))
    x_guess.append(attempt_count)
    current_percent = scores.count(attempt_count) / sample_size * 100
    if current_percent % 1 ==0:
        guess_percent.append(int(current_percent))
    else:
        guess_percent.append(round(current_percent, 2))

# plotting first graph

pyplot.xlabel('Number of attempts')
pyplot.ylabel('Number of games')
pyplot.bar(x_guess, guess_count, color='#097969', label='Score')

pyplot.savefig('page2.pdf')
# pyplot.show()
pyplot.close()


week_bound = sample_size - 7

# added averages done here
avs = []
for average_yeild in range(week_bound):
    seven_selection = scores[average_yeild:average_yeild+7]
    average_seven = sum(seven_selection) / 7
    avs.append(average_seven)

max_av = min(avs)
day_ind = avs.index(max_av)

player_name = d_skip[2][0]

# text pdf created here using data collected

pdf = FPDF('P', 'mm', (163, 122))
pdf.add_page()
pdf.set_font('helvetica', 'U', 20)
pdf.cell(0, 10, 'Statistics for ' + player_name, ln=True)
pdf.set_font('helvetica', '', 12)


start_date = 'Start date: ' + \
    str(first_year) + '/' + str(first_month) + '/' + str(first_day)
final_day = str(last_date.strftime('%d'))
if len(final_day) == 2 and final_day[0] == '0':
    final_day = final_day[1]
final_month = str(last_date.strftime('%m'))
if len(final_month) == 2 and final_month[0] == '0':
    final_month = final_month[1]
final_year = str(last_date.strftime('%Y'))
final_date = 'End date: ' + final_year + '/' + final_month + '/' + final_day
total_games = 'Total times played: ' + str(sample_size)
total_skips = 'Total skipped days: ' + str(skip_amount)
total_guesses = 'Total guesses: ' + str(sum(scores))
best_streak = 'Best 7 game average: Game starting number ' + str(day_ind + 1)


average_number = sum(scores) / len(scores)

average_guess = 'Average guess amount: ' + str(round(average_number, 2))

streak_date = date_cycle[day_ind]
streak_day = str(streak_date.strftime('%d'))
if len(streak_day) == 2 and streak_day[0] == '0':
    streak_day = streak_day[1]
streak_month = str(streak_date.strftime('%m'))
if len(streak_month) == 2 and streak_month[0] == '0':
    streak_month = streak_month[1]
streak_year = str(streak_date.strftime('%Y'))

streak_date = 'Date starting: ' + streak_year + '/' + streak_month + '/' + \
    streak_day


text_lines = (
    start_date, final_date, total_games,
    total_skips, total_guesses, average_guess,
    best_streak, streak_date
    )


for pdf_lines in text_lines:
    pdf.cell(0, 5, pdf_lines, ln=True)

pdf.output('page3.pdf')

# merges all 3 pages together for final product

pdfs = ['page1.pdf', 'page2.pdf', 'page3.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()

# removes all redundant pdfs after merge has been completed
for deadwood in pdfs:
    os.remove(deadwood)

# by Anwar Louis
