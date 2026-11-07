"""Penyetelan hyperparameter dengan Optuna (TPE + pruning median) memakai fungsi
dari latih_fashion.py. Kode 10.4 pada buku."""
import optuna
import torch
from torch import nn

from latih_fashion import buat_model, data, evaluasi, set_seed


def objektif(trial):
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)      # skala log
    p_drop = trial.suggest_float("dropout", 0.0, 0.5)
    lebar = trial.suggest_categorical("lebar", [256, 512, 1024])
    wd = trial.suggest_float("weight_decay", 1e-6, 1e-2, log=True)

    set_seed(0)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    dl_latih, dl_val, _ = data(256, seed=0, augmentasi=False)
    model = buat_model(lebar, p_drop).to(dev)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(8):
        model.train()
        for xb, yb in dl_latih:
            loss = loss_fn(model(xb.to(dev)), yb.to(dev))
            opt.zero_grad(); loss.backward(); opt.step()
        loss_val, akurasi = evaluasi(model, dl_val, loss_fn, dev)
        trial.report(akurasi, epoch)
        if trial.should_prune():                  # hentikan percobaan yang tertinggal
            raise optuna.TrialPruned()
    return akurasi


if __name__ == "__main__":
    studi = optuna.create_study(direction="maximize",
                                sampler=optuna.samplers.TPESampler(seed=0),
                                pruner=optuna.pruners.MedianPruner(n_warmup_steps=2))
    studi.optimize(objektif, n_trials=30)
    print("terbaik:", studi.best_params, "akurasi validasi:", round(studi.best_value, 4))
