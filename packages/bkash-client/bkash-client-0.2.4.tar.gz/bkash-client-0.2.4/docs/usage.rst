=====
Usage
=====

**IN DEVELOPMENT! DO NOT USE IN PRODUCTION!!**

To use bkash-client in a project:

.. code-block:: python

	from bkash_client import get_client, ClientTypeEnum
	client = get_client(credentials, type=ClientTypeEnum.IFRAME_BASED)


Basic Interaction
------------------

Every Request will take either the path parameter as an string, or a dict, or specific pydantic model for Request (see dataclasses for all Request and Response Models).

In return it will:

* Return a Response object based on request type.
* Return an Error Response in case of non-network errors.
* Raise an Error in case of network error.

