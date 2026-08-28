from tier1_meep_optics.sb2s3_switch_cell import Sb2S3SwitchCellFDTD

s = Sb2S3SwitchCellFDTD()
r_cr = s.solve_state("crystalline")
print("CR IL:", r_cr["insertion_loss_dB"])
print("CR XT:", r_cr["crosstalk_dB"])
print("CR Passivity:", r_cr["passivity"])
r_am = s.solve_state("amorphous")
print("AM IL:", r_am["insertion_loss_dB"])
print("AM XT:", r_am["crosstalk_dB"])
print("AM Passivity:", r_am["passivity"])
