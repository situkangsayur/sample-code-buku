"""Melihat isi buffer Arrow: validity bitmap, values, dan offsets (Kode 5.x)."""
import pyarrow as pa

nominal = pa.array([120, None, 75, 300], type=pa.int64())
validity, values = nominal.buffers()
print("null_count :", nominal.null_count)
print("validity   :", format(validity.to_pybytes()[0], "08b"), "(bit 0 di kanan)")
print("values     :", values.size, "byte untuk", len(nominal), "nilai int64")

kanal = pa.array(["QRIS", "ATM", "MOBILE"])
_, offsets, data = kanal.buffers()
print("offsets    :", [int.from_bytes(offsets.to_pybytes()[i:i + 4], "little")
                       for i in range(0, 16, 4)])
print("data       :", data.to_pybytes())

# RecordBatch = beberapa array sepanjang sama + schema
batch = pa.record_batch([nominal, pa.array(["QRIS", "ATM", None, "QRIS"])],
                        names=["nominal", "kanal"])
print(batch.schema)
