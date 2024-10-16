import cell_model, charger_model
import json
import time

with open("./cell_lab_data.json") as file:
    data = json.load(file)
cell_name = "LiFePO4_generic"
data = data[cell_name]

cell = cell_model.Cell(data)
charger = charger_model.Charger()

charger.V_Set = 3.5
charger.I_Set = 5
charger.start_charger()

while charger.power_on:
    charger.update_output(cell.V, cell.R0)
    cell.charge_cell(charger.I, 1)
    time.sleep(1)



