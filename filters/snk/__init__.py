# __init__.py
import butterworth as bt
import bessel as bl

'''
lowpass = bl.Lowpass()
highpass = bl.Highpass()

# Spécifier les résistances et calculer les condensateurs
c_vals = [1e-6,1e-9,1e-6,1e-9]
tf, stages = highpass.multiple_order_highpass(order=4, cutoff_freq=1000, c_vals=c_vals)

print("Fonction de transfert combinée :", tf)
for i, stage in enumerate(stages):
    print(f"Stage {i+1}:")
    print("Fonction de transfert :", stage['tf'])
    print("Paramètres :", stage['params'])
'''
lowpass = bt.Butterworth_LowPass()

# Spécifier les résistances et calculer les condensateurs
tf = lowpass.components(order=11,cutoff_frequency=10000000,c1=2.2e-6, c2=3e-3)
print("Fonction de transfert combinée :", tf)
