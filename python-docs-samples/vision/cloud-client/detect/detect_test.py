# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import storage

import detect

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
OUTPUT_PREFIX = 'OCR_PDF_TEST_OUTPUT'
GCS_SOURCE_URI = 'gs://{}/HodgeConj.pdf'.format(BUCKET)
GCS_DESTINATION_URI = 'gs://{}/{}/'.format(BUCKET, OUTPUT_PREFIX)


def test_labels(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect.detect_labels(file_name)
    out, _ = capsys.readouterr()
    assert 'Labels' in out


def test_labels_uri(capsys):
    file_name = 'gs://{}/vision/wakeupcat.jpg'.format(BUCKET)
    detect.detect_labels_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'Labels' in out


def test_labels_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/wakeupcat.jpg'
    detect.detect_labels_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'Labels' in out


def test_landmarks(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect.detect_landmarks(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_landmarks_uri(capsys):
    file_name = 'gs://{}/vision/landmark.jpg'.format(BUCKET)
    detect.detect_landmarks_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_landmarks_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/landmark.jpg'
    detect.detect_landmarks_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'Palace' in out


def test_faces(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/face_no_surprise.jpg')
    detect.detect_faces(file_name)
    out, _ = capsys.readouterr()
    assert 'POSSIBLE' in out


def test_faces_uri(capsys):
    file_name = 'gs://{}/vision/face_no_surprise.jpg'.format(BUCKET)
    detect.detect_faces_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'POSSIBLE' in out


def test_faces_http(capsys):
    uri = ('https://storage-download.googleapis.com/{}/vision/' +
           'face_no_surprise.jpg')
    detect.detect_faces_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'POSSIBLE' in out


def test_logos(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/logos.png')
    detect.detect_logos(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_logos_uri(capsys):
    file_name = 'gs://{}/vision/logos.png'.format(BUCKET)
    detect.detect_logos_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_logos_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/logos.png'
    detect.detect_logos_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'Google' in out


def test_safe_search(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect.detect_safe_search(file_name)
    out, _ = capsys.readouterr()
    assert 'VERY_LIKELY' in out
    assert 'racy: ' in out


def test_safe_search_uri(capsys):
    file_name = 'gs://{}/vision/wakeupcat.jpg'.format(BUCKET)
    detect.detect_safe_search_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'VERY_LIKELY' in out
    assert 'racy: ' in out


def test_safe_search_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/wakeupcat.jpg'
    detect.detect_safe_search_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'VERY_LIKELY' in out
    assert 'racy: ' in out


def test_detect_text(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect.detect_text(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_text_uri(capsys):
    file_name = 'gs://{}/vision/text.jpg'.format(BUCKET)
    detect.detect_text_uri(file_name)
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_text_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/text.jpg'
    detect.detect_text_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert '37%' in out


def test_detect_properties(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect.detect_properties(file_name)
    out, _ = capsys.readouterr()
    assert 'frac' in out


def test_detect_properties_uri(capsys):
    file_name = 'gs://{}/vision/landmark.jpg'.format(BUCKET)
    detect.detect_properties_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'frac' in out


def test_detect_properties_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/landmark.jpg'
    detect.detect_properties_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'frac' in out


# Vision 1.1 tests
def test_detect_web(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/landmark.jpg')
    detect.detect_web(file_name)
    out, _ = capsys.readouterr()
    assert 'Description: Palace of Fine Arts Theatre' in out
    assert 'Best guess label: palace of fine arts' in out


def test_detect_web_uri(capsys):
    file_name = 'gs://{}/vision/landmark.jpg'.format(BUCKET)
    detect.detect_web_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'Description: Palace of Fine Arts Theatre' in out
    assert 'Best guess label: palace of fine arts' in out


def test_detect_web_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/landmark.jpg'
    detect.detect_web_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'Description: Palace of Fine Arts Theatre' in out
    assert 'Best guess label: palace of fine arts' in out


def test_detect_web_with_geo(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/city.jpg')
    detect.web_entities_include_geo_results(file_name)
    out, _ = capsys.readouterr()
    assert 'Zepra' in out or 'Electra Tower' in out


def test_detect_web_with_geo_uri(capsys):
    file_name = 'gs://{}/vision/city.jpg'.format(BUCKET)
    detect.web_entities_include_geo_results_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'Zepra' in out or 'Electra Tower' in out


def test_detect_document(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/text.jpg')
    detect.detect_document(file_name)
    out, _ = capsys.readouterr()
    assert 'class' in out


def test_detect_document_uri(capsys):
    file_name = 'gs://{}/vision/text.jpg'.format(BUCKET)
    detect.detect_document_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'class' in out


def test_detect_document_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/text.jpg'
    detect.detect_document_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'class' in out


def test_detect_crop_hints(capsys):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/wakeupcat.jpg')
    detect.detect_crop_hints(file_name)
    out, _ = capsys.readouterr()
    assert 'bounds: (0,0)' in out


def test_detect_crop_hints_uri(capsys):
    file_name = 'gs://{}/vision/wakeupcat.jpg'.format(BUCKET)
    detect.detect_crop_hints_uri(file_name)
    out, _ = capsys.readouterr()
    assert 'bounds: (0,0)' in out


def test_detect_crop_hints_http(capsys):
    uri = 'https://storage-download.googleapis.com/{}/vision/wakeupcat.jpg'
    detect.detect_crop_hints_uri(uri.format(BUCKET))
    out, _ = capsys.readouterr()
    assert 'bounds: (0,0)' in out


def test_async_detect_document(capsys):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 0

    detect.async_detect_document(
        gcs_source_uri=GCS_SOURCE_URI,
        gcs_destination_uri=GCS_DESTINATION_URI)
    out, _ = capsys.readouterr()

    assert 'Hodge conjecture' in out
    assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 3

    for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
        blob.delete()
