from glbooker import GLBooker

if __name__ == '__main__':
    booker = GLBooker(
        username='',
        password='',
        days_later=7,
        workout_start='6:00PM',
        workout_end='7:00PM')
    booker.book()
