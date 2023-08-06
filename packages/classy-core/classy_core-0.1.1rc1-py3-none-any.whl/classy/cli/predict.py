from omegaconf import OmegaConf

from classy.cli.subcmd import CommandWithSubcommands


class PredictCommand(CommandWithSubcommands):
    pass


def load_model_and_dataset_conf_for_prediction(
    model_checkpoint_path: str,
    prediction_params: str,
    cuda_device: int,
):
    import torch
    from classy.utils.lightning import load_classy_module_from_checkpoint, load_prediction_dataset_conf_from_checkpoint

    model = load_classy_module_from_checkpoint(model_checkpoint_path)
    model.to(torch.device(cuda_device if cuda_device != -1 else "cpu"))
    model.freeze()

    if prediction_params is not None:
        model.load_prediction_params(dict(OmegaConf.load(prediction_params)))

    dataset_conf = load_prediction_dataset_conf_from_checkpoint(model_checkpoint_path)

    # mock call to load resources
    next(model.predict(samples=[], dataset_conf=dataset_conf), None)

    return model, dataset_conf


def interactive_main(
    model_checkpoint_path: str,
    prediction_params: str,
    cuda_device: int,
):

    model, dataset_conf = load_model_and_dataset_conf_for_prediction(
        model_checkpoint_path, prediction_params, cuda_device
    )

    while True:
        _, prediction = next(
            model.predict(
                [model.read_input_from_bash()],
                dataset_conf=dataset_conf,
            )
        )
        print(f"\t# prediction: \t{prediction}")


def file_main(
    model_checkpoint_path: str,
    input_path: str,
    output_path: str,
    prediction_params: str,
    cuda_device: int,
    token_batch_size: int,
):
    from classy.data.data_drivers import get_data_driver

    model, dataset_conf = load_model_and_dataset_conf_for_prediction(
        model_checkpoint_path, prediction_params, cuda_device
    )

    input_extension, output_extension = input_path.split(".")[-1], output_path.split(".")[-1]
    assert input_extension == output_extension, (
        f"Having different input and output extensions is not currently a supported use case: "
        f"input {input_extension} != output {output_extension}"
    )
    data_driver = get_data_driver(model.task, input_extension)

    def it():
        for source, prediction in model.predict(
            data_driver.read_from_path(input_path),
            token_batch_size=token_batch_size,
            dataset_conf=dataset_conf,
            progress_bar=True,
        ):
            source.update_classification(prediction)
            yield source

    data_driver.save(it(), output_path)
