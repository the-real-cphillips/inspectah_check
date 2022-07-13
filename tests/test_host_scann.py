#!/usr/bin/env python

import pytest
import requests
import responses
from scann import HostScan

nginx_response = {
    "headers": {
        "Server": "nginx/1.2.0",
    },
    "text": "Index of",
}

iis_response = {
    "headers": {
        "Server": "Microsoft/IIS-7.0.1",
    },
    "text": "127.0.0.1",
}


@pytest.fixture(scope="session", autouse=True)
def host_obj():
    obj = HostScan(HostIp="127.0.0.1")
    return obj


def test_open_ports_is_list(host_obj):
    port_list = host_obj.open_ports()
    assert isinstance(port_list, list)


def test_open_ports_elements_are_ints(host_obj):
    port_list = host_obj.open_ports()
    assert isinstance(port_list[0], int)

@pytest.mark.mocked
@responses.activate
def test_request(host_obj):
    responses.get(url="http://127.0.0.1:8082")
    response = host_obj.request(8082)
    assert isinstance(response, requests.models.Response)


@pytest.mark.mocked
@responses.activate
def test_headers(host_obj):
    responses.get(url="http://127.0.0.1:8082", headers=nginx_response["headers"])
    response = host_obj.request(8082)
    assert host_obj.headers(response) == True


@pytest.mark.mocked
@responses.activate
def test_server_header(host_obj):
    responses.get(url="http://127.0.0.1:8082", headers=nginx_response["headers"])
    response = host_obj.request(8082)
    assert host_obj.server_header(response) == True


@pytest.mark.mocked
@pytest.mark.nginx
@responses.activate
def test_server_type_nginx(host_obj):
    responses.get(url="http://127.0.0.1:8082", headers=nginx_response["headers"])
    response = host_obj.request(8082)
    assert host_obj.server_type(response) == True


@pytest.mark.mocked
@pytest.mark.nginx
@responses.activate
def test_can_list_directory_nginx(host_obj):
    responses.get(url="http://127.0.0.1:8082", json={"body": nginx_response["text"]})
    response_call = host_obj.request(8082)
    response = response_call.json()
    assert response["body"] == nginx_response["text"]


@pytest.mark.mocked
@pytest.mark.iis
@responses.activate
def test_server_type_iis(host_obj):
    responses.get(url="http://127.0.0.1:8082", headers=iis_response["headers"])
    response = host_obj.request(8082)
    assert host_obj.server_type(response) == True


@pytest.mark.mocked
@pytest.mark.iis
@responses.activate
def test_can_list_directory_iis(host_obj):
    responses.get(url="http://127.0.0.1:8082", json={"body": iis_response["text"]})
    response_call = host_obj.request(8082)
    response = response_call.json()
    assert response["body"] == iis_response["text"]
