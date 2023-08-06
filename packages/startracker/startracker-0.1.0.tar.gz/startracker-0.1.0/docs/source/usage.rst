StarTracker usage
#################

Star tracker provides collection of tools derived from `ctapipe.core.Tool`.
The actual functionality is implemented through `ctapipe.core.Component` based classes
and containers, used for the data exchange and preservation are derived from `ctapipe.core.Container`.
The functionality of base class is preserved:
- Configuration is provided through JSON files
- Logging module and provenance is available


Star reconstruction
===================

Star reconstruction is performed with `image_producer` tool. The results are stored as HDF5 files,
one per each analyzed subrun. The files contain collection of variance images, reference events
and star tables with the expected and reconstructed positions of each star considered.

Running the tool::

     image_producer --config /path/to/image_producer_configuration.json --log-level |DEBUG|INFO|WARNING|ERROR|CRITICAL|

Let's consider one complete and valid example of the configuration file.
Below you will find the detailed breakdown and explanation for each configuration block.

.. code-block:: JSON

    {
        "ImageProducer" : {
            "SlurmParameters": {
              "partition": "short"
            },
            "workdir" : "/tmp/",
            "data_path" : "/fefs/aswg/data/real/R0/20210813/",
            "run_number" : 5737
        },
        "StarExtractor" : {
            "max_images_per_file" : 1,
            "skipping_interval" : 10000,
            "cleaning" : {
                "bound_thresh" : 15,
                "pic_thresh" : 30
            },
            "telescope_location" : {
                "longitude" : 342.108612,
                "lattitude" : 28.761389,
                "elevation" : 2147
            },
            "events_per_image" : 200,
            "event_type" : 32,
            "check_broken_pixels" : true,
            "check_star_detection" : true,
            "min_star_prominence" : 3,
            "max_star_magnitude" : 5.0,
            "min_distance_between_stars" : 0.7,
            "max_star_offset" : 2.0
        },
        "EventTimeCalculator": {
          "extract_reference": true,
          "dragon_reference_counter": null,
          "dragon_reference_time": null,
          "dragon_module_id": null
        },
        "LSTR0Corrections" : {
            "drs4_pedestal_path" : "/fefs/aswg/data/real/calibration/20210813/v0.7.3/drs4_pedestal.Run05717.0000.fits",
            "calibration_path" : "/fefs/aswg/data/real/calibration/20210813/v0.7.3/calibration.Run05718.0000.hdf5",
            "drs4_time_calibration_path" : "/fefs/aswg/data/real/calibration/20210813/v0.7.3/time_calibration.Run05718.0000.hdf5" 
        },
        "PointingSource" : {
            "drive_report_path" : "/fefs/aswg/data/real/monitoring/DrivePositioning/drive_log_21_08_13.txt"
        },
        "LocalPeakWindowSum":{
            "window_shift": 4,
            "window_width": 8,
            "apply_integration_correction": false
        }
    }


ImageProducer tool configuration
--------------------------------

.. code-block:: JSON

    "ImageProducer" : {
        "SlurmParameters": {
          "partition": "short"
        },
        "workdir" : "/tmp/",
        "data_path" : "/fefs/aswg/data/real/R0/20210813/",
        "run_number" : 5737
    }

- `SlurmParameters` block contains regular slurm job parameters and used through the `simple-slurm` python module to submit the jobs to the SLURM-driven cluster
- `workdir` is simply a working directory, where all the results of the code will be stored
- `data_path` is a path to a folder with telescope data at R0 level


StarExtractor component configuration
-------------------------------------

.. code-block:: JSON

    "StarExtractor" : {
        "max_images_per_file" : 1,
        "skipping_interval" : 10000,
        "cleaning" : {
            "bound_thresh" : 15,
            "pic_thresh" : 30
        },
        "telescope_location" : {
            "longitude" : 342.108612,
            "lattitude" : 28.761389,
            "elevation" : 2147
        },
        "events_per_image" : 200,
        "event_type" : 32,
        "check_broken_pixels" : true,
        "check_star_detection" : true,
        "min_star_prominence" : 3,
        "max_star_magnitude" : 5.0,
        "min_distance_between_stars" : 0.7,
        "max_star_offset" : 2.0
    }

- `max_images_per_file` limits number of variance images produced per each processed file (subrun).
  Optional parameter which can be used for testing purposes.
- `skipping_interval` defines the number of events to be skipped between consecutive variance images production.
  Used to regulate the frequency of variance image production
- `cleaning` provides parameters for ctapipe's :code:`tailcut_clean` function 
- `telescope_location` specifies the telescope location. Dimensions: [deg, deg, m]
- `events_per_image` specifies how many triggered events will be used to compute one (average) variance image.
  As more events we have, as less we suffer from the NSB- and EAS- related pixel flickering,
  however the star should not move substantially during the time required to collect this number of events
- `event_type` -  event trigger type to use according to CTA nomenclature
- `check_broken_pixels` placeholder to account for camera pixels which are not fully functional for some reason.
  Not used at the moment
- `check_star_detection` currently always used and a candidate for deprecation
- `min_star_prominence` minimal star signal prominence over background, expressed in background std deviations
- `max_star_magnitude` maximal magnitude of star to be considered in the analysis
- `min_distance_between_stars` placeholder, which will be used to provide special treatment
  to extended or variable objects such as double stars`
- `max_star_offset` maximal angular distance between the pointing direction and the star [deg]


Other configuration blocks
--------------------------

The rest of the configuration blocks are parts of the standard reconstruction pipeline.
They are used for event calibration and EAS detection (and subsequent masking).

Fitting and pointing extraction
===============================

The example configuration is provided below and is quite self-explanatory. Notable parameters are:

- `use_errors` is a boolean flag which controls the fitter behavior with respect to
  whether account for the reconstructed star position uncertainty or not

- `analysis_type`: you can select between "by_run" and "by_subrun" analyses.
  In first case, the data from all subruns will be merged in one table and only the stars,
  which are reconstructed during entire run will be used in the fit.
  In second case the same analysis will go, but on a much shorter. subrun-based timescale,
  allowing the number of stars, used in a fit be different for different subruns.

.. code-block:: JSON

    {
        "FitRunner":{
            "telescope_coordinates" : {
                  "longitude" : 342.108612,
                  "lattitude" : 28.761389,
                  "elevation" : 2147
             },
             "run_number" : 2967,
             "use_errors" : true,
             "input_path" : "/path/to/output/of/previous/step/run_2967/out",
             "output_path" : "/path/to/output/of/previous/step/run_2967/fit_res/",
             "analysis_type" : "by_subrun"
        }
    }

As a result, the fitter will produce a pandas dataframe (with multiindexed columns) and will store it as a csv file.
