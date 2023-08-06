from pathlib import Path
from typing import Tuple, List, Optional

import haiku

from alphafold.model import model, config, data


def load_models_and_params(
    num_models: int,
    num_recycle: bool = 3,
    model_order: Optional[List[int]] = None,
    model_suffix: str = "_ptm",
    data_dir: Path = Path("."),
    recompile_all_models: bool = False,
) -> List[Tuple[str, model.RunModel, haiku.Params]]:
    """We use only two actual models and swap the parameters to avoid recompiling.

    Note that models 1 and 2 have a different number of parameters compared to models 3, 4 and 5,
    so we load model 1 and model 3.
    """
    if not model_order:
        model_order = [3, 4, 5, 1, 2]

    # Use only two model and later swap params to avoid recompiling
    model_runner_and_params: [Tuple[str, model.RunModel, haiku.Params]] = []
    model_runner_1 = None
    model_runner_3 = None
    if recompile_all_models:
        for n, model_number in enumerate(model_order):
            model_name = f"model_{model_number}"
            params = data.get_model_haiku_params(
                model_name=model_name + model_suffix, data_dir=str(data_dir)
            )
            model_config = config.model_config(model_name + model_suffix)
            if model_suffix == "_ptm":
                model_config.data.eval.num_ensemble = 1
                model_config.data.common.num_recycle = num_recycle
                model_config.model.num_recycle = num_recycle
            elif model_suffix == "_multimer":
                model_config.model.num_recycle = num_recycle
                model_config.model.num_ensemble_eval = 1
            model_runner_and_params.append(
                (model_name, model.RunModel(model_config, params), params)
            )
        return model_runner_and_params
    else:
        for n, model_number in enumerate(model_order):
            if n == num_models:
                break
            if model_number in [1, 2]:
                if not model_runner_1:
                    model_config = config.model_config("model_1" + model_suffix)
                    if model_suffix == "_ptm":
                        model_config.data.eval.num_ensemble = 1
                        model_config.data.common.num_recycle = num_recycle
                        model_config.model.num_recycle = num_recycle
                    elif model_suffix == "_multimer":
                        model_config.model.num_ensemble_eval = 1
                        model_config.model.num_recycle = num_recycle

                    model_runner_1 = model.RunModel(
                        model_config,
                        data.get_model_haiku_params(
                            model_name="model_1" + model_suffix, data_dir=str(data_dir)
                        ),
                    )
                model_runner = model_runner_1
            else:
                assert model_number in [3, 4, 5], model_number

                if not model_runner_3:
                    model_config = config.model_config("model_3" + model_suffix)
                    if model_suffix == "_ptm":
                        model_config.data.eval.num_ensemble = 1
                        model_config.data.common.num_recycle = num_recycle
                        model_config.model.num_recycle = num_recycle
                    elif model_suffix == "_multimer":
                        model_config.model.num_ensemble_eval = 1
                        model_config.model.num_recycle = num_recycle
                    model_runner_3 = model.RunModel(
                        model_config,
                        data.get_model_haiku_params(
                            model_name="model_3" + model_suffix, data_dir=str(data_dir)
                        ),
                    )
                model_runner = model_runner_3

            model_name = f"model_{model_number}"
            params = data.get_model_haiku_params(
                model_name=model_name + model_suffix, data_dir=str(data_dir)
            )
            model_runner_and_params.append((model_name, model_runner, params))
        return model_runner_and_params
