import os

def main ():
    extensions = [
        ".jpg",
        ".png"
    ]
    root = os.getcwd ()
    imgs = os.path.join (root, "IMGS")

    for character in os.listdir (imgs):
        if ("." in character):
            continue
        character = os.path.join (imgs, character)
        
        for item in os.listdir (character):
            item = os.path.join (character, item)

            if (os.path.isdir (item)):
                for image in os.listdir (item):
                    image_orig = image
                    if (os.path.isfile (os.path.join(item, image))):
                        if (" " not in image):
                            image_save = image
                            for extension in extensions:
                                if (extension in image):
                                    image = image.replace (extension, "")
                            
                            
                            
                            image = image[-2:]
                            if (not image.isnumeric ()):
                                image = image_save[:-5] + "0" + image_save[-5:]
                            else:
                                image = image_save
                            
                            os.rename (
                                os.path.join (item, image_orig),
                                os.path.join (item, image)
                            )



if (__name__ == "__main__"):
    main ()