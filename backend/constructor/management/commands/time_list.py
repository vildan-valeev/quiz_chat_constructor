from datetime import datetime, time, timedelta
from django.db import models
from django.core.management.base import BaseCommand, CommandError
from constructor.models import Event, Staff
from django.core import serializers


def get_free_dates(primary, inners):
    i = 0
    # TODO: Написать исключение при неправильном оформлении "свободных/занятых" событий в календаре
    for t in inners:
        while t[0] > primary[i][1]:
            i += 1
            if i >= len(primary):
                break
        if t[1] < primary[i][1] and t[0] > primary[i][0]:
            # t cuts l1[i] in 2 pieces
            primary = primary[:i] + [(primary[i][0], t[0]), (t[1], primary[i][1])] + primary[i + 1:]
        elif t[1] >= primary[i][1] and t[0] <= primary[i][0]:
            # t eliminates l1[i]
            primary.pop(i)
        elif t[1] >= primary[i][1]:
            # t cuts off the top end of l1[i]
            primary[i] = (primary[i][0], t[0])
        elif t[0] <= primary[i][0]:
            # t cuts off the bottom end of l1[i]
            primary[i] = (t[1], primary[i][1])
        else:
            exit()
    return primary


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def get_time(self, date, pk):
        q = Event.objects.filter(staff_id=pk, start__day=date.day)

        free = []
        busy = []
        if q:
            for i in q:
                if i.status == 'FR':
                    start = i.start
                    end = i.end
                    free.append((start, end))
                else:
                    start = i.start
                    end = i.end
                    busy.append((start, end))

            # s = serializers.serialize('json', snippet)
            # s = [time(9, 30), ]
            # print(s)
            print(f'{free=}')
            print(f'{busy=}')


            # primary = []
            # inners = buf
            #
            result = get_free_dates(free, busy)
            print(f'{result=}')

            # ---------- нарезаем по duration ----------------
            btns = []
            for k in result:
                # print(f'{k=}, {k[0]}, {type(k[0])}, {k[0].hour}')
                btn_start = k[0],
                btn_end = k[1],
                td = k[1] - k[0]
                # print(f'{td=}')
                if (td / timedelta(minutes=30)) <= 1:
                    btns.append({'h': f'{k[0].hour:02d}', 'm': f'{k[0].minute:02d}', })
                else:
                    temp_start = k[0]
                    print(f'{temp_start.hour=}')
                    while temp_start < k[1]:
                        btn = {
                            'h': f'{temp_start.hour:02d}',
                            'm': f'{temp_start.minute:02d}',
                        }
                        btns.append(btn)
                        temp_start += timedelta(minutes=30)
            print(btns)
            return 'ok'
        else:
            s = []
            print(s)
            return 'None'

    def handle(self, *args, **options):
        date = datetime(2021, 4, 28)
        pk = 11
        return self.get_time(date, pk)
