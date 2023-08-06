#      A python library for getting Load Shedding schedules.
#      Copyright (C) 2021  Werner Pieterson
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from unittest import TestCase

from load_shedding import get_schedule, get_suburb_schedule, get_schedule_by_suburb_id, list_to_dict, ScheduleError
from providers.mock_eskom import MockEskom
from providers.eskom import Province, Stage, Suburb


class Test(TestCase):
    schedule = [
        ['2021-11-11 06:00', '2021-11-11 08:30'], ['2021-11-12 06:00', '2021-11-12 08:30'],
        ['2021-11-12 14:00', '2021-11-12 16:30'], ['2021-11-13 12:00', '2021-11-13 14:30'],
        ['2021-11-13 20:00', '2021-11-13 22:30'], ['2021-11-14 20:00', '2021-11-14 22:30'],
        ['2021-11-15 04:00', '2021-11-15 06:30'], ['2021-11-16 04:00', '2021-11-16 06:30'],
        ['2021-11-16 12:00', '2021-11-16 14:30'], ['2021-11-17 10:00', '2021-11-17 12:30'],
        ['2021-11-17 18:00', '2021-11-17 20:30'], ['2021-11-18 18:00', '2021-11-18 20:30'],
        ['2021-11-19 02:00', '2021-11-19 04:30'], ['2021-11-20 02:00', '2021-11-20 04:30'],
        ['2021-11-20 10:00', '2021-11-20 12:30'], ['2021-11-21 08:00', '2021-11-21 10:30'],
        ['2021-11-21 16:00', '2021-11-21 18:30'], ['2021-11-22 16:00', '2021-11-22 18:30'],
        ['2021-11-23 00:00', '2021-11-23 02:30'], ['2021-11-24 00:00', '2021-11-24 02:30'],
        ['2021-11-24 08:00', '2021-11-24 10:30'], ['2021-11-25 06:00', '2021-11-25 08:30'],
        ['2021-11-25 14:00', '2021-11-25 16:30'], ['2021-11-26 14:00', '2021-11-26 16:30'],
        ['2021-11-26 22:00', '2021-11-26 00:30'], ['2021-11-27 22:00', '2021-11-27 00:30'],
        ['2021-11-28 06:00', '2021-11-28 08:30'], ['2021-11-29 04:00', '2021-11-29 06:30'],
        ['2021-11-29 12:00', '2021-11-29 14:30'], ['2021-11-30 12:00', '2021-11-30 14:30'],
        ['2021-11-30 20:00', '2021-11-30 22:30'], ['2021-12-01 18:00', '2021-12-01 20:30'],
        ['2021-12-02 02:00', '2021-12-02 04:30'], ['2021-12-03 02:00', '2021-12-03 04:30'],
        ['2021-12-03 10:00', '2021-12-03 12:30'], ['2021-12-04 10:00', '2021-12-04 12:30'],
        ['2021-12-04 18:00', '2021-12-04 20:30'], ['2021-12-05 16:00', '2021-12-05 18:30'],
        ['2021-12-06 00:00', '2021-12-06 02:30'], ['2021-12-07 00:00', '2021-12-07 02:30'],
        ['2021-12-07 08:00', '2021-12-07 10:30'], ['2021-12-08 08:00', '2021-12-08 10:30'],
        ['2021-12-08 16:00', '2021-12-08 18:30'], ['2021-12-09 14:00', '2021-12-09 16:30'],
        ['2021-12-09 22:00', '2021-12-09 00:30']
    ]

    def setUp(self) -> None:
        self.eskom = MockEskom()

    def test_get_area_schedule(self):
        want = {
            Stage.STAGE_1.value: Test.schedule,
            Stage.STAGE_2.value: Test.schedule,
            Stage.STAGE_3.value: Test.schedule,
            Stage.STAGE_4.value: Test.schedule
        }
        got = get_suburb_schedule(self.eskom, province=Province(id=Province.WESTERN_CAPE), suburb=Suburb(id=1058852),
                                  cached=True)
        self.assertEqual(dict, type(got))
        self.assertDictEqual(want, got)

    def test_get_schedule(self):
        self.assertRaises(ScheduleError, get_schedule, self.eskom, province=Province(id=Province.WESTERN_CAPE),
                          suburb=Suburb(id=1058852), stage=Stage.UNKNOWN, cached=True)

        want = Test.schedule
        got = get_schedule(self.eskom, province=Province(id=Province.WESTERN_CAPE), suburb=Suburb(id=1058852),
                           stage=Stage.STAGE_2, cached=True)
        self.assertListEqual(want, got)

    def test_get_schedule_by_suburb_id(self):
        self.assertRaises(ScheduleError, get_schedule_by_suburb_id, self.eskom, province=Province.WESTERN_CAPE, suburb_id=1058852, stage=Stage.UNKNOWN)

        want = Test.schedule
        got = get_schedule_by_suburb_id(self.eskom, province=Province.WESTERN_CAPE, suburb_id=1058852, stage=Stage.STAGE_2)
        self.assertListEqual(want, got)

    def test_list_to_dict(self):
        schedule = self.eskom.get_schedule(province=Province(id=Province.WESTERN_CAPE), suburb=Suburb(id=1058852),
                                           stage=Stage.STAGE_2)
        self.assertEqual(list, type(schedule))
        got = list_to_dict(schedule)
        self.assertEqual(dict, type(got))
