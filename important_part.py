@main.command("evaluate", help="Evaluate model by estimating image tag.")
@click.argument(
    "target_paths",
    nargs=-1,
    type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True),
)
@click.option(
    "--project-path",
    type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True),
    help="Project path. If you want to use specific model and tags, use --model-path and --tags-path options.",
)
@click.option(
    "--model-path",
    type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--tags-path",
    type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False),
)
@click.option("--threshold", default=0.5)
@click.option("--allow-gpu", default=False, is_flag=True)
@click.option("--compile/--no-compile", "compile_model", default=False)
@click.option(
    "--allow-folder",
    default=False,
    is_flag=True,
    help="If this option is enabled, TARGET_PATHS can be folder path and all images (using --folder-filters) in that folder is estimated recursively. If there are file and folder which has same name, the file is skipped and only folder is used.",
)
@click.option(
    "--save-txt",
    default=False,
    is_flag=True,
    help="Enable this option to save tags to a txt file with the same filename.",
)
@click.option(
    "--folder-filters",
    default="*.[Pp][Nn][Gg],*.[Jj][Pp][Gg],*.[Jj][Pp][Ee][Gg],*.[Gg][Ii][Ff]",
    help="Glob pattern for searching image files in folder. You can specify multiple patterns by separating comma. This is used when --allow-folder is enabled. Default:*.[Pp][Nn][Gg],*.[Jj][Pp][Gg],*.[Jj][Pp][Ee][Gg],*.[Gg][Ii][Ff]",
)
@click.option("--verbose", default=False, is_flag=True)
def evaluate(
    target_paths, # I guess its this one
    project_path,
    model_path,
    tags_path,
    threshold,
    allow_gpu,
    compile_model,
    allow_folder,
    save_txt,
    folder_filters,
    verbose,
):
    if verbose:
        warnings.filterwarnings("always")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    dd.commands.evaluate(
        target_paths,
        project_path,
        model_path,
        tags_path,
        threshold,
        allow_gpu,
        compile_model,
        allow_folder,
        save_txt,
        folder_filters,
        verbose,
    )