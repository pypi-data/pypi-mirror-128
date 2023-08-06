# cosmics
[![pipeline status](https://gitlab.com/emmerich-os/cosmics/badges/main/pipeline.svg)](https://gitlab.com/emmerich-os/cosmics/-/commits/main)
[![coverage report](https://gitlab.com/emmerich-os/cosmics/badges/main/coverage.svg)](https://gitlab.com/emmerich-os/cosmics/-/commits/main)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A set of helper classes suitable for an event-driven software design. Inspired by the Cosmic Python book.

The API documentation can be found [here](https://emmerich-os.gitlab.io/cosmics).

## Helper Classes

- Repository as a database inferface.
- Client for interaction between repository and database. Allows to decouple the repository from the database type.
- Messagebus for forwarding commands and events to their respective handler functions.
- Unit of Work for processing commands/events with(-out) database access.
