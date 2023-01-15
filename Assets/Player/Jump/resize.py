import PIL.Image


class ImageUtils(object):
    @classmethod
    def resize_image(cls, image: PIL.Image.Image, width=None, height=None) -> PIL.Image.Image:
        if height is None and width is not None:
            height = image.height * width // image.width
        elif width is None and height is not None:
            width = image.width * height // image.height
        elif height is None and width is None:
            raise RuntimeError("At lease one of width and height must be present")
        return image.resize((width, height))


def main():
    ImageUtils.resize_image(PIL.Image.open("Jump.png"), height=77).save(f"Jump.png")
    #for i in range(1,19):
    #    ImageUtils.resize_image(PIL.Image.open(f"{i}.png"), height=78).save(f"resized/{i}.png")


if __name__ == '__main__':
    main()
