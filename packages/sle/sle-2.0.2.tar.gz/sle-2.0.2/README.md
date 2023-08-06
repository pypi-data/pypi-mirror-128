# Python SLE

Implementation of the CCSDS Space Link Extension (SLE) API in Python. It
provides the [RAF (Return All Frames)](docs/911x1b4.pdf) and
[RCF (Return Channel Frames)](docs/911x2b3.pdf) Return Link Services and the
[CLTU Forward Link Service](docs/912x1b4.pdf).

The CCSDS Space Link Extension (SLE) services are used by all major space
agencies to interconnect ground stations to mission control systems. The
SLE is a standardized protocol that enable such cross-support. In basic terms,
a groundstation communicates with a spacecraft through CCSDS telecommand and
telemetry frames. The transfer of those frames between a groundstation and
a remote mission control system is done via SLE, which is essentially just a
container protocol that runs over [TCP/IP](docs/913x1b2.pdf).
On the side of the groundstation there sits a SLE provider gateway and on
the mission control side there is a SLE user gateway.

This Python package implements the SLE User API and can be used to develop
SLE user and provider gateway applications on top of it.

## Installation

Install via pip:

```bash
$ pip install sle
```

## Example

To create a service for receiving all return frames, we create a RAF User.
Then we bind to the remote SLE Provider and start the reception of frames.

```python
import sle

raf_service = sle.RaServicefUser(
    service_instance_identifier=SI_IDENTIFIER,
    responder_host=RESPONDER_HOST,
    responder_port=RESPONDER_PORT,
    auth_level="bind",  # or "all" or None
    local_identifier=LOCAL_IDENTIFIER,
    peer_identifier=PEER_IDENTIFIER,
    local_password=LOCAL_PASSWORD,
    peer_password=PEER_PASSWORD)

raf_service.bind()
raf_service.start()
time.sleep(10)  # wait for 10 seconds to show incoming frames
raf_service.stop()
raf_service.unbind()

```

## Documentation

The API documentation is in [docs/README.md](docs/README.md).

## Contribute

- Issue Tracker: https://gitlab.com/librecube/lib/python-sle/-/issues
- Source Code: https://gitlab.com/librecube/lib/python-sle

To learn more on how to successfully contribute please read the contributing
information in the [LibreCube guidelines](https://gitlab.com/librecube/guidelines).

## Support

If you are having issues, please let us know. Reach us at
[Matrix](https://app.element.io/#/room/#librecube.org:matrix.org)
or via [Email](mailto:info@librecube.org).

## License

The project is licensed under the MIT license. See the [LICENSE](./LICENSE.txt) file for details.
