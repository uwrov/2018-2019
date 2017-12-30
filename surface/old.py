# attempts to connect to the optionally specified cameras
# returns the number of cameras found
def cameraSetup(p1=1, p2=2):
    global cam1, cam2
    global image

    try:
        p1 = int(p1)
    except (ValueError):
        p1 = 1
    try:
        p2 = int(p2)
    except (ValueError):
        p2 = p1 + 1

    cam1 = cv2.VideoCapture(p1)
    cam2 = cv2.VideoCapture(p2)

    cam1.grab()
    _, testImg1 = cam1.retrieve()
    cam2.grab()
    _, testImg2 = cam2.retrieve()

    if testImg1 == None and testImg2 == None:
        print "cameraSetup: no cameras found"
        return 0
    elif testImg1 == None and not testImg2 == None:
        cam1, cam2 = cam2, cam1
        testImg1, testImg2 = testImg2, testImg1

    cam1.set(cv.CV_CAP_PROP_FRAME_WIDTH, DESIRED_IMAGE_SIZE['width'])
    cam1.set(cv.CV_CAP_PROP_FRAME_HEIGHT, DESIRED_IMAGE_SIZE['height'])
    if not testImg2 == None:
        cam2.set(cv.CV_CAP_PROP_FRAME_WIDTH, DESIRED_IMAGE_SIZE['width'])
        cam2.set(cv.CV_CAP_PROP_FRAME_HEIGHT, DESIRED_IMAGE_SIZE['height'])

    c1w = cam1.get(cv.CV_CAP_PROP_FRAME_WIDTH)
    c1h = cam1.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
    if not testImg2 == None:
        c2w = cam2.get(cv.CV_CAP_PROP_FRAME_WIDTH)
        c2h = cam2.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
    else:
        c2w = c2h = 0

    IMAGE_SIZE['width'] = max(c1w, c2w)
    IMAGE_SIZE['height'] = max(c1w, c2w)

    image = numpy.zeros((IMAGE_SIZE['width'], IMAGE_SIZE['height'] * 2), numpy.uint8)

    if testImg2 == None:
        return 1
    else:
        return 2


# Return the latest image from the camera
# Image type 1 returns the image from camera 1
# Image type 2 returns the image from camera 2
# Image type 3 returns both images stacked vertically
def getImage(imageType):
    if imageType == 1:
        cam1.grab()
        _, img1 = cam1.retrieve()

        if not img1 == None:
            # rotate image
            img1 = numpy.rot90(img1)
            # flip image
            img1 = img1[::-1, :,]
            # switch color channels because cv2 and pygame don't play nice together
            img1[:,:,[0,2]] = img1[:,:,[2, 0]]
        return img1

    elif imageType == 2:
        cam2.grab()
        _, img2 = cam2.retrieve()

        if not img2 == None:
            # rotate image
            img2 = numpy.rot90(img2)
            # flip image
            img2 = img2[::-1, :,]
            # switch color channels because cv2 and pygame don't play nice together
            img2[:,:,[0,2]] = img2[:,:,[2, 0]]
        return img2

    elif imageType == 3:
        cam1.grab()
        _, img1 = cam1.retrieve()

        cam2.grab()
        _, img2 = cam2.retrieve()

        img1 = numpy.rot90(img1)
        img1 = img1[::-1, :,]
        img1[:,:,[0,2]] = img1[:,:,[2, 0]]

        img2 = numpy.rot90(img2)
        img2 = img2[::-1, :,]
        img2[:,:,[0,2]] = img2[:,:,[2, 0]]

        # Add images to blank image, puts 2 images onto 1 frame
        image[0 : IMAGE_SIZE['width'], 0 : IMAGE_SIZE['height']] = img1
        image[0 : IMAGE_SIZE['width'], IMAGE_SIZE['height'] : IMAGE_SIZE['height'] * 2] = img2

        return image

    else:
        print "getImage: imageType " + str(imageType) + " is not a valid image type"
        return None
