# brestclient
in terminal rest client, super simple and super useful

# how to install
- install [python3](https://www.python.org/downloads/)
- install with pip `python3 -m pip install brestclient`

# how to use
## overview
first of all create a file with requests  
syntax similar to other rest clients:
- [emacs restclient-mode](https://github.com/pashky/restclient.el)
- [vscode restclient](https://github.com/Huachao/vscode-restclient)

then perform requests with `python3 -m brestclient ./path/po/file`

## file syntax
```restclient
### request name
# name REQUIRED to be UNIQUE in entire file
# there should not be any two requests with same name
# it's matter to have no spaces before ###
# all next lines started with # is a comments, will be ignored
# it's matter to use ### only in the begining of request
# cuz ### means a request start, for comments use # or ##
# METHOD - can be any html method, case does not matter
# URL - any valid http url, if protocol is not specified (google.com for example)
# request will be performed with https protocol
# headers - all what is left of : is a header key,
# all is right of : is a header value
# both will be striped
# body will be striped as one big line
METHOD URL?a={{in_url_variable}}
HEADER_KEY: HEADER_VALUE
HEADER_KEY: HEADER_VALUE
HEADER_{{var1}}: HEADER_{{var2}}

{
    "all lines till the end are {{variables_can_be_everywhere}} lines of a request body",
    "there can be anything, json or plane text, or nothing if it's GET request"
}
```

## file example
```restclient
### yandex request
# it's just a search get request, no headers or body requeired
GET https://ya.ru?q=coala


### ask google fo no reason
POST google.com?q=weffwe
Authorization: Bearer foj23fjjf03jf3029jf30jf3029j23f09
content-type: application/json

{
    "something": [1, 2, 3],
    "please_collect_all_my_data": true
}
```

## perform requests
run `brestclient` with requests file specified
```bash
python3 -m brestclient ./path/to/file
```
then pick a request by number  
when request will be done, it will print to you status code,  
response headers and body. if body in json format - it will be pretty printed

also you can run it without interactive menu, for it specify --query or -q param  
in this case request will be finded by it's name
```bash
python3 -m brestclient ./path/to/file -q google
```

or you can run it with -l or --list argument to print list of requests with their order number  
and then run program with -n NUMBER or --request-number NUMBER to perform request  
example:
```bash
python3 -m brestclient ./path/to/file -l
1: first request
2: second request
...

python3 -m brestclient ./path/to/file -n 2
```

# development plans
- [X] just requests
- [X] json output parsing, pretty print
- [X] make it a python package
- [X] create documentation how to use
- [X] publish package
- [ ] save output to variables, and ability to use them later
- [ ] if response in html format - ask for open it in browser
- [ ] flag -r to get raw response in http format
- [ ] json output syntax coloring
- [ ] html output parsing, pretty print and syntax coloring
