from value_calculator import DCF
current_CF,growth_rate,discount_rate,FCF_multiple=24.58,0.1,0.15,25.5
print(DCF.GetIntrinsicValue(current_CF,growth_rate,discount_rate,FCF_multiple))