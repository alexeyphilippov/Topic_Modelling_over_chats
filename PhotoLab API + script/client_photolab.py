import requests
import logging
import json
import re
import io
from collections import OrderedDict

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s')

class ClientPhotolab(object):

    api_endpoint = 'http://api-soft.photolab.me'
    api_upload_endpoint = 'http://upload-soft.photolab.me/upload.php?no_resize=1'
    api_endpoint_proxy = 'http://api-proxy-soft.photolab.me'

    web_endpoint = 'https://photolab.me'

    def image_upload(self, image):
        image_blob = None
        if type(image) is str:
            image_blob = open(image, 'rb')
        elif isinstance(image, io.IOBase):
            image_blob = image
        elif type(image) is bytes:
            image_blob = image
        else:
            raise Exception('image not file and not filename')

        files = {'file1': image_blob}
        response = requests.post(self.api_upload_endpoint, files=files)
        resp_body = response.text
        logging.info('response: {}'.format(resp_body))
        return resp_body

    def photolab_process(self, template_name, contents):
        form = {
            'template_name' : template_name
        }
        for i in range(0, len(contents)):
            content = contents[i]
            form['image_url[' + str(i+1) + ']'] = content['url']
            if 'crop' in content:
                form['crop[' + str(i+1) + ']'] = content['crop']
            if 'flip' in content:
                form['flip[' + str(i+1) + ']'] = content['flip']
            if 'rotate' in content:
                form['rotate[' + str(i+1) + ']'] = content['rotate']

        endpoint = '{}/photolab_process.php'.format(self.api_endpoint)
        return self._post_query(endpoint, data=form)

    def photolab_steps(self, combo_id):
        templates = self.templates_list_for_photo(combo_id)
        # form = {
        #     'combo_id' : combo_id
        # }
        # endpoint = '{}/photolab_steps.php'.format(self.api_endpoint)
        return templates

    def templates_list_for_photo(self, photo_id):
        resp = self._get_query(endpoint=self.web_endpoint + '/d/{}'.format(photo_id))
        pattern = '(?<=\<a href\=\"\/t\/)(.*)(?=\"\>)'
        template_list = re.findall(pattern, resp)
        return list(OrderedDict.fromkeys(template_list))

    def image_id_list_for_tag(self, tag: str):
        resp = self._get_query(endpoint= self.web_endpoint + '/tag/{}'.format(tag))
        pattern = '(?<=\"\/d\/)(.*)(?=\" d)'
        id_list = re.findall(pattern, resp)
        return id_list

    def _get_query(self, endpoint):
        response = requests.get(endpoint)
        resp_body = response.text
        logging.info('responce: {}'.format(resp_body))
        if response.status_code != 200:
            raise Exception('error: {}'.format(resp_body))

        return resp_body

    def _post_query(self, endpoint, data=None, files=None):
        response = requests.post(endpoint, data=data, files=files)
        resp_body = response.text
        logging.info('response: {}'.format(resp_body))
        if response.status_code != 200:
            raise Exception('_post_query: {}, error: {}'.format(endpoint, resp_body))

        return resp_body

class PhotoLabStepsNotFoundException(Exception):
    """
    In some cases api does not tell us the list of filters applied to images.
    """
    pass
