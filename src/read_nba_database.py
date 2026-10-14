import kagglehub
import shutil

def main():
    # Download latest version
    dataset_path = kagglehub.dataset_download("wyattowalsh/basketball")
    print("Path to dataset files:", dataset_path)

    # NOTE(Khanh): the downloaded dataset is a directory, we're copying the entire DIRECTORY, not a single file
    shutil.copytree(dataset_path, "./cmpe138_project")


if __name__=="__main__":
    main()


