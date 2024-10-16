
class Charger():

    V_MIN, V_MAX = 0, 5
    I_MIN, I_MAX = 0, 20
    MODES = {"OFF" : "OFF", "CC" : "CC", "CV" : "CV"}


    def __init__(self):

        self.V_Set = 0
        self.I_Set = 0
        self.power_on = False
        self.mode = self.MODES["OFF"] 
        self.V = 0
        self.I = 0
        self.P = self.V * self.I

    def start_charger(self):
        self.I = self.I_Set
        self.V = self.V_Set
        self.power_on = True

    def determine_charger_mode(self, V_load, R_load):
        """
        Set the system in OFF< CC, or CV mode depending on the conditions. 
        """
        
        if (not self.power_on) or (not self.check_system_safe(V_load, R_load)):
            self.mode =  self.MODES["OFF"]        
        elif self.I < self.I_Set:
            self.mode = self.MODES["CV"]
        elif self.V < self.V_Set:
            self.mode = self.MODES["CC"]
        else:
            print("Your CC/CV math is messed up.")


    def check_system_safe(self, V_load, R_load):
        """
        Returns True if system might be safe, False if system definitely not safe
        """
        assert self.V_Set <= self.V_MAX, f"Cannot exceed V_MAX={self.V_MAX}"
        assert self.I_Set <= self.I_MAX, f"Cannot exceed I_MAX={self.I_MAX}"

        OV_safe_setpoint = self.V_Set >= self.V
        OC_safe_setpoint = self.I_Set >= self.I
        OV_safe = self.V_Set >= V_load
        OC_safe = (self.V - V_load) / R_load <= self.I_MAX

        if OV_safe_setpoint and OC_safe_setpoint and OV_safe and OC_safe:
            return True
        
        assert OV_safe_setpoint, f"SAFETY - setpoint voltage too high."
        assert OC_safe_setpoint, f"SAFETY - setpoint current too high."
        assert OV_safe, f"SAFETY - overvoltage protection."
        assert OC_safe, f"SAFETY - overcurrent protection."

        self.V = 0
        self.I = 0
        self.mode = self.MODES["OFF"]

        return False
    
    def update_output(self, V_load, R_load):

        self.power_on = self.check_system_safe(V_load, R_load)

        V_drop = self.V - V_load
        self.V = min(self.V_Set, self.I * R_load + V_load)
        self.I = min(self.I_Set, V_drop / R_load)

        self.determine_charger_mode(V_load, R_load)
        print(f"System state: {self.mode}")
        print(f"CHRG | V: {self.V:.2f} V | I: {self.I:.2f} A")
