from pythermalcomfort.models import pmv_ppd_iso

# Stałe
COMFORT_AIR_SPEED = 0.1  # Prędkość powietrza [m/s]
COMFORT_MET = 1.4  # Metabolizm [met]
COMFORT_CLO = 0.5  # Izolacyjność odzieży [clo]

def pmv_ppd_calc(temperature, humidity):
    result = pmv_ppd_iso(tdb=temperature, tr=temperature,
                         vr=COMFORT_AIR_SPEED,
                         rh=humidity,
                         met=COMFORT_MET,
                         clo=COMFORT_CLO,
                         model='7730-2005')

    print(f"PMV: {result.pmv:.2f}  |  PPD: {result.ppd:.2f} %")
    return result.pmv, result.ppd