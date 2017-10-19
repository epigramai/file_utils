# file_utils
This is a small library of command line tools to make file manipulation easier. At present it contains:
* categorise_images.py: look at the images in a folder and sort them to subfolders
    * Takes the path of a folder containing images, displays them one by one
    * Images in the folder are considered uncategorised, images in direct subfolders are considered categorised
    * Use right and left arrows to navigate forwards and backwards
    * Use the up arrow to view categorised images, and the down arrow to view uncategorised images
    * Pressing any letter or number moves an image into the corresponding subfolder, thus (re)categorising it
    * Pressing the backspace key uncategorises a categorised image
    * Pressing any other key exits the program
* resize_images.py: resize all the images in a subfolder and/or reduce the jpg-quality
    * Takes a list of lengths (:= max(height, width)) and a list of jpg-qualities
    * For each combination of length and jpg-quality, creates a subfolder with modified images
    * If no length or jpg-quality are supplied, the defaults are unchanged and 100 respectively
    * Optionally also applies to subfolders
    * Only works with jpg-images at present
* replace_image_names_with_numbers: rename images to 0.jpg, 1.jpg, ..., n-1.jpg
    * Optionally prepends the folder name
    * Keeps a record of the renamings. If a record already exists, this is updated rather than replaced
    * Optionally also applies to subfolders, in which case images are renamed as if they were all in the base folder