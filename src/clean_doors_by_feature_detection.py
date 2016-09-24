import cv2
from misc_utils import is_not_boring_image, make_grey
import shutil
import os.path
import os
from joblib import Parallel, delayed


def parallel_try(subdir, file_name):
    full_name = os.path.join(subdir, file_name)
    
    img = cv2.imread(full_name)
    img = make_grey(img)
    #cv2.imshow("image", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    if is_not_boring_image(img):
        shutil.copy(full_name, sys.argv[2])
    return

    
def filter_folder(folder):
    """
    Itrates over a folder and sub folders, and adds the images to the dataset
    """
    for subdir, dirs, files in os.walk(folder):
        
        #for file_name in files:
        outputs = Parallel(n_jobs=4, backend="threading")(delayed(parallel_try)(subdir, file_name)
                                                          for file_name in files)



if __name__ == "__main__":
    filter_folder(sys.argv[1])
