"""FSDP (ZeRO-3 versi PyTorch) dengan mixed precision BF16 dan sharded checkpoint.

Butuh >= 2 GPU:  torchrun --nproc_per_node=2 fsdp_latih.py
"""
import functools
import os

import torch
import torch.distributed as dist
import torch.distributed.checkpoint as dcp
import torch.nn as nn
import torch.nn.functional as F
from torch.distributed.checkpoint.state_dict import get_state_dict
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP, MixedPrecision
from torch.distributed.fsdp.wrap import size_based_auto_wrap_policy


def blok(d: int) -> nn.Module:
    return nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))


def main() -> None:
    dist.init_process_group("nccl")
    lr = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(lr)
    d = 2048
    model = nn.Sequential(*[blok(d) for _ in range(8)], nn.Linear(d, 10)).cuda()
    model = FSDP(
        model,
        auto_wrap_policy=functools.partial(size_based_auto_wrap_policy, min_num_params=1_000_000),
        mixed_precision=MixedPrecision(param_dtype=torch.bfloat16,
                                       reduce_dtype=torch.bfloat16,
                                       buffer_dtype=torch.bfloat16),
        device_id=lr,
    )  # tiap rank kini hanya memegang 1/N bobot, gradien, dan optimizer state
    opt = torch.optim.AdamW(model.parameters(), lr=1e-4)
    for langkah in range(50):
        x = torch.randn(32, d, device="cuda")
        y = torch.randint(0, 10, (32,), device="cuda")
        loss = F.cross_entropy(model(x), y)     # all-gather bobot per unit sebelum dipakai
        opt.zero_grad()
        loss.backward()                         # reduce-scatter gradien
        opt.step()
    if dist.get_rank() == 0:
        print(f"loss {loss.item():.4f}; memori puncak rank 0: "
              f"{torch.cuda.max_memory_allocated() / 1e9:.2f} GB")
    # Sharded checkpoint: setiap rank menulis potongannya sendiri secara paralel
    model_sd, opt_sd = get_state_dict(model, opt)
    dcp.save({"model": model_sd, "opt": opt_sd}, checkpoint_id="ckpt_fsdp")
    dist.destroy_process_group()


if __name__ == "__main__":
    main()
