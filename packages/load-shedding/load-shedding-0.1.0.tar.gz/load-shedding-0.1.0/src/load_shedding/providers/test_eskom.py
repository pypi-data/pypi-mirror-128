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

import os
import unittest
from unittest import TestCase

from .eskom import Eskom, AreaInfo, Province, Stage, Suburb, Municipality

skip_slow = os.environ.get('skip_slow', False)


@unittest.skipIf(skip_slow, "Slow (Network calls)")
class TestEskom(TestCase):

    def setUp(self) -> None:
        self.eskom = Eskom()

    def test_find_suburbs(self):
        suburbs = self.eskom.find_suburbs(search_text="Milnerton")
        self.assertEqual(list, type(suburbs))
        self.assertNotEqual(len(suburbs), 0)
        self.assertEqual(Suburb, type(suburbs[0]))
        self.assertEqual(1058852, suburbs[0].id)

    def test_get_municipalities(self):
        municipalities = self.eskom.get_municipalities(province=Province(id=Province.WESTERN_CAPE))
        self.assertEqual(list, type(municipalities))
        self.assertNotEqual(len(municipalities), 0)
        self.assertEqual(Municipality, type(municipalities[0]))
        self.assertEqual("Beaufort West", municipalities[0].name)

    def test_get_schedule(self):
        schedule = self.eskom.get_schedule(province=Province(id=Province.WESTERN_CAPE), suburb=Suburb(id=1058852),
                                           stage=Stage.STAGE_2)
        self.assertEqual(list, type(schedule))
        self.assertNotEqual(len(schedule), 0)
        self.assertNotEqual(len(schedule[0]), 0)

    def test_get_schedule_area_info(self):
        area_info = self.eskom.get_schedule_area_info(suburb_id=1058852)
        self.assertEqual(AreaInfo, type(area_info))
        self.assertEqual(Province.WESTERN_CAPE, area_info.province.id)
        self.assertEqual("Milnerton", area_info.suburb.name)

    def test_get_stage(self):
        stage = self.eskom.get_stage()
        self.assertEqual(Stage, type(stage))
        self.assertEqual(Stage, type(stage))

    def test_search(self):
        suburbs = self.eskom.find_suburbs(search_text="Milnerton")
        schedule = self.eskom.get_schedule(province=suburbs[0].province, suburb=suburbs[0], stage=Stage.STAGE_2)
        self.assertEqual(list, type(schedule))
        self.assertNotEqual(len(schedule), 0)
        self.assertNotEqual(len(schedule[0]), 0)
