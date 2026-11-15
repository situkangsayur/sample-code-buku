"""Bab 39: log append-only berpartisi ala Kafka dan queue klasik sebagai pembanding.

Partisi dipilih dengan FNV-1a 64 bit (Kafka sendiri memakai murmur2 untuk key).
Jalankan: python3 kafka_log.py
"""

FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
MASK64 = (1 << 64) - 1


def fnv1a64(data: bytes) -> int:
    """Hash FNV-1a 64 bit: sederhana, deterministik, sama di Python dan Rust."""
    h = FNV_OFFSET
    for b in data:
        h ^= b
        h = (h * FNV_PRIME) & MASK64
    return h


class Partition:
    """Satu partisi: list yang hanya boleh ditambah di ujung (append-only)."""

    def __init__(self):
        self.records = []

    def append(self, key, value):
        self.records.append((key, value))
        return len(self.records) - 1  # offset = indeks record

    def read(self, offset, max_records):
        # membaca tidak menghapus apa pun
        return self.records[offset:offset + max_records]


class Topic:
    def __init__(self, name, num_partitions):
        self.name = name
        self.partitions = [Partition() for _ in range(num_partitions)]

    def partition_for(self, key):
        return fnv1a64(key.encode()) % len(self.partitions)

    def produce(self, key, value):
        p = self.partition_for(key)
        offset = self.partitions[p].append(key, value)
        return p, offset


def range_assign(num_partitions, members):
    """Bagi partisi ke anggota group secara berurutan (mirip RangeAssignor)."""
    members = sorted(members)
    result = {m: [] for m in members}
    per, extra = divmod(num_partitions, len(members))
    p = 0
    for i, m in enumerate(members):
        count = per + (1 if i < extra else 0)
        result[m] = list(range(p, p + count))
        p += count
    return result


class ConsumerGroup:
    """Satu consumer group menyimpan committed offset per partisi."""

    def __init__(self, topic, members):
        self.topic = topic
        self.committed = [0] * len(topic.partitions)
        self.assignment = range_assign(len(topic.partitions), members)

    def rebalance(self, members):
        self.assignment = range_assign(len(self.topic.partitions), members)

    def poll(self, member, max_records=10):
        out = []
        for p in self.assignment[member]:
            start = self.committed[p]
            batch = self.topic.partitions[p].read(start, max_records)
            for i, (k, v) in enumerate(batch):
                out.append((p, start + i, k, v))
            self.committed[p] = start + len(batch)  # commit setelah diproses
        return out

    def lag(self):
        return sum(len(part.records) - c
                   for part, c in zip(self.topic.partitions, self.committed))


class ClassicQueue:
    """Queue klasik: dequeue menghapus message (bandingkan Bab 17)."""

    def __init__(self):
        self.items = []
        self.head = 0

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        if self.head == len(self.items):
            return None
        x = self.items[self.head]
        self.head += 1
        return x


def demo():
    t = Topic("pembayaran", 3)
    events = [("mhs-01", "bayar SPP"), ("mhs-02", "bayar SPP"),
              ("mhs-01", "bayar praktikum"), ("mhs-03", "bayar SPP"),
              ("mhs-02", "refund"), ("mhs-01", "bayar wisuda")]
    placed = [t.produce(k, v) for k, v in events]
    return t, placed


if __name__ == "__main__":
    assert fnv1a64(b"") == 0xCBF29CE484222325
    assert fnv1a64(b"a") == 0xAF63DC4C8601EC8C  # vektor uji resmi FNV-1a 64

    t, placed = demo()
    for (k, v), (p, off) in zip([("mhs-01", "bayar SPP"), ("mhs-02", "bayar SPP"),
                                  ("mhs-01", "bayar praktikum"), ("mhs-03", "bayar SPP"),
                                  ("mhs-02", "refund"), ("mhs-01", "bayar wisuda")], placed):
        print(f"{k:7s} {v:16s} -> partisi {p}, offset {off}")

    # semua event satu key berada di satu partisi, urut sesuai offset
    p01 = t.partition_for("mhs-01")
    assert [v for k, v in t.partitions[p01].records if k == "mhs-01"] == \
        ["bayar SPP", "bayar praktikum", "bayar wisuda"]

    # dua consumer group membaca data yang sama secara mandiri
    billing = ConsumerGroup(t, ["c1", "c2"])
    audit = ConsumerGroup(t, ["a1"])
    got_billing = billing.poll("c1") + billing.poll("c2")
    got_audit = audit.poll("a1")
    assert len(got_billing) == 6 and len(got_audit) == 6
    assert billing.lag() == 0 and audit.lag() == 0

    # replay: group baru mulai dari offset 0 dan tetap mendapat semuanya
    replay = ConsumerGroup(t, ["r1"])
    assert len(replay.poll("r1")) == 6

    # rebalance: anggota bertambah, partisi dibagi ulang
    assert range_assign(3, ["c1", "c2"]) == {"c1": [0, 1], "c2": [2]}
    assert range_assign(3, ["c1", "c2", "c3", "c4"]) == {"c1": [0], "c2": [1], "c3": [2], "c4": []}

    # queue klasik: setelah diambil satu consumer, message hilang bagi yang lain
    q = ClassicQueue()
    for _, v in [("mhs-01", "bayar SPP"), ("mhs-02", "bayar SPP")]:
        q.enqueue(v)
    assert q.dequeue() == "bayar SPP" and q.dequeue() == "bayar SPP" and q.dequeue() is None
    print("semua uji kafka_log lolos")
