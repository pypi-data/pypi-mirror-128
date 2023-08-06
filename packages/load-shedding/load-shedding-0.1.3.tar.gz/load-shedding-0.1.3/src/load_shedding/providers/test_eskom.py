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

from eskom import Eskom, AreaInfo, Province, Stage, Suburb, Municipality

skip_slow = os.environ.get('skip_slow', False)


@unittest.skipIf(skip_slow, "Slow (Network calls)")
class TestEskom(TestCase):

    def setUp(self) -> None:
        self.eskom = Eskom()

    def test_find_suburbs(self):
        suburbs = self.eskom.find_suburbs(search_text="Milnerton")
        self.assertEqual(type(suburbs), list)
        self.assertNotEqual(len(suburbs), 0)
        self.assertEqual(type(suburbs[0]), Suburb)
        self.assertEqual(suburbs[0].id, 1058852)

    def test_get_municipalities(self):
        municipalities = self.eskom.get_municipalities(province=Province(id=Province.WESTERN_CAPE))
        self.assertEqual(type(municipalities), list)
        self.assertNotEqual(len(municipalities), 0)
        self.assertEqual(type(municipalities[0]), Municipality)
        self.assertEqual(municipalities[0].name, "Beaufort West")

    def test_get_schedule(self):
        schedule = self.eskom.get_schedule(province=Province(id=Province.WESTERN_CAPE), suburb=Suburb(id=1058852),
                                           stage=Stage.STAGE_2)
        self.assertEqual(type(schedule), list)
        self.assertNotEqual(len(schedule), 0)
        self.assertNotEqual(len(schedule[0]), 0)

    def test_get_schedule_area_info(self):
        area_info = self.eskom.get_schedule_area_info(suburb_id=1058852)
        self.assertEqual(type(area_info), AreaInfo)
        self.assertEqual(Province.WESTERN_CAPE, area_info.province.id)
        self.assertEqual(area_info.suburb.name, "Milnerton")

    def test_get_stage(self):
        stage = self.eskom.get_stage()
        self.assertEqual(type(stage), Stage)
        self.assertEqual(type(stage), Stage)

    def test_search(self):
        suburbs = self.eskom.find_suburbs(search_text="Milnerton")
        schedule = self.eskom.get_schedule(province=suburbs[0].province, suburb=suburbs[0], stage=Stage.STAGE_2)
        self.assertEqual(type(schedule), list)
        self.assertNotEqual(len(schedule), 0)
        self.assertNotEqual(len(schedule[0]), 0)
