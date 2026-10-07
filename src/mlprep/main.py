from mlprep.utils import prep_img, prep_img_logic


def main():
    source = "images"
    target = "processed_images"
    prep_img(source, target, 256, 256)
    return 1

if __name__ == "__main__":
    import sys
    # If user provides arguments in terminal, run the Click CLI
    if len(sys.argv) > 1:
        prep_img_logic()
    else:
        main()