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
from utils.logger import AgentLogger
from agents.agent_3 import ExecutionAgent

class TacticianLink:
    def __init__(self, config_manager, browser_bot):
        self.cfg = config_manager
        self.log = AgentLogger("TACTICIAN")
        # Inicjalizujemy wbudowanego Agenta 3
        self.agent_3 = ExecutionAgent(config_manager, browser_bot)

    def dispatch_order(self, decision_json):
        """
        Otrzymuje decyzję (JSON) ze Strategist i przekazuje do wykonania Agentowi 3.
        """
        if not decision_json:
            return

        try:
            action = decision_json.get('action', 'HOLD')
            
            # Logowanie decyzji
            self.log.log(f"Otrzymano rozkaz: {action}")
            
            if action == "HOLD":
                self.log.log("Decyzja strategiczna: HOLD. Brak akcji.")
                return

            # --- FIREWALL: Walidacja podstawowa ---
            # Tutaj można dodać sprawdzanie limitów ryzyka (np. max quantity)
            
            # --- EGZEKUCJA ---
            self.log.log(f"Przekazuję do Agenta 3: {action}")
            self.agent_3.execute_order(decision_json)
            
        except Exception as e:
            self.log.log(f"Błąd dispatchera Tactician: {e}", "ERROR")