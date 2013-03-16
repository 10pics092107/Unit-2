NOTE- the server program must be running before you try to run the client program
             and the program must be run from unix environment only as input = [self.server,sys.stdin] works in unix, in windows it would give an error.
requires enchant module 

Sample queries the client can ask
1)to list the urls
url
2)to list features supported by a given url
features:url-www.qxzHNnTSYoGy.edu
3)to list media_queries,urls having screen size true
media_queries,url:small_screen_size-true

