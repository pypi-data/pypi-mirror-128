#!/usr/bin/env python3
#
# Copyright 2021 Jonathan Lee Komar
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from typing import Callable, Dict
from opencastapi.domain.config import Configuration,EnvironmentThenFileConfiguration
from opencastapi.domain.call import OpencastApiCallable
import logging

class OpencastApi():
    """Main point of entry for API calls to Opencast nodes.

        Objects created from this class abstract away the details of API calls to Opencast.
        Simply create an object of this type and use its methods to interact with Opencast nodes.
    """
    def __init__(self, conf: Configuration=EnvironmentThenFileConfiguration):
       self._conf = conf()

    def create_call(self, 
        target: str="",
        http_verb: str="", 
        path: str="", 
        parameters: Dict[str,str]={},
        headers: Dict[str, str]={'Content-Type': 'application/json', 'Accept':'application/json', 'X-Requested-Auth': 'Basic', 'Access': 'application/v1.6.0+json', "accept-charset": "UTF-8"}) -> Callable[[str,str,Dict[str,str],Dict[str,str]], str]:
        data=b"",
        auth_strategy: str="basic"
        """
            Parameters:
            http_verb: HTTP Verb
            path: Path segment of request
            parameters: Parameters segment of request
            headers: Headers of the request
        """
        return OpencastApiCallable(
            http_verb=http_verb, 
            address=self._conf.target(target),
            path=path, 
            parameters=parameters, 
            headers=headers,
            data=data,
            auth_strategy=auth_strategy, 
            username=self._conf.username(),
            password=self._conf.password())
