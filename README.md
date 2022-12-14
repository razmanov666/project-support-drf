# project-support-drf
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#urls-for-working)
## General info
Customer support service:
1) User writes a ticket and sends it.
2) The helpdesk sees solved, unresolved and frozen tickets (all according to the fact) and can respond to them.
3) The user can view the response of the helpdesk and add a new message (helpdesk responds to it).
4) Support can change the status of tickets.
## Technologies
Project is created with:
* python = "^3.10"
    - Django = "^4.1.1"
    - djangorestframework = "^3.14.0"
* celery = "^5.2.7"
* redis = "^4.3.4"
* postgres = "13.3"
* docker = "20.10.21"
    - docker-compose "1.29.2"

## Setup
To run this project, install it locally using docker & docker-compose:

```
$ git clone https://github.com/razmanov666/project-support-drf.git
$ cd project-support-drf
$ docker-compose up --build
```

### Urls for working:
General:
* api/tickets/
    - List all tickets
* api/tickets/<int:ticket_pk>/
    - Edit the ticket
* api/tickets_info/
    - Full info about tickets (only for admins and managers)
* api/tickets_destroy/<int:ticket_pk>/
    - Destroy the ticket
* api/tickets/<int:ticket_pk>/comments
    - Add comment for ticket
* api/tickets/<int:ticket_pk>/assigned
    - Assign ticket on self (if self is Manager)

Filter ticket by status:
* api/tickets/opened
* api/tickets/closed
* api/tickets/on_hold

Manage user role:
* api/users/<int:user_pk>/to_admin
* api/users/<int:user_pk>/to_manager
* api/users/<int:user_pk>/to_client

Manage ticket status:
* api/tickets/<int:ticket_pk>/to_opened
* api/tickets/<int:ticket_pk>/to_in_progress
* api/tickets/<int:ticket_pk>/to_done
* api/tickets/<int:ticket_pk>/to_on_hold
* api/tickets/<int:ticket_pk>/to_rejected
