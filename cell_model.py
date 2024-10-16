
class Cell():

    def __init__(self, cell_data):

        # Empirical values        
        self.R0 = cell_data["R0"]
        self.C1 = cell_data["C1"]
        self.R1 = cell_data["R1"]
        self.Q_capacity = cell_data["Q_capacity"]
        self.charge_curve = cell_data["charge_curve"]

        # State variables
        self.I = 0
        self.T = 0

        # Configured values        
        self.V = 2.5   # [V]
        self.Q = 0.01 # [C]
        self.soc = 0 # [%]
        self.soc_confidence = False

    def __voltage_lookup__(self):
        Q_trunc = round(self.Q, 2)
        Q_index = self.charge_curve["energy"].index(Q_trunc)
        return self.charge_curve["voltage"][Q_index]

    def determine_soc(self):

        if self.V == 2.5:
            self.soc = 0
            self.soc_confidence = True
        elif self.V == 3.65:
            self.soc = 100
            self.soc_confidence = True

    def charge_cell(self, I, t):
        """
        Simulates chargin behaviour of the cell.
            I [A]: charging current
            t [s]: amount of time at current I
        """

        charge_energy = I * t / 3600 # [A*h]
        self.Q = self.Q + charge_energy
        self.V = self.__voltage_lookup__()

        print(f"CELL | V: {self.V:.2f} V | Q: {self.Q:.3f} A*h")

