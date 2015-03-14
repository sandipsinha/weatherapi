# weatherapi
A micro script which pulls weather data from api.weathersource.com and creates two APIs to pull weather related data via zip codes(for US only).

It has 2 end points. 

1. /<int:zipcode>/temperature-stats : If the site is called using for ex. localhost:8080/94566/temeprature-stats
it will give 

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: length

{
    "current": 65,
    "historical": [
        {
            "date": "2015-01-02T00:00:00Z",
            "min": 40,
            "max": 66,
        },
        ....
2./temperature-stats/<postalcodes> if it is called using localhost:8080/temperature-stats/90210,94566 it will give the same output as above but for all the zip codes(upto 10).
