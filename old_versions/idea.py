
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io, os

    credential_path = "C:\\Users\\param\\OneDrive\\Documents\\GitHub\\Idea-Hacks-2020\\credentials.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description).encode("utf-8"))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def temp_text():
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import vision
    from google.cloud.vision import types

    credential_path = "C:\\Users\\param\\OneDrive\\Documents\\GitHub\\Idea-Hacks-2020\\credentials.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('C:\\Users\\param\\OneDrive\\Documents\\GitHub\\Idea-Hacks-2020\\images\\IMG-1627.JPG')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)


if __name__ == '__main__':
    # detect_text("C:\\Users\\param\\OneDrive\\Documents\\GitHub\\Idea-Hacks-2020\\images\\IMG-1627.JPG")
    temp_text()
