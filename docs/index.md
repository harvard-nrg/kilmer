# Welcome
Kilmer is a software project designed to help you run [iProc][iProc] validation
tests.

The main command line utility `kilmer` will clone two branches from iProc, 
install each branch into a separate [virtual environment][venv], run a data 
set through each branch, compare the results, and generate a report of any 
differences.

## Installation
Just use `pip`

```bash
python3.11 -m venv kilmer
source kilmer/bin/activate
(kilmer) pip install --upgrade pip
(kilmer) pip install git+https://github.com/harvard-nrg/kilmer
```

## Configuration
`kilmer` uses a simple configuation file in [YAML][YAML] format. You will 
pass this configuration file using the `-c|--config` argument

```bash
kilmer --config kilmer.yaml ...
```

### example
```yaml
containers:
    # This is where to define the path to your singularity container 
    # image
    wrapper: /path/to/kilmer.sif

inputs:
    # This is where to define your input datasets 
    # directory. An example subject directory should 
    # look like the following
    #
    # datasets
    # └── ASDF
    #     ├── configs
    #     │   ├── cluster_requests.csv
    #     │   └── tasktype_consolidated.csv
    #     ├── mocks
    #     │   └── freesurfer.tar.gz
    #     ├── README.md
    #     └── subject_lists
    #         ├── ASDF.cfg
    #         └── scanlist_ASDF.csv
    datasets: /path/to/datasets

outputs:
    # This is where to define where all 
    # iProc branches will be installed
    branches: /path/to/branches

    # This is where to define where all 
    # iProc output will be saved
    results: /path/to/results

# This is where to define your "left" branch
left:
    url: https://github.com/harvard-nrg/iProc
    branch: main

# This is where to define your "right" branch
right:
    url: https://github.com/harvard-nrg/iProc
    branch: develop

iproc:
    # These are the iProc stages you want to run 
    # during kilmer's "launch" mode
    stages:
        - setup
        - bet
        - unwarp_motioncorrect_align
        - T1_warp_and_mask
        - combine_and_apply_warp
        - filter_and_project

validation:
    nifti:
        # This is where to define all directories 
        # and file patterns to ignore when comparing 
        # NIfTI files
        exclude:
            - .*/scratch/.*
            - .*/time_point_\d+.nii.gz$
            - .*/T1_TARG_WARP_\d+.nii.gz$
            - .*/T1_TARG_FILE_\d+.nii.gz$
            - .*/MNI_TARG_FILE_\d+.nii.gz$
```

## Container
`kilmer` will run all iProc commands within a Singularity container. This 
container has all of the required operating system dependencies installed. 

!!! question "Why?"
    The main reason for using a container is to trick iProc into thinking 
    it's writing output to `/output` by using `--bind` mounts. This will 
    ensure that any strings written to any output files that contain the 
    output directory are identical, enabling more direct file comparisons.

### building the container
The Singularity definition file is included within the `kilmer` repository 
under `singularity/kilmer.def`. To build the container, run the the following 
commands

!!! tip "proot"
    If you're building this container as a non-root user, you will need to use
    `--fake-root` or `proot`. On FASSE, you can load `proot` by running 
    `module load proot`.

```bash
singularity build kilmer.sif kilmer.def
```

## Usage
The three stages of `kilmer` are `setup`, `launch`, and `validate`.

### setup
The `setup` stage will download the `left` and `right` branches from 
iProc and install each branch into a separate virtual environment.

```bash
kilmer -c kilmer.yaml setup
```

### launch
The `launch` stage will run a dataset through either the `left` or `right` 
branch. All iProc stages will be run sequentially

!!! important "iProc configuration"
    Your subject configuration files should be configured to write all output 
    to `/output` and accept any input files from `/input`.

```bash
kilmer -c kilmer.yaml launch --subject ASDF --branch left
kilmer -c kilmer.yaml launch --subject ASDF --branch right
```

If you have a HPC cluster, you can launch the `left` and `right` branches 
in parallel.

#### mock data
You can have `kilmer` extract preprocessed data into your output directory to 
save time.

For example, to have iProc skip running FreeSurfer, you can `tar` up your 
preprocessed FreeSurfer data and place the tarball under the `mocks` directory

```bash
/path/to/datasets/ASDF/
├── configs
│   ├── cluster_requests.csv
│   └── tasktype_consolidated.csv
├── mocks
│   └── freesurfer.tar.gz
└── subject_lists
    ├── ASDF.cfg
    └── scanlist_ASDF.csv
```

Then pass the `-m|--mock` argument to `kilmer`

```bash
kilmer -c kilmer.yaml launch -s ASDF -b left --mock freesurfer
```

### validation
The `validate` stage will compare the `left` and `right` branches, look for 
differences, and generate a report file

```bash
kilmer -c kilmer.yaml validate -s ASDF
```

By default, all differences will be printed to the console and saved to 
`report.json`.

#### output file
By default, differences will be saved to `report.json` in your current working 
directory. You can customize the output file using the `-o|--output-file` 
argument

```bash
kilmer -c kilmer.yaml validate -s ASDF --output-file ASDF.json
```

For your convenience, files listed within the report will be sorted (ascending) 
based on the file's modification time.

#### reverse
By default, `kilmer` will compare the `left` branch to the `right` branch. The 
direction of this comparison is an important consideration. 

If any files that appear within the `left` branch are missing from the `right` 
branch, those files will be flagged as different. If you want to reverse the 
direction, you can pass the `-r|--reverse` flag

```bash
kilmer -c kilmer.yaml validate -s ASDF --reverse
```

You may want to use this flag if you want to compare files before your `right` 
or `left` branch is finished processing i.e., one of the branches is behind the
other.

[venv]: https://docs.python.org/3/library/venv.html
[iProc]: https://github.com/harvard-nrg/iProc/
[YAML]: https://yaml.org/spec/1.2.2/
