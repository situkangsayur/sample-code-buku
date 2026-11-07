"""Error budget dan jejak energi (contoh hitungan Bab 14)."""
import math

pemuatan = 30 * 24
slo = 0.99
budget = math.floor(pemuatan * (1 - slo) + 1e-9)
print(f"{pemuatan} pemuatan, SLO {slo:.0%} -> boleh terlambat {budget} kali")

kwh_ti = 10 * 0.3 * 2              # mesin x kW x jam
kwh = kwh_ti * 1.5                 # PUE
print(f"energi harian {kwh:.1f} kWh, tahunan {kwh * 365:,.0f} kWh")
faktor = 0.8                       # ILUSTRASI; pakai faktor emisi resmi terbaru
print(f"emisi ilustrasi {kwh * 365 * faktor / 1000:.1f} t CO2e/tahun")
