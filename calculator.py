"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
from functools import reduce

def resp_body(msg):
  lines = msg.split('\n')
  body = ""
  for line in lines:
    body += f"{line}<br />"
  print(body)
  return body

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    result = sum(args)
    return str(result)

def multiply(*args):
    result = reduce((lambda x,y: x*y), args)
    return str(result)

def divide(*args):
    result = reduce((lambda x,y: x/y), args)
    return str(result)

def subtract(*args):
  result = reduce((lambda x,y: x-y), args)
  return str(result)

def calc(*args):
  welcome = """
  Welcom to calculator
  usage http://localhost:8080/<func>/arg1/arg2/../argN
  where "func" is one of the following:
    add,
    subtract.
    multiply,
    divide
  """
  return welcome

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': calc,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide,
    }

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    # func = add
    # args = ['25', '32']
    print(f">>>> {func_name}, {args}")

    if func_name not in funcs:
      raise NameError
    elif (func_name != '') & (len(args) < 2):
      raise ValueError("required at least 2 operans")
    try:
      func = funcs[func_name]
    except KeyError as e:
      raise NameError
    try:
      args = list(map(int, args))
    except ValueError:
      raise ValueError("all arguments must be integers")

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    print(f"+++ route: {environ['PATH_INFO']}")
    headers = [("Content-type", "text/html")]
    try:
      path = environ.get('PATH_INFO', None)
      if path is None:
          raise NameError
      func, args = resolve_path(path)
      print(f"+++ func: {func}, args: {args}")
      # body = func(*args)
      body = resp_body(func(*args))
      status = "200 OK"
    except ZeroDivisionError:
      status = "400 Bad Request"
      body = "<h1>Error code: 400</h1>"
      body += ""
      # body += "<h1>Division by Zero</h1>"
      body += "<h1 style=\"{}\">Division by Zero</h1>".format("color:red;")
    except NameError:
      status = "404 Not Found"
      body = body = "<h1>Error code: 404</h1>"
      body += ""
      # body += "<h1>Not Found</h1>"
      body += "<h1 style=\"{}\">Not Found</h1>".format("color:red;")
    except ValueError as e:
      status = "500 Internal Server Error"
      body = "<h1>Error code: 500</h1>"
      body += ""
      # body += f"<h1>{str(e)}</h1>"
      body += "<h1 style=\"{}\">{}</h1>".format("color:red;", str(e))

    except Exception as e:
      status = "500 Internal Server Error"
      body = body = "<h1>Error code: 500</h1>"
      body += "<h1>Internal Server Error</h1>"
      body += ""
      body += f"<h1 style=\"color:red;\">{str(e)}</h1>"
      print(traceback.format_exc())
    finally:
      headers.append(('Content-length', str(len(body))))
      start_response(status, headers)
      return [body.encode('utf8')]

    # status = "200 OK"
    # body = "tra la la"
    # func, args = resolve_path(path)
    # body = func(*args)
    # headers.append(('Content-length', str(len(body))))
    # start_response(status, headers)
    # return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
    
