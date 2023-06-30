# import required libraries
import pygame
import sys
import datetime
import calendar
from time import sleep
import csv
import pandas as pd
import os

# ================================================================================
# FUTURE FIXES
# ================================================================================
# TODO it would have been better to have built buttons as a reusable class/functions
# TODO it would have been better to have built animations (fade in/out) as reusable class/functions
# TODO it would have been better to have built input boxes as reusable class/functions

# ================================================================================
# INITIAL PYGAME SETUP
# ================================================================================
# initiate pygame and create initial display surface
pygame.init()
screen = pygame.display.set_mode((400, 480))
pygame.display.set_caption('Period Tracker')
logo_image = pygame.image.load('./assets/logo.png')
pygame.display.set_icon(logo_image)

# create a clock object to help set fps
fps_clock = pygame.time.Clock()

# hide the mouse
pygame.mouse.set_visible(False)

# function to pull, rotate, and resize images
def create_image(file, rotate, x, y):
    img = pygame.image.load(file).convert_alpha()
    img = pygame.transform.rotate(img, rotate)
    img = pygame.transform.smoothscale(img, (x, y))
    return img

# set up arrow images
a = 15
b = 22.638
left_arrow_default = create_image('./assets/angle-default.png', 0, a, b)
right_arrow_default = create_image('./assets/angle-default.png', 180, a, b)
left_arrow_hover = create_image('./assets/angle-hover.png', 0, a, b)
right_arrow_hover = create_image('./assets/angle-hover.png', 180, a, b)
left_arrow_click = create_image('./assets/angle-click.png', 0, a, b)
right_arrow_click = create_image('./assets/angle-click.png', 180, a, b)

a = 23
b = 20
down_arrow_default = create_image('./assets/angle-default.png', 90, a, b)
up_arrow_default = create_image('./assets/angle-default.png', 270, a, b)
down_arrow_hover = create_image('./assets/angle-hover.png', 90, a, b)
up_arrow_hover = create_image('./assets/angle-hover.png', 270, a, b)
down_arrow_click = create_image('./assets/angle-click.png', 90, a, b)
up_arrow_click = create_image('./assets/angle-click.png', 270, a, b)

# submit button images
a = 125
b = 69.866
submit_button_default = create_image('./assets/submit_default.png', 0, a, b)
submit_button_hover = create_image('./assets/submit_hover.png', 0, a, b)
submit_button_click = create_image('./assets/submit_click.png', 0, a, b)

# mouse
mouse = create_image('./assets/cursor.png', 0, 40, 40)

# help button images
a = 50
b = 50
help_button_default = create_image('./assets/help_default.png', 0, a, b)
help_button_hover = create_image('./assets/help_hover.png', 0, a, b)
help_button_click = create_image('./assets/help_click.png', 0, a, b)

# x button images
a = 50
b = 50
x_button_default = create_image('./assets/x_default.png', 0, a, b)
x_button_hover = create_image('./assets/x_hover.png', 0, a, b)
x_button_click = create_image('./assets/x_click.png', 0, a, b)

# help window
help_window = create_image('./assets/legend_window.png', 0, 400, 384.27)

# + button images
a = 50
b = 50
add_button_default = create_image('./assets/add_default.png', 0, a, b)
add_button_hover = create_image('./assets/add_hover.png', 0, a, b)
add_button_click = create_image('./assets/add_click.png', 0, a, b)

# add window
add_window = create_image('./assets/add_window.png', 0, 450, 308.25)

# save button images
a = 100
b = 55.893
save_button_default = create_image('./assets/save_default.png', 0, a, b)
save_button_hover = create_image('./assets/save_hover.png', 0, a, b)
save_button_click = create_image('./assets/save_click.png', 0, a, b)

# Create rectangles
mouse_rect = mouse.get_rect(center=(100, 50))
help_window_rect = help_window.get_rect(center=(200, 200))
add_window_rect = add_window.get_rect(center=(200, 168))
left_arrow_rect = left_arrow_default.get_rect(center=(20, 75))
left_arrow_image = left_arrow_default
right_arrow_rect = right_arrow_default.get_rect(center=(375, 75))
right_arrow_image = right_arrow_default
data_arrow_rect = down_arrow_default.get_rect(center=(160, 312))
data_arrow_image = down_arrow_default
submit_button_rect = submit_button_default.get_rect(center=(200, 320))
submit_button_image = submit_button_default
help_button_rect = help_button_default.get_rect(center=(370, 30))
help_button_image = help_button_default
x_button_rect = x_button_default.get_rect(center=(280, 110))
x_button_image = x_button_default
add_button_rect = add_button_default.get_rect(center=(330, 30))
add_button_image = add_button_default
save_button_rect = save_button_default.get_rect(center=(200, 225))
save_button_image = save_button_default

# Create states for building the display screen and interacting with it
# Set up initial disclaimer state to load first every launch
current_state = 'disclaimer'
# new - on first launch, must create csv and get last period info
# general - home screen with calendar and data section
# disclaimer - on every launch, display disclaimer window first
pop_up = 'none'
# none - no pop-ups, just the main screen
# help - for when user clicks on the help button
# add - for adding a new period

# ================================================================================
# COLORS AND FONTS
# ================================================================================
# create font objects
title_font = pygame.font.Font('./fonts/junction-regular.ttf', 25)
body_font = pygame.font.Font('./fonts/junction-regular.ttf', 15)

# create color swatches
rgb_light_gray = (234, 234, 234)
rgb_mid_gray = (173, 173, 173)
rgb_dark = (37, 42, 52)
rgb_light_pink = (255, 223, 223)
rgb_dark_pink = (251, 146, 158)
rgb_bright_pink = (255, 46, 99)
rgb_light_blue = (174, 222, 252)
rgb_blue = (0, 90, 141)
rgb_turquoise = (8, 217, 214)
rgb_white = (255, 255, 255)


# ================================================================================
# INITIAL DATES SETUP
# ================================================================================
today = datetime.date.today()
week_days = body_font.render('SUN    MON    TUE   WED   THU     FRI    SAT', True, rgb_dark)
use_date = today
# use date - builds the calendar based on a target date

# default values
# we need to build a list of rectangles where the dates are located to interact with
# sets the default values for building the hover box
date_rects = []
hover_color = rgb_white
hover_x = 0
hover_y = 0
hover_w = 0
hover_h = 0

# function for pulling and visualizing dates
def pull_dates(start_date, x, y, w, h, df_dates):
    date_rects = []

    # get target month, target year, and grab applicable dates for the calendar
    month = start_date.month
    year = start_date.year
    cal = calendar.Calendar(6)
    date_iterable = cal.itermonthdates(year, month)
    date_list = list(date_iterable)

    # for determining where to locate the rect and when to create a new row
    a = 0
    b = x

    # pull applicable ovulation dates from the data frame (can have multiple in one month window)
    ov_list = []
    for index, row in df_dates.iterrows():
        check_date = row['Start']
        # convert date to date object if it was stored as a string
        if type(check_date) == str:
            check_date = datetime.datetime.strptime(check_date, '%Y-%m-%d').date()
        # checking for NaN, default to use is average
        if row['Distance'] == row['Distance']:
            dis = row['Distance']
        else:
            dis = ave_dis
        # determine ovulation date based on row's info, add to list to use if it falls in the target date window
        o_date = check_date + datetime.timedelta(days=(dis / 2))
        if o_date.year == year and (month - 1) <= o_date.month <= (1 + month):
            ov_list.append(o_date)

    # pull applicable period dates from the data frame (can have multiple in one month window)
    p_list = []
    for index, row in df_dates.iterrows():
        # pull start and finish dates and convert to dates if stored as strings
        start_check = row['Start']
        if type(start_check)==str:
            start_check = datetime.datetime.strptime(start_check, '%Y-%m-%d').date()
        finish_check = row['Finish']
        if type(finish_check)==str:
            finish_check = datetime.datetime.strptime(finish_check, '%Y-%m-%d').date()
        # if they fall out in the target date window, add the info to the list of what to use
        if (start_check.year == year and (month - 1) <= start_check.month <= (month + 1)) or (finish_check.year == year and (month - 1) <= finish_check.month <= (month + 1)):
            len = row['Length']
            p_list.append((start_check, finish_check, len))

    for d in date_list:
        # default gray font
        font_color = rgb_mid_gray

        # previous month data will be light gray
        if not month == date_list[a].month:
            font_color = rgb_light_gray

        # check ovulation data, dark blue for actual est. date, light blue for est. window
        for o_date in ov_list:
            if date_list[a] == o_date:
                font_color = rgb_blue
            elif (o_date - datetime.timedelta(days=1)) <= date_list[a] <= (o_date + datetime.timedelta(days=1)):
                font_color = rgb_light_blue

        # check period data, lighter pink for lighter flow days, darker pink for heavier flow
        for p_item in p_list:
            p_start = p_item[0]
            p_len = p_item[2]-1
            r = p_len % 3
            k = (p_len - r) / 3
            if (p_start + datetime.timedelta(days=k)) <= date_list[a] <= (p_start + datetime.timedelta(days=2 * k + r)):
                font_color = rgb_bright_pink
            elif p_start <= date_list[a] <= (p_start + datetime.timedelta(days=p_len)):
                font_color = rgb_dark_pink

        # check for today's date, color will be dark gray
        if date_list[a] == datetime.date.today():
            font_color = rgb_dark

        # render the text and create the rectangles for the hover box to interact with
        # text rectangles and the date rectangles generate differently (center vs corner) so x and y are offset
        text = body_font.render(str(date_list[a].day), True, font_color)
        text_rect = text.get_rect(center=(x, y))
        new_rect = pygame.draw.rect(screen, rgb_white, (x-13, y-14, w, h), 0)
        date_rects.append(new_rect)
        screen.blit(text, text_rect)
        x += w
        a += 1
        if a % 7 == 0:
            x = b
            y += h
    return date_rects


# ================================================================================
# INITIAL CSV FILE PULL AND DATAFRAME SETUP
# ================================================================================
# Default values to set up animations
data_expand = False
grow_rate_rect = 4
grow_rate_line = 10
current_height = 60
current_width = 0
alpha = 255
grow_alpha = 10
intro_alpha = 255
intro_grow = 10
start_default = 'mm/dd/yyyy'
finish_default = 'mm/dd/yyyy'
start_text = start_default
finish_text = finish_default
start_text_color = rgb_mid_gray
finish_text_color = rgb_mid_gray

# Default file name
working_file = 'mydata.csv'


# FUNCTIONS
# PROJECT NEXT PERIOD DATE
# note - usually we end up calling this twice to account for if a month had two periods
#        (if we shift to the next month, we want to make sure we capture all possible periods in that month)
def project_next(initial_df):
    # pull the last start date and convert to date if stored as string
    last_start = initial_df['Start'].iloc[-1]
    if type(last_start) == str:
        last_start = datetime.datetime.strptime(last_start, '%Y-%m-%d').date()
    # estimate the next start and finish date based on averages and add it to the dataframe
    new_start = last_start + datetime.timedelta(days=int(ave_dis))
    new_finish = new_start + datetime.timedelta(days=int(ave_len-1))
    initial_df.loc[len(initial_df.index)] = [new_start, new_finish, ave_len, ave_dis]


# ADD DATA TO THE CSV
def add_data_csv(start, finish):
    # determine the length
    length = 1 + (finish - start).days

    # reload the dataframe to start clean and overwrite projected data with actual data
    df_reload = pd.read_csv(working_file)

    # if there is only one row in the data sheet, default to average distance otherwise calculate distance
    if len(df_reload) > 0:
        last_start = df_reload['Start'].iloc[-1]
        if type(last_start) == str:
            last_start = datetime.datetime.strptime(last_start, '%Y-%m-%d').date()
        distance = 1 + (start - last_start).days
        with open(working_file, 'a', newline='') as file:
            new_writer = csv.writer(file)
            new_field = [start, finish, length, distance]
            new_writer.writerow(new_field)
    else:
        with open(working_file, 'a', newline='') as file:
            new_writer = csv.writer(file)
            new_field = [start, finish, length, ave_dis]
            new_writer.writerow(new_field)

# Set up initial disclaimer state with animations and messages
title_message = title_font.render('DISCLAIMER', True, rgb_bright_pink)
logo_rect = logo_image.get_rect(center=(200, 100))
a = 255
a_two = 0
grow_a = 1
initial = True


# ================================================================================
# MAIN PYGAME LOOP
# ================================================================================
# create the primary loop
while True:
    # ===============================================================================
    # HANDLING EVENTS
    # ===============================================================================
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # locate mouse, check for collisions
        if event.type == pygame.MOUSEMOTION:
            mouse_rect = mouse.get_rect(center=event.pos)

            # check for collisions with the arrow buttons
            if current_state == 'general' and pop_up == 'none':

                # check arrows for collision to set them to hover image
                if left_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    left_arrow_image = left_arrow_hover
                else:
                    left_arrow_image = left_arrow_default

                if right_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    right_arrow_image = right_arrow_hover
                else:
                    right_arrow_image = right_arrow_default

                if data_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    if data_expand:
                        data_arrow_image = up_arrow_hover
                    else:
                        data_arrow_image = down_arrow_hover
                else:
                    if data_expand:
                        data_arrow_image = up_arrow_default
                    else:
                        data_arrow_image = down_arrow_default

                # check for date collisions
                for date_rect in date_rects:
                    if date_rect.collidepoint(pygame.mouse.get_pos()):
                        hover_x = date_rect.x
                        hover_y = date_rect.y

                # check for the help and add buttons
                if help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    help_button_image = help_button_hover
                else:
                    help_button_image = help_button_default

                if add_button_rect.collidepoint(pygame.mouse.get_pos()):
                    add_button_image = add_button_hover
                else:
                    add_button_image = add_button_default

            if pop_up == 'help' or pop_up == 'add':
                if x_button_rect.collidepoint(pygame.mouse.get_pos()):
                    x_button_image = x_button_hover
                else:
                    x_button_image = x_button_default

            if pop_up == 'add':
                if save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    save_button_image = save_button_hover
                else:
                    save_button_image = save_button_default

            if current_state == 'new':
                # check for submit button collisons
                if submit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    submit_button_image = submit_button_hover
                else:
                    submit_button_image = submit_button_default

            # elif current_state == 'add':
            # TODO add the new period screen

        # check for clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_state == 'general' and pop_up == 'none':
                # arrow buttons to check for hover
                # left and right arrows will shift the dates by one month
                # the down arrow on the data frame will expand/collapse the data section
                if left_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    left_arrow_image = left_arrow_click
                    use_date = use_date - datetime.timedelta(days=31)
                if right_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    right_arrow_image = right_arrow_click
                    use_date = use_date + datetime.timedelta(days=31)
                    project_next(df)
                    project_next(df)
                if data_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    if data_expand:
                        data_arrow_image = up_arrow_click
                        data_expand = False
                    else:
                        data_arrow_image = down_arrow_click
                        data_expand = True
                if help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    help_button_image = help_button_click
                    pop_up = 'help'
                if add_button_rect.collidepoint(pygame.mouse.get_pos()):
                    add_button_image = add_button_click
                    pop_up = 'add'
                    start_color = rgb_dark
                    finish_color = rgb_dark
                    start_text = start_default
                    finish_text = finish_default
                    start_text_color = rgb_mid_gray
                    finish_text_color = rgb_mid_gray
                    start_box = pygame.Rect(200, 135, 100, 25)
                    finish_box = pygame.Rect(200, 165, 100, 25)
                    display_error = False

            if pop_up == 'help' or pop_up == 'add':
                if x_button_rect.collidepoint(pygame.mouse.get_pos()):
                    x_button_image = x_button_click
                    pop_up = 'none'

            if pop_up == 'add':
                # save button
                if save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    save_button_image = save_button_click

                    # check for data being correctly filled out
                    # if not correct, highlight that field pink and flag false for adding the data
                    add_to_file = True
                    if start_text == '':
                        start_text = start_default
                        start_color = rgb_bright_pink
                        start_active = False
                        add_to_file = False
                    else:
                        try:
                            start_date = datetime.datetime.strptime(start_text, '%m/%d/%Y').date()
                        except ValueError:
                            start_color = rgb_bright_pink
                            start_active = False
                            add_to_file = False

                    if finish_text == '':
                        finish_text = finish_default
                        finish_color = rgb_bright_pink
                        finish_active = False
                        add_to_file = False
                    else:
                        try:
                            finish_date = datetime.datetime.strptime(finish_text, '%m/%d/%Y').date()
                        except ValueError:
                            finish_color = rgb_bright_pink
                            finish_active = False
                            add_to_file = False

                    # add_to file if data was okay, otherwise display error message
                    if add_to_file:
                        # add new info to the file
                        add_data_csv(start_date, finish_date)

                        # repull the data frame with the new info, overwriting projected info
                        df = pd.read_csv(working_file)

                        # recalc averages and key dates
                        ave_len = round(df['Length'].mean(), 1)
                        ave_dis = round(df['Distance'].mean(), 1)
                        last_date = df['Start'].iloc[-1]
                        if type(last_date) == str:
                            last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d').date()
                        ov_date = last_date + datetime.timedelta(days=int(ave_dis / 2))
                        period_date = last_date + datetime.timedelta(days=int(ave_dis))
                        project_next(df)
                        project_next(df)
                        data_expand = False
                        use_date = datetime.date.today()
                        pop_up = 'none'

                    else:
                        display_error = True

                # input boxes - if clicked, set to active and highlight the box
                # if a user has edited the default info, update the text color
                # if it is default info, clear it out for initial data entry
                if start_box.collidepoint(pygame.mouse.get_pos()):
                    start_active = True
                    start_color = rgb_turquoise
                    start_text_color = rgb_turquoise
                    if start_text == start_default:
                        start_text = ''
                else:
                    if start_text == start_default:
                        start_text_color = rgb_mid_gray
                    elif start_text == '':
                        start_text_color = rgb_mid_gray
                        start_text = start_default
                        start_color = rgb_dark
                    elif start_active == True:
                        start_text_color = rgb_dark
                        start_color = rgb_dark
                    start_active = False

                if finish_box.collidepoint(pygame.mouse.get_pos()):
                    finish_active = True
                    finish_color = rgb_turquoise
                    finish_text_color = rgb_turquoise
                    if finish_text == finish_default:
                        finish_text = ''
                else:
                    if finish_text == finish_default:
                        finish_text_color = rgb_mid_gray
                    elif finish_text == '':
                        finish_text_color = rgb_mid_gray
                        finish_text = finish_default
                        finish_color = rgb_dark
                    elif finish_active == True:
                        finish_text_color = rgb_dark
                        finish_color = rgb_dark
                    finish_active = False

            if current_state == 'new':
                # submit button
                if submit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    submit_button_image = submit_button_click

                    # check for all data being correctly filled out
                    # if not correct, highlight that field pink and flag false for file creation
                    create_file = True

                    if start_text == '':
                        start_color = rgb_bright_pink
                        start_text = start_default
                        start_active = False
                        create_file = False
                    else:
                        try:
                            start_date = datetime.datetime.strptime(start_text, '%m/%d/%Y').date()
                        except ValueError:
                            start_color = rgb_bright_pink
                            start_active = False
                            create_file = False

                    if finish_text == '':
                        finish_text = finish_default
                        finish_color = rgb_bright_pink
                        finish_active = False
                        create_file = False
                    else:
                        try:
                            finish_date = datetime.datetime.strptime(finish_text, '%m/%d/%Y').date()
                        except ValueError:
                            finish_color = rgb_bright_pink
                            finish_active = False
                            create_file = False

                    if length_text == '':
                        length_text = length_default
                        length_color = rgb_bright_pink
                        length_active = False
                        create_file = False
                    else:
                        try:
                            ave_len = int(length_text)
                        except ValueError:
                            length_color = rgb_bright_pink
                            length_active = False
                            create_file = False

                    if distance_text == '':
                        distance_text = distance_default
                        distance_color = rgb_bright_pink
                        distance_active = False
                        create_file = False
                    else:
                        try:
                            ave_dis = int(distance_text)
                        except ValueError:
                            distance_color = rgb_bright_pink
                            distance_active = False
                            create_file = False

                    # create file if data was okay, otherwise display error message
                    if create_file:
                        # create the initial file
                        with open(working_file, 'w', newline='') as file:
                            writer = csv.writer(file)
                            field = ['Start', 'Finish', 'Length', 'Distance']
                            writer.writerow(field)

                        # add the initial info to the file
                        add_data_csv(start_date, finish_date)

                        # create the initial data frame
                        df = pd.read_csv(working_file)
                        last_date = df['Start'].iloc[-1]
                        if type(last_date) == str:
                            last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d').date()
                        ov_date = last_date + datetime.timedelta(days=ave_dis / 2)
                        period_date = last_date + datetime.timedelta(days=ave_dis)

                        # project the next couple of periods so we can build out the dates correctly
                        project_next(df)
                        project_next(df)

                        # set current state to the home screen and turn off data expansion to hide data window
                        data_expand = False
                        current_state = 'general'

                    else:
                        display_error = True

                # input boxes - if clicked, set to active and highlight the box
                # if a user has edited the default info, update the text color
                # if it is default info, clear it out for initial data entry
                if start_box.collidepoint(pygame.mouse.get_pos()):
                    start_active = True
                    start_color = rgb_turquoise
                    start_text_color = rgb_turquoise
                    if start_text == start_default:
                        start_text = ''
                else:
                    if start_text == start_default:
                        start_text_color = rgb_mid_gray
                    elif start_text == '':
                        start_text_color = rgb_mid_gray
                        start_text = start_default
                        start_color = rgb_dark
                    elif start_active == True:
                        start_text_color = rgb_dark
                        start_color = rgb_dark
                    start_active = False

                if finish_box.collidepoint(pygame.mouse.get_pos()):
                    finish_active = True
                    finish_color = rgb_turquoise
                    finish_text_color = rgb_turquoise
                    if finish_text == finish_default:
                        finish_text = ''
                else:
                    if finish_text == finish_default:
                        finish_text_color = rgb_mid_gray
                    elif finish_text == '':
                        finish_text_color = rgb_mid_gray
                        finish_text = finish_default
                        finish_color = rgb_dark
                    elif finish_active == True:
                        finish_text_color = rgb_dark
                        finish_color = rgb_dark
                    finish_active = False

                # length and distance look a little different because the default value is a valid entry
                if length_box.collidepoint(pygame.mouse.get_pos()):
                    length_active = True
                    if length_text_color == rgb_mid_gray:
                        length_text = ''
                    length_color = rgb_turquoise
                    length_text_color = rgb_turquoise
                else:
                    if length_text == '':
                        length_text_color = rgb_mid_gray
                        length_text = length_default
                        length_color = rgb_dark
                    elif length_active == True:
                        length_text_color = rgb_dark
                        length_color = rgb_dark
                    length_active = False

                if distance_box.collidepoint(pygame.mouse.get_pos()):
                    distance_active = True
                    if distance_text_color == rgb_mid_gray:
                        distance_text = ''
                    distance_color = rgb_turquoise
                    distance_text_color = rgb_turquoise
                else:
                    if distance_text == '':
                        distance_text_color = rgb_mid_gray
                        distance_text = distance_default
                        distance_color = rgb_dark
                    elif distance_active == True:
                        distance_text_color = rgb_dark
                        distance_color = rgb_dark
                    distance_active = False

        # check for typing
        if event.type == pygame.KEYDOWN:
            if current_state == 'new' or pop_up == 'add':
                # for whichever input box is active, edit the text
                if start_active:
                    if event.key == pygame.K_BACKSPACE:
                        start_text = start_text[:-1]
                    else:
                        start_text += event.unicode
    
                if finish_active:
                    if event.key == pygame.K_BACKSPACE:
                        finish_text = finish_text[:-1]
                    else:
                        finish_text += event.unicode
            
            if current_state == 'new':
                if length_active:
                    if event.key == pygame.K_BACKSPACE:
                        length_text = length_text[:-1]
                    else:
                        length_text += event.unicode
    
                if distance_active:
                    if event.key == pygame.K_BACKSPACE:
                        distance_text = distance_text[:-1]
                    else:
                        distance_text += event.unicode

        # when releasing the mouse button, reset buttons
        if event.type == pygame.MOUSEBUTTONUP:

            if current_state == 'general' and pop_up == 'none':
                # arrows will either be hovered or default depending on mouse location
                if left_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    left_arrow_image = left_arrow_hover
                else:
                    left_arrow_image = left_arrow_default

                if right_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    right_arrow_image = right_arrow_hover
                else:
                    right_arrow_image = right_arrow_default

                if data_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    if data_expand:
                        data_arrow_image = up_arrow_hover
                    else:
                        data_arrow_image = down_arrow_hover
                else:
                    if data_expand:
                        data_arrow_image = up_arrow_default
                    else:
                        data_arrow_image = down_arrow_default

                # help and add buttons
                if help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    help_button_image = help_button_hover
                else:
                    help_button_image = help_button_default

                if add_button_rect.collidepoint(pygame.mouse.get_pos()):
                    add_button_image = add_button_hover
                else:
                    add_button_image = add_button_default

            if pop_up == 'help':
                if x_button_rect.collidepoint(pygame.mouse.get_pos()):
                    x_button_image = x_button_hover
                else:
                    x_button_image = x_button_default

            if pop_up == 'add':
                if save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    save_button_image = save_button_hover
                else:
                    save_button_image = save_button_default

            if current_state == 'new':
                # submit button
                if submit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    submit_button_image = submit_button_hover
                else:
                    submit_button_image = submit_button_default

    # ===============================================================================
    # BUILDING THE SCREEN
    # ===============================================================================
    # background
    screen.fill(rgb_white)

    if current_state == 'general':
        # month message in top left corner
        month = use_date.strftime('%B')
        year = use_date.year
        month_message = title_font.render(str(year) + ' | ' + month, True, rgb_mid_gray)
        screen.blit(month_message, (20, 20))

        # help and add button in the top right
        screen.blit(help_button_image, help_button_rect)
        screen.blit(add_button_image, add_button_rect)

        # arrows and weekdays area
        screen.blit(left_arrow_image, left_arrow_rect)
        screen.blit(right_arrow_image, right_arrow_rect)
        screen.blit(week_days, (53, 70))
        pygame.draw.line(screen, rgb_turquoise, (35, 85), (360, 85))
        date_rects = pull_dates(use_date, 65, 100, 44, 30, df)

        # box when hovering over dates
        if len(date_rects) > 35:
            y_height = 243
        else:
            y_height = 213
        if 28 < mouse_rect.x < 330 and 70 < mouse_rect.y < y_height and pop_up == 'none':
            pygame.draw.rect(screen, rgb_turquoise, (hover_x, hover_y, 30, 25), 1, 5)

        # build the 'my data' area messages and expand/collapse arrow
        data_message = title_font.render('My Data', True, rgb_mid_gray)
        average_length_message = body_font.render('AVERAGE PERIOD LENGTH: ', True, rgb_mid_gray)
        average_distance_message = body_font.render('AVERAGE TIME BETWEEN: ', True, rgb_mid_gray)
        ovulation_message = body_font.render('ESTIMATED OVULATION: ', True, rgb_mid_gray)
        start_message = body_font.render('EXPECTED START DATE: ', True, rgb_mid_gray)
        ave_len_message = body_font.render(str(ave_len) + ' days', True, rgb_dark)
        ave_dis_message = body_font.render(str(ave_dis) + ' days', True, rgb_dark)
        ov_date_message = body_font.render(str(ov_date), True, rgb_blue)
        period_message = body_font.render(str(period_date), True, rgb_bright_pink)
        screen.blit(average_length_message, (50, 340))
        screen.blit(ave_len_message, (245, 340))
        screen.blit(average_distance_message, (57, 365))
        screen.blit(ave_dis_message, (245, 365))
        screen.blit(ovulation_message, (68, 390))
        screen.blit(ov_date_message, (245, 390))
        screen.blit(start_message, (66, 415))
        screen.blit(period_message, (245, 415))
        screen.blit(data_arrow_image, data_arrow_rect)
        screen.blit(data_message, (50, 300))

        # animations for expanding/collapsing
        block_box = pygame.Surface((300, 100))
        block_box.fill(rgb_white)
        if data_expand:
            if current_height < 165:
                current_height += grow_rate_rect
                if current_height > 165:
                    current_height = 165
            if current_width < 324:
                current_width += grow_rate_line
            else:
                current_width = 324
            if alpha > 0:
                alpha = alpha - grow_alpha
                if alpha < 0:
                    alpha = 0
        else:
            if current_height > 60:
                current_height = current_height - grow_rate_rect
                if current_height < 60:
                    current_height = 60
            if current_width > 0:
                current_width = current_width - grow_rate_line
            else:
                current_width = 0
            if alpha < 255:
                alpha = alpha + grow_alpha
                if alpha > 255:
                    alpha = 255

        # draw the data box outline, line, and block boxes for animations
        pygame.draw.rect(screen, rgb_turquoise, (35, 280, 325, current_height), 1, 30)
        block_box.set_alpha(alpha)
        block_box.fill(rgb_white)
        screen.blit(block_box, (50, 340))
        if not current_width == 0:
            pygame.draw.line(screen, rgb_turquoise, (197-current_width/2, 330), (196+current_width/2, 330))

        # pop up window for the help button to open the legend/key
        if pop_up == 'help':
            screen.blit(help_window, help_window_rect)
            screen.blit(x_button_image, x_button_rect)

        # pop up window for the add button to add new period data
        if pop_up == 'add':
            # load window and buttons
            screen.blit(add_window, add_window_rect)
            screen.blit(x_button_image, x_button_rect)
            screen.blit(save_button_image, save_button_rect)

            # set up input rects
            pygame.draw.rect(screen, start_color, start_box, 1, 5)
            pygame.draw.rect(screen, finish_color, finish_box, 1, 5)

            # messages
            start_message = body_font.render('START DATE:', True, rgb_dark)
            finish_message = body_font.render('FINISH DATE:', True, rgb_dark)
            error_message = body_font.render('CHECK FORMAT', True, rgb_bright_pink)
            screen.blit(start_message, (95, 140))
            screen.blit(finish_message, (102, 170))
            if display_error == True:
                screen.blit(error_message, (195, 193))

            # text inputs
            start_text_message = body_font.render(start_text, True, start_text_color)
            finish_text_message = body_font.render(finish_text, True, finish_text_color)
            screen.blit(start_text_message, (205, 140))
            screen.blit(finish_text_message, (205, 170))

        # intro fade-in animation on launch
        intro_box = pygame.Surface((400, 480))
        intro_box.fill(rgb_white)
        if intro_alpha > 0:
            intro_alpha = intro_alpha - intro_grow
            if intro_alpha < 0:
                intro_alpha = 0
        intro_box.set_alpha(intro_alpha)
        intro_box.fill(rgb_white)
        screen.blit(intro_box, (0, 0))

    if current_state == 'new':
        # create boxes to block text for fade in
        block_box = pygame.Surface((400, 79))
        block_box.fill(rgb_white)
        block_box_two = pygame.Surface((400, 80))
        block_box.fill(rgb_white)
        block_box_three = pygame.Surface((400, 350))
        block_box_three.fill(rgb_white)

        # create all messages for user
        new_message = title_font.render('Welcome!', True, rgb_turquoise)
        new_message_two = body_font.render('Please enter the information for', True, rgb_dark)
        new_message_three = body_font.render('your last period below.', True, rgb_dark)
        screen.blit(new_message, (145, 50))
        screen.blit(new_message_two, (82, 110))
        screen.blit(new_message_three, (117, 135))
        last_start_message = body_font.render('Start Date of Last Period:', True, rgb_dark)
        last_finish_message = body_font.render('Finish Date of Last Period:', True, rgb_dark)
        length_message = body_font.render('Average Period Length:', True, rgb_dark)
        between_message = body_font.render('Average Time Between Periods:', True, rgb_dark)
        screen.blit(last_start_message, (80, 180))
        screen.blit(last_finish_message, (73, 210))
        screen.blit(length_message, (90, 240))
        screen.blit(between_message, (30, 270))
        screen.blit(submit_button_image, submit_button_rect)

        # create input boxes
        pygame.draw.rect(screen, start_color, start_box, 1, 5)
        pygame.draw.rect(screen, finish_color, finish_box, 1, 5)
        pygame.draw.rect(screen, length_color, length_box, 1, 5)
        pygame.draw.rect(screen, distance_color, distance_box, 1, 5)
        start_text_message = body_font.render(start_text, True, start_text_color)
        finish_text_message = body_font.render(finish_text, True, finish_text_color)
        length_text_message = body_font.render(length_text, True, length_text_color)
        distance_text_message = body_font.render(distance_text, True, distance_text_color)
        screen.blit(start_text_message, (270, 180))
        screen.blit(finish_text_message, (270, 210))
        screen.blit(length_text_message, (270, 240))
        screen.blit(distance_text_message, (270, 270))

        # error message when applicable
        if display_error:
            error_message = body_font.render('Please check the highlighted fields.', True, rgb_bright_pink)
            error_message_two = body_font.render('Dates should be entered in mm/dd/yyyy format.', True, rgb_bright_pink)
            error_message_three = body_font.render('Length and time between should be whole numbers.', True, rgb_bright_pink)
            screen.blit(error_message, (80, 370))
            screen.blit(error_message_two, (35, 400))
            screen.blit(error_message_three, (15, 420))

        # animations
        if current_width < 324:
            current_width += grow_rate_line
        else:
            current_width = 324
        if alpha > 0:
            alpha = alpha - (grow_alpha/2)
            if alpha < 0:
                alpha = 0
        else:
            grow_alpha_two = 4
        if alpha_two > 0:
            alpha_two = alpha_two - (grow_alpha_two/2)
            if alpha_two < 0:
               alpha_two = 0
        else:
            grow_alpha_three = 4
        if alpha_three > 0:
            alpha_three = alpha_three - (grow_alpha_three/2)
            if alpha_three < 0:
                alpha_three = 0

        # draw boxes and lines for animations
        block_box.set_alpha(alpha)
        block_box.fill(rgb_white)
        screen.blit(block_box, (0, 0))
        block_box_two.set_alpha(alpha_two)
        block_box_two.fill(rgb_white)
        screen.blit(block_box_two, (0, 81))
        block_box_three.set_alpha(alpha_three)
        block_box.fill(rgb_white)
        screen.blit(block_box_three, (0, 160))
        if not current_width == 0:
            pygame.draw.line(screen, rgb_turquoise, (197 - current_width / 2, 80), (196 + current_width / 2, 80))

    if current_state == 'disclaimer':
        screen.blit(logo_image, logo_rect)

        blocker = pygame.Surface((400, 200))
        blocker.fill(rgb_white)
        blocker_two = pygame.Surface((400, 200))
        blocker_two.fill(rgb_white)
        if initial:
            body_message_one = body_font.render('In light of Roe v. Wade being overturned,', True, rgb_dark)
            body_message_two = body_font.render('I wanted to develop an app that I was sure', True, rgb_dark)
            body_message_three = body_font.render('would store my data locally on my device,', True, rgb_dark)
            body_message_four = body_font.render(f"where I was sure it wouldn't be accessed by", True, rgb_dark)
            body_message_five = body_font.render('or sold to third parties.  Security of your data', True, rgb_dark)
            body_message_six = body_font.render('is dependent on the security of your device.', True, rgb_dark)
            if a > 0:
                a = a - grow_a
                if a <= 0:
                    a = 0
                    initial = False
                    sleep(10)
                    a_two = 255
        else:
            body_message_one = body_font.render('Period and ovulation forecasts are estimates,', True, rgb_dark)
            body_message_two = body_font.render('and are not intended as medical advice.', True, rgb_dark)
            body_message_three = body_font.render('Estimates will get more accurate the more', True, rgb_dark)
            body_message_four = body_font.render('you use the app.  Please consult a doctor for', True, rgb_dark)
            body_message_five = body_font.render('any medical advice or questions!', True, rgb_dark)
            body_message_six = body_font.render(' ', True, rgb_dark)
            if a_two > 0:
                a_two = a_two - grow_a
                if a_two <= 0:
                    a_two = 0
                    sleep(5)
                    if os.path.isfile(working_file) == False:
                        # set state to 'new' for building the screen
                        current_state = 'new'

                        # set values for animations
                        grow_alpha_two = 0
                        alpha_two = 255
                        grow_alpha_three = 0
                        alpha_three = 255
                        display_error = False

                        # set initial border colors for entry fields
                        start_color = rgb_dark
                        finish_color = rgb_dark
                        length_color = rgb_dark
                        distance_color = rgb_dark

                        # set up input rects
                        start_box = pygame.Rect(265, 175, 100, 25)
                        finish_box = pygame.Rect(265, 205, 100, 25)
                        length_box = pygame.Rect(265, 235, 30, 25)
                        distance_box = pygame.Rect(265, 265, 30, 25)

                        # set up input text
                        length_text_color = rgb_mid_gray
                        distance_text_color = rgb_mid_gray
                        length_default = '7'
                        distance_default = '28'
                        length_text = length_default
                        distance_text = distance_default
                        distance_active = False
                        length_active = False
                    else:
                        # set state for building the screen to default
                        current_state = 'general'

                        # pull initial data frame
                        df = pd.read_csv(working_file)
                        ave_len = round(df['Length'].mean(), 1)
                        ave_dis = round(df['Distance'].mean(), 1)
                        last_date = df['Start'].iloc[-1]
                        if type(last_date) == str:
                            last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d').date()
                        ov_date = last_date + datetime.timedelta(days=int(ave_dis / 2))
                        period_date = last_date + datetime.timedelta(days=int(ave_dis))
                        project_next(df)
                        project_next(df)

        screen.blit(title_message, (130, 210))
        y = 240
        d = 20
        s = 15
        screen.blit(body_message_one, (40, y))
        screen.blit(body_message_two, (40, y + d))
        screen.blit(body_message_three, (40, y + (2*d)))
        screen.blit(body_message_four, (40, y + (3*d)))
        screen.blit(body_message_five, (40, y + (4*d)))
        screen.blit(body_message_six, (40, y + (5*d)))
        pygame.draw.line(screen, rgb_bright_pink, (30, 232), (370, 232), 2)
        blocker.set_alpha(a)
        blocker.fill(rgb_white)
        screen.blit(blocker, (0, 209))
        blocker_two.set_alpha(a_two)
        blocker_two.fill(rgb_white)
        screen.blit(blocker_two, (0, y))

    # mouse and last touches
    screen.blit(mouse, mouse_rect)

    # update surface display
    pygame.display.update()
    fps_clock.tick(60)
