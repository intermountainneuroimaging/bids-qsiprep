"""Parser module to parse gear config.json."""
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

from utils.fly.set_performance_config import set_n_cpus


# This function mainly parses gear_context's config.json file and returns relevant inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[bool, dict, dict]:
    """Parse the config and other options from the context,
     both gear and app options

    Returns:
        debug: debug flag
        gear_options: options for the gear
        app_options: options to pass to the app
    """

    debug = gear_context.config.get("debug")

    """   Gear config   """

    gear_options = {
        "ignore-bids-errors": gear_context.config.get("gear-ignore-bids-errors"),
        "run-bids-validation": gear_context.config.get("gear-run-bids-validation"),
        "save-intermediate-output": gear_context.config.get(
            "gear-save-intermediate-output"
        ),
        "intermediate-files": gear_context.config.get("gear-intermediate-files"),
        "intermediate-folders": gear_context.config.get("gear-intermediate-folders"),
        "dry-run": gear_context.config.get("gear-dry-run"),
        "keep-output": gear_context.config.get("gear-keep-output"),
        "freesurfer-license": gear_context.config.get("gear-FREESURFER_LICENSE"),
        "freesurfer-license-path": gear_context.get_input_path("freesurfer_license"),
        "output-dir": gear_context.output_dir,
        "destination-id": gear_context.destination["id"],
        "work-dir": gear_context.work_dir,
        "client": gear_context.client,
    }

    """   App options   """
    """
     Notes on inputs:  These notes follow the input order as documented here:
     https://qsiprep.readthedocs.io/en/latest/usage.html#command-line-arguments

    * Positional arguments are covered by the template
    * version: SKIPPED, can be passed in as a gear argument
    * skip-bids-validation: SKIPPED combined with the template's "run_validation"
    * participant-label: SKIPPED handled by the template
    * acquisition_type: ADDED  but it may be handled by the template, not sure what it does
    * bids-database-dir:
    * bids-filter-file:
    * interactive-reports-only: ADDED as boolean
    * recon-only: SKIPPED for now because I think due to flywheel infrastructure, there's no
        way to pass in "preprocessed" data to this gear...I could be wrong. 
    * recon-spec: ADDED, maybe qsi has some recon pipeline stuff built in? (added as input)
    * recon-input: SKIPPED because gear
    * freesurfer-input: 
    * skip-odf-reports: 
    * nthreads: SKIPPED, handled by template
    * omp-nthreads: SKIPPED, handled by template
    * mem_mb: SKIPPED, handled by template
    * low-mem: SKIPPED, not necessary
    * use-plugin: SKIPPED, UNKNOWN, skipped
    * anat-only: ADDED
    * dwi-only: ADDED
    * infant: ADDED
    * boilerplate: ADDED
    * verbose: SKIPPED handled by template
    * ignore: SKIPPED handled by template
    * longitudinal: ADDED
    * b0-threshold: ADDED
    * dwi-denoise-window: ADDED
    * denoise-method: 
    * unringing-method: ADDED
    * dwi-no-biascorr: ADDED
    * no-b0-harmonization: ADDED
    * denoise-before-combining: SKIPPED, because deprecated
    * denoise-after-combining: ADDED
    * combine-all-dwis: ADDED because denoise-after requires it
    * separate-all-dwis: ADDED
    * distortion-group-merge: ADDED
    * write-local-bvecs: ADDED
    * output-space: ADDED...though it seems limited, it's not deprecated...maybe they have future plans?
    * template: ADDED, though also limited
    * output-resolution: ADDED
    * b0-to-t1w-transform: ADDED
    * intramodal-template-iters: ADDED
    * intramodal-template-transform: ADDED
    * b0-motion-corr-to: ADDED
    * hmc-transform: ADDED
    * hmc_model: ADDED
    * eddy-config: ADDED
    * shoreline_iters: ADDED
    * impute-slice-threshold: ADDED
    * skull-strip-template: ADDED
    * skull-strip-fixed-seed: ADDED as bool, not clear if it needs an input
    * skip-t1-based-spatial-normalization: ADDED
    * fs-license-file: SKIPPED, handled by template
    * do-reconall: ADDED
    * prefer_dedicated_fmaps: ADDED
    * fmap-bspline: ADDED
    * fmap-no-demean: ADDED
    * use-syn-sdc: ADDED
    * force-syn: ADDED
    * reports-only: ADDED for ease of access
    All other options from the "Other Options" section are left out, as these can be passed into the 
    "bids_app_args" section

    """

    app_options_keys = [
        "bids_app_args",
        "interactive-reports-only",
        "acquisition_type",
        "anat-only",
        "dwi-only",
        "infant",
        "boilerplate",
        "longitudinal",
        "b0-threshold",
        "dwi_denoise_window",
        "unringing-method",
        "dwi-no-biascorr",
        "no-b0-harmonization",
        "denoise-after-combining",
        "combine-all-dwis",
        "separate_all_dwis",
        "distortion-group-merge",
        "write-local-bvecs",
        "output-space",
        "template",
        "output-resolution",
        "b0-to-t1w-transform",
        "intramodal-template-iters",
        "intramodal-template-transform",
        "b0-motion-corr-to",
        "hmc-transform",
        "hmc_model",
        "shoreline_iters",
        "impute-slice-threshold",
        "skull-strip-template",
        "skull-strip-fixed-seed",
        "skip-t1-based-spatial-normalization",
        "do-reconall",
        "prefer_dedicated_fmaps",
        "fmap-bspline",
        "fmap-no-demean",
        "use-syn-sdc",
        "force-syn",
        "reports-only",
        "participant_label",
        "n_cpus",
        "mem_mb",
        "write-graph",
        "ignore",
    ]
    app_options = {key: gear_context.config.get(key) for key in app_options_keys}

    app_options["n_cpus"] = set_n_cpus(app_options["n_cpus"])
    # app_options["mem_mb"] = set_mem_gb(app_options["mem_gb"])

    rs_path = gear_context.get_input_path("recon-spec")
    if rs_path:
        app_options["recon-spec"] = rs_path

    eddy_path = gear_context.get_input_path("eddy-config")
    if eddy_path:
        app_options["eddy-config"] = eddy_path

    # TO-DO: Validate app_options here, before launching the whole code
    # Note: Is it possible to validate directly against the QSIprep parser?
    # (https://github.com/PennLINC/qsiprep/blob/0.15.1/qsiprep/cli/run.py#L76-L517)

    return debug, gear_options, app_options
