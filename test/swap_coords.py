# -*- coding: utf-8 -*-
# Copyright (C) 2026 plaisant
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import configparser

CONFIG_FILE = "intel_config_v33.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Read current values
confirm_x = config.get('BINANCE_CONTROLS','bin_confirm_x')
confirm_y = config.get('BINANCE_CONTROLS','bin_confirm_y')
close_x = config.get('BINANCE_CONTROLS','bin_close_all_x')
close_y = config.get('BINANCE_CONTROLS','bin_close_all_y')

# Swap values
config.set('BINANCE_CONTROLS','bin_close_all_x',confirm_x)
config.set('BINANCE_CONTROLS','bin_close_all_y',confirm_y)
config.set('BINANCE_CONTROLS','bin_confirm_x',close_x)
config.set('BINANCE_CONTROLS','bin_confirm_y',close_y)

with open(CONFIG_FILE, 'w') as f:
    config.write(f)

print("Swapped coordinates successfully.")
