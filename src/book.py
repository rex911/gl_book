import os

from glbooker import GLBooker

if __name__ == '__main__':
    booker = GLBooker(
        username=os.environ['GOODLIFE_USERNAME'],
        password=os.environ['GOODLIFE_PASSWORD'],
        days_later=os.environ['DAYS_LATER'],
        workout_start=os.environ['WORKOUT_START'],
        workout_end=os.environ['WORKOUT_END'],
        driver=os.environ['WEBDRIVER'])
    booker.book()
