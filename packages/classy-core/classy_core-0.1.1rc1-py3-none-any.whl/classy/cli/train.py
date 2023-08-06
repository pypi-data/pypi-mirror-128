import os
from pathlib import Path
from typing import Optional


from jsonargparse import ArgumentParser
from omegaconf import DictConfig, OmegaConf

from cli.subcmd import BaseCommand
from utils.log import get_project_logger


logger = get_project_logger(__name__)


class TrainCommand(BaseCommand):
    name = "train"

    def run(self, args):
        if args.resume_from is not None:
            _main_resume(args.resume_from)
            return

        if args.root is not None:
            config_name = args.root
        else:
            config_name = args.task

        # TODO: do we need to add a specific config dir parameter to classy train? in case the user wants to override it
        cmd = ["classy-train", "-cn", config_name]  # , "-cd", str(Path.cwd() / "conf")]

        # override all the fields modified by the profile
        if args.profile is not None:
            cmd.append(f"+profiles={args.profile}")

        # choose device
        device = get_device(args.device)
        if device >= 0:
            if args.fp16:
                cmd.append("device=cuda_amp")
            else:
                cmd.append(f"device=cuda")
            cmd.append(f"device.gpus=[{device}]")
        else:
            if args.fp16:
                logger.error("fp16 is only available when training on a GPU")
                return
            cmd.append(f"device=cpu")

        # create default experiment name if not provided
        exp_name = args.exp_name or f"{args.task}-{args.model_name}"
        cmd.append(f"exp_name={exp_name}")

        # add dataset path
        cmd.append(f"data.datamodule.dataset_path={args.dataset}")

        # turn off shuffling if requested
        if args.no_shuffle:
            cmd.append("data.datamodule.shuffle_dataset=False")

        # wandb logging
        if args.wandb is not None:
            cmd.append(f"logging.wandb.use_wandb=True")
            if args.wandb == "anonymous":
                cmd.append(f"logging.wandb.anonymous=allow")
            else:
                assert "@" in args.wandb, (
                    "If you specify a value for '--wandb' it must contain both the name of the "
                    "project and the name of the specific experiment in the following format: "
                    "'<project-name>@<experiment-name>'"
                )

                project, experiment = args.wandb.split("@")
                cmd.append(f"logging.wandb.project_name={project}")
                cmd.append(f"logging.wandb.experiment_name={experiment}")

        # change the underlying transformer model
        if args.transformer_model is not None:
            cmd.append(f"transformer_model={args.transformer_model}")

        # precomputed vocabulary from the user
        if args.vocabulary_dir is not None:
            cmd.append(f"+data.vocabulary_dir={args.vocabulary_dir}")

        # bid-dataset option
        if args.big_dataset:
            logger.info(
                "The user selected the --big-dataset option. "
                "Hence we will: 1) assume the training dataset is ALREADY SHUFFLED "
                "2) evaluate the model performance every 2 thousand steps"
                "3) If the dataset provided is a file path when splitting the whole dataset in train, validation and test"
                "we will partition with the following ratio: 0.90 / 0.05 / 0.05"
            )
            cmd.append("data.datamodule.shuffle_dataset=False")
            cmd.append("training.pl_trainer.val_check_interval=2000")  # TODO: 2K steps seems quite arbitrary
            cmd.append("data.datamodule.validation_split_size=0.05")
            cmd.append("data.datamodule.test_split_size=0.05")

        # append all user-provided configuration overrides
        cmd += args.config

        # we import streamlit so that the stderr handler is added to the root logger here and we can remove it
        # it was imported in task_ui.py and was double-logging stuff...
        # this is the best workaround at this time, but we should investigate and / or (re-)open an issue
        # https://github.com/streamlit/streamlit/issues/1248
        import streamlit
        import logging

        # at this point, streamlit's is the only handler added, so we can safely reset the handlers
        logging.getLogger().handlers = []

        import hydra
        import sys

        # we are basically mocking the normal python script invocation by setting the argv to those we want
        # unfortunately there is no better way to do this at this moment in time :(
        sys.argv = cmd
        hydra.main(config_path="../../configurations")(_main_mock)()

    def parser(self) -> Optional[ArgumentParser]:
        # TODO: help
        parser = ArgumentParser(description="classy train -- TODO")
        parser.add_argument("task", choices=("sequence", "token", "sentence-pair", "qa", "generation"), help="TODO")
        parser.add_argument("dataset", type=Path)
        parser.add_argument("--profile", type=str, default=None)
        parser.add_argument("--transformer-model", type=str, default=None)
        parser.add_argument("-n", "--exp-name", "--experiment-name", dest="exp_name", default=None)
        parser.add_argument("-d", "--device", default="gpu")  # TODO: add validator?
        parser.add_argument("--root", type=str, default=None)
        parser.add_argument("-c", "--config", nargs="+", default=[])
        parser.add_argument("--resume-from", type=str)
        parser.add_argument("--wandb", nargs="?", const="anonymous", type=str)
        parser.add_argument("--no-shuffle", action="store_true")
        parser.add_argument("--fp16", action="store_true")
        parser.add_argument("--vocabulary-dir", default=None)
        parser.add_argument("--big-dataset", action="store_true")
        return parser


def _main_mock(cfg):
    # import here to avoid importing torch before it's actually needed
    import hydra
    from classy.scripts.model.train import fix_paths, train

    fix_paths(
        cfg,
        check_fn=lambda path: os.path.exists(hydra.utils.to_absolute_path(path[: path.rindex("/")])),
        fix_fn=lambda path: hydra.utils.to_absolute_path(path),
    )
    train(cfg)


def _main_resume(model_dir: str):

    if not os.path.isdir(model_dir):
        logger.error(f"The previous run directory provided: '{model_dir}' does not exist.")
        exit(1)

    if not os.path.isfile(f"{model_dir}/checkpoints/last.ckpt"):
        logger.error(
            "The directory must contain the last checkpoint stored in the previous run (checkpoints/last.ckpt)."
        )
        exit(1)

    import hydra

    # import here to avoid importing torch before it's actually needed
    from classy.utils.lightning import load_training_conf_from_checkpoint
    from classy.utils.hydra import fix_paths
    from classy.scripts.model.train import train

    os.chdir(model_dir)

    last_ckpt_path = "checkpoints/last.ckpt"
    cfg = load_training_conf_from_checkpoint(last_ckpt_path, post_trainer_init=True)
    cfg.training.resume_from = last_ckpt_path

    fix_paths(
        cfg,
        check_fn=lambda path: os.path.exists(hydra.utils.to_absolute_path(path[: path.rindex("/")])),
        fix_fn=lambda path: hydra.utils.to_absolute_path(path),
    )
    train(cfg)


def train(conf: DictConfig) -> None:
    import pytorch_lightning as pl
    import hydra
    from data.data_modules import ClassyDataModule

    # reproducibility
    pl.seed_everything(conf.training.seed)

    # data module declaration
    pl_data_module: ClassyDataModule = hydra.utils.instantiate(
        conf.data.datamodule, external_vocabulary_path=getattr(conf.data, "vocabulary_dir", None), _recursive_=False
    )
    pl_data_module.prepare_data()

    # main module declaration
    pl_module_init = {"_recursive_": False}
    if pl_data_module.vocabulary is not None:
        pl_module_init["vocabulary"] = pl_data_module.vocabulary
    pl_module = hydra.utils.instantiate(conf.model, **pl_module_init)

    # callbacks declaration
    callbacks_store = []

    # lightning callbacks
    if conf.training.early_stopping_callback is not None:
        early_stopping = hydra.utils.instantiate(conf.training.early_stopping_callback)
        callbacks_store.append(early_stopping)

    if conf.training.model_checkpoint_callback is not None:
        model_checkpoint = hydra.utils.instantiate(
            conf.training.model_checkpoint_callback,
            filename="{epoch:02d}-{" + conf.training.callbacks_monitor + ":.2f}",
        )
        callbacks_store.append(model_checkpoint)

    # model callbacks
    for callback in conf.callbacks.callbacks:
        callbacks_store.append(hydra.utils.instantiate(callback, _recursive_=False))

    # logging
    logger = None

    # wandb
    if conf.logging.wandb.use_wandb:
        from pytorch_lightning.loggers import WandbLogger

        wandb_params = dict(
            project=conf.logging.wandb.project_name,
            name=conf.logging.wandb.experiment_name,
            resume="allow",
            id=conf.logging.wandb.run_id,
        )
        if conf.logging.wandb.anonymous is not None:
            wandb_params["anonymous"] = "allow"

        logger = WandbLogger(**wandb_params)

        if conf.logging.wandb.run_id is None:
            conf.logging.wandb.run_id = logger.experiment.id

        # learning rate monitor
        learning_rate_monitor = pl.callbacks.LearningRateMonitor(logging_interval="step")
        callbacks_store.append(learning_rate_monitor)

    # trainer
    if conf.training.resume_from is not None:
        trainer = pl.trainer.Trainer(
            resume_from_checkpoint=conf.training.resume_from,
            callbacks=callbacks_store,
            logger=logger,
            **conf.device,
        )
    else:
        trainer: pl.trainer.Trainer = hydra.utils.instantiate(
            conf.training.pl_trainer,
            callbacks=callbacks_store,
            logger=logger,
            **conf.device,
        )

    # save resources
    pl_module.save_resources_and_update_config(
        conf=conf,
        working_folder=hydra.utils.get_original_cwd(),
        experiment_folder=Path.cwd(),
        data_module=pl_data_module,
    )

    # save updated config (and bk old config)
    Path(".hydra/config.yaml").rename(".hydra/config.bk.yaml")
    with open(".hydra/config.yaml", "w") as f:
        f.write(OmegaConf.to_yaml(conf))

    # saving post trainer-init conf
    with open(".hydra/config_post_trainer_init.yaml", "w") as f:
        f.write(OmegaConf.to_yaml(conf))

    # module fit
    trainer.fit(pl_module, datamodule=pl_data_module)
