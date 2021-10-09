#!/usr/bin/env python
#_*_ coding: utf-8 _*_

def durationTime(duration):

    unit = ""

    if duration < 60:

        if duration == 1: unit = "1 segundo."

        else: unit = str(duration) + " segundos."

    elif duration >= 60 and duration < 3600:

        if duration / 60 == 1: unit = "1 minuto."

        else:

            seconds = duration % 60

            if duration // 60 != 1:

                if seconds == 1: unit = str(duration // 60) + " minutos y 1 segundo."

                else: unit = str(duration // 60) + " minutos y " + str(seconds) + " segundos."

            else:

                if seconds == 1: unit = "1 minuto y 1 segundo."

                else: unit = "1 minuto y " + str(seconds) + " segundos."

    elif duration >= 3600:

        if duration / 3600 == 1: unit = "1 hora."

        else:

            minutes = (duration % 3600) // 60

            seconds = minutes % 60

            if duration // 3600 != 1:

                if seconds == 1 and minutes == 1: unit = str(duration // 3600) + " horas con 1 minuto y 1 segundo."

                elif seconds == 1 and minutes > 1: unit = str(duration // 3600) + " hora con " + str(minutes) + " minutos y 1 segundo."

                elif seconds > 1 and minutes == 1: unit = str(duration // 3600) + " hora con 1 minuto y " + str(seconds) + " segundos."

                else: unit = str(duration // 3600) + " horas con " + str(minutes) + " minutos y " + str(seconds) + " segundos."

            else:

                if seconds == 1 and minutes == 1: unit = "1 hora con 1 minuto y 1 segundos."

                elif seconds == 1 and minutes > 1: unit = "1 hora con " + str(minutes) + " minutos y 1 segundo."

                elif seconds > 1 and minutes == 1: unit = "1 hora con 1 minuto con " + str(seconds) + " segundos."

                else: unit = "1 hora con " + str(minutes) + " minutos y " + str(seconds) + " segundos."

    return unit