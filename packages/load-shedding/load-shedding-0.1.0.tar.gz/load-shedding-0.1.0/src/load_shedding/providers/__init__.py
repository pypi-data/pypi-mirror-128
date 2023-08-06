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

class Provider:
    pass


class ProviderError(Exception):
    pass


class Suburb:
    def __init__(self, /, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.municipality = kwargs.get("municipality")
        self.province = kwargs.get("province")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{name} ({id}), {municipality}, {province}>".format(
            id=self.id,
            name=self.name,
            municipality=self.municipality,
            province=self.province
        )


class Municipality:
    def __init__(self, /, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{name} ({id})>".format(
            id=self.id,
            name=self.name,
        )


class Province:
    def __init__(self, /, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{name} ({id})>".format(
            id=self.id,
            name=self.name,
        )
