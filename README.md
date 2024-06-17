# Moydodyr API
A better implementation of the ELS booking system.

<img src="./doc/images/Screenshot_20240518_152428_Firefox.jpg" alt="Old interface screenshot" width="200"/>

Link to diagrams: https://github.com/myxit/my-diag/blob/main/moydodyr/

## Python Dev setup
A bit complex setup:
 - Python version in venv is `3.11.4`
 - Packages managed by the `poetry` package manager. Run `poetry install` in the project directory root.

## Plan
0. Poller
 - [X] authentication
 - [X] bookings scraper
 - [X] save parsed bookings in the storage 
 - [-] bookings parser
======
Last try before fall:
setup mitmproxy and check how the viewstate data get send to srv
Problem: "Next page" returns 500

======


    - [ ] walkthrough the following laundry screens
    - [ ] collect bookings for the all available laundries
 - [ ] booking reservation
 - [ ] booking cancellation
 - [ ] my bookings

1. Intermediate storage (sqlite)
 - [X] Setup
 - [ ] rethink on structure: fixed objects vs event log
 - [ ] A few user stories:
    - user looks for available nearest bookings
    - same as above with preferred laundry nr
    - same as previous with preferred time range
 
2. JSON API
    - GET /api/bookings returns JSON occupied bookings
    - GET /api/bookings returns JSON all bookings
    - POST /api/bookings
    - DELETE /api/bookings
 - [ ] Authentication 
2. Good to have
 - [ ] SSE
