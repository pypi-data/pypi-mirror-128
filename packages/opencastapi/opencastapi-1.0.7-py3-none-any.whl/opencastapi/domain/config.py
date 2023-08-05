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
import abc
import os
from functionaljlk import getMapValue, IniConfigReader, Result
import logging
import threading

class Configuration(abc.ABC):
    """Main configuration.

        Example:
        [Targets]
        admin=https://admin.opencast.org
        player=https://player.opencast.org
        worker1=https://worker1.opencast.org
        
        [Security]
        authentication=basic
        username=myuser
        password=mypassword

    """
    #_instance = None # singleton
    #_lock = threading.Lock()

    DEFAULT_PATH='/etc/opencastapi/opencastapi.conf'
    ENV_PATH_KEY='OPENCASTAPI_CONF_PATH'
    TARGETS_SECTION_NAME="Targets"
    SECURITY_SECTION_NAME="Security"

    def __init__(self, obj):
        """
            Parameters:
            obj: the subclass implementation of this configuration
        """
        pass
        #if Configuration._instance == None:
        #    Configuration._instance = obj   
        #return Configuration._instance

    # PROVIDES INDEX SYNTAX []
    def __getitem__(self, key):
        logging.debug(f"Fetching conf key \"{key}\"")
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get(self, key):
        return self.__getitem__(key)

    @abc.abstractmethod
    def target(self, target_id: str) -> str:
        """Getter URL for target id from a map of str -> URL where str is a target_id and URL is a urlparse.ParseResult 
            
            Supports arbitrary number of server urls for Opencast instances.

            Parameters:
            target_id (str): example may be one of [admin, player, worker] whereby the case is sensitive.

            Return:
            target_url (Result[urlparse.ParseResult]): The URL retrieved.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def username(self):
        raise NotImplementedError

    @abc.abstractmethod
    def password(self):
        raise NotImplementedError

    def encrypt(self, value) -> str:
        if value is None or len(value) == 0:
            return ""
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key.encode(''), AES.MODE_CFB, iv)

    def decrypt(self) -> str:
        pass

class DefaultsConfiguration(Configuration):
    pass
class EnvironmentThenFileConfiguration(Configuration):
    """

        Priority:
         1. Use path provided
         2. Use environment variable
         3. Use default path
    """
    def __init__(self, path: str=None):
        """Constructor

            Policy: Fail to construct if the configuration is not sufficient.
        """
        determined_path = Result.of(path)\
            .orElse(Result.of(os.environ.get(Configuration.ENV_PATH_KEY)))\
            .getOrElse(Configuration.DEFAULT_PATH)
        reader = IniConfigReader(determined_path, f"Consider setting environment variable {Configuration.ENV_PATH_KEY}.") 
        self._target_map = reader.getEntries(section=Configuration.TARGETS_SECTION_NAME)\
            .map(lambda l: dict((a,b) for (a,b) in l))
        self._username = reader.getProperty(section=Configuration.SECURITY_SECTION_NAME, key='username')\
            .getOrElse(lambda: logging.error(f'Config missing {Configuration.SECURITY_SECTION_NAME} section with username key.'))
        self._password = reader.getProperty(section=Configuration.SECURITY_SECTION_NAME, key='password')\
            .getOrElse(lambda: logging.error(f'Config missing {Configuration.SECURITY_SECTION_NAME} section with password key.'))
        super().__init__(self)

    def target(self, target_id: str) -> str:
        """

            Parameters:
            target_id (str): The id of the configuration key under the section Configuration.TARGET_SECTION_NAME.

            Return:
            Result.Success[str] if found.
            Result.Failure if not found.
        """
        return self._target_map\
            .flatMap(lambda m: getMapValue(target_id, m)).getOrException()

    def username(self) -> str:
        return self._username

    def password(self) -> str:
        return self._password

