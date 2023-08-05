import os 


def resolve_path_from_base(filename: str, base_path: str) -> str:
	return os.path.abspath(os.path.join(base_path, filename))

	
def path_exists(config_filepath: str) -> bool:
	return os.path.exists(config_filepath)


def create_dir(path: str):
	try:
		os.mkdir(path)
	except FileExistsError:
		pass


def join_paths(path1: str, path2: str) -> str:
	return os.path.join(path1, path2)