"""Module for managing import/export of models."""
from cobra.io.json import load_json_model as load_json_cobra_model
from cobra.io.json import save_json_model as save_json_cobra_model


# from mass.io.json import load_json_model as load_json_mass_model
# from mass.io.json import save_json_model as save_json_mass_model


def save_model_filetype(model, filename, module, **kwargs):
    """TODO DOCSTRING."""
    filetype = filename.suffix.split(".")[-1]
    try:
        save_function = {
            # ("json", "mass"): save_json_mass_model,
            ("json", "cobra"): save_json_cobra_model,
        }[(filetype, module)]
    except KeyError as e:
        raise ValueError("Unrecognized model and file types `{}`".format(str(e)))
    if kwargs.pop("verbose"):
        print("Saving model at {}".format(filename))
    save_function(model, str(filename), **kwargs)


def load_model_filetype(filename, module, **kwargs):
    """TODO DOCSTRING."""
    filetype = filename.suffix.split(".")[-1]
    try:
        load_function = {
            # ("json", "mass"): load_json_mass_model,
            ("json", "cobra"): load_json_cobra_model,
        }[(filetype, module)]
    except KeyError as e:
        raise ValueError("Unrecognized model and file types `{}`".format(str(e)))
    if kwargs.get("verbose"):
        print("Loading model at {}".format(filename))
    return load_function(filename=str(filename))
