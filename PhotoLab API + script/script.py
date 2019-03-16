from client_photolab import ClientPhotolab, PhotoLabStepsNotFoundException

if __name__ == '__main__':
    pass

api = ClientPhotolab()

def copy_hash_tag_styles_to_image(image, hashtag: str, output_len: int) -> list:
    """
    :param image: path to file, file or bytes of input image
    :param hashtag: hashtag used for filtration
    :param output_len: limit of output, max value = 25
    :return: list of url strings of of filters, applied to input image
    """
    combo_ids = api.image_id_list_for_tag(hashtag)
    content_url = api.image_upload(image)
    output = []
    i = 0
    for combo_id in combo_ids:
        try:
            output += [apply_combo_style(content_url, combo_id)]
        except PhotoLabStepsNotFoundException:
            continue

        i += 1
        if i >= output_len:
            break

    return output

def apply_combo_style(content_url, combo_id):
    for template_name in api.photolab_steps(combo_id):
        result_url = api.photolab_process(str(template_name), [{
            'url': content_url,
            'rotate': 0,
            'flip': 0,
            'crop': '0,0,1,1'
        }])
        content_url = result_url
    return content_url

# Usage:

with open('selfie.jpg', mode='rb') as f:
    data = f.read()

image_urls = copy_hash_tag_styles_to_image(image=data, hashtag='sex', output_len=6)
for url in image_urls:
    print(url)