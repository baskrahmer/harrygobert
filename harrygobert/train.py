import torch
from lightning import Trainer
from lightning import seed_everything

from harrygobert.data import get_dataloaders
from harrygobert.export import quantize, export_model_and_tokenizer, test_model_inference
from harrygobert.model import OFFClassificationModel, get_tokenizer, get_tokenize_fn
from harrygobert.util import get_callbacks, get_wandb_logger, parse_args


def main(cfg):
    seed_everything(1997)

    if cfg.debug:
        cfg.num_steps = 200

    if torch.cuda.is_available():
        torch.cuda.set_device(0)

    if cfg.use_wandb:
        wandb_logger = get_wandb_logger(cfg)

    model = OFFClassificationModel(cfg)
    tokenizer = get_tokenizer(cfg)
    tokenize_fn = get_tokenize_fn(cfg, tokenizer)

    train, val = get_dataloaders(cfg, tokenize_fn)

    trainer = Trainer(
        accelerator="auto",
        max_steps=cfg.num_steps,
        val_check_interval=cfg.eval_steps,
        check_val_every_n_epoch=None,
        logger=wandb_logger if cfg.use_wandb else None,
        callbacks=get_callbacks(cfg),
        precision=cfg.precision,
    )

    trainer.fit(
        model=model,
        train_dataloaders=train,
        val_dataloaders=val,
    )

    if cfg.quantize:
        model = quantize(cfg, trainer, train, val)
    export_model_and_tokenizer(cfg, model, tokenizer)
    test_model_inference(cfg)


if __name__ == '__main__':
    args = parse_args()
    main(args)
