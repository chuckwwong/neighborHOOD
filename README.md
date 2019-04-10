# neighborHOOD
See how safe your neighborhood is!
This project only has data on the city of Chicago.
The link to the hosted website is http://neighborhood.web.cs.illinois.edu/.


## Install Dependencies
We're using python version 2.7 (3.5 and 3.7 work as well) and we used MySQL as our database. Our front-end interface
was implemented with Angular 7.
Run `pip install Django` (v1.11.0) , `pip install mysqlclient`, `pip install pymysql`, and other dependencies.
To run the front-end, Install `node` version 10.15.3, with `npm` version 6.4.1. Run `npm install -g @angular/cli`.

## Testing
To test this project locally, in the folder hoodtest run `python manage.py <ip_address:port>`(specifying ip address and port is
optional). In frontend/interface/app/crime.service.ts, set `private baseURL='https://<ip_address:port>'` to match the address where the django server is served, then run `ng build` and
`ng test` or `ng serve`.
