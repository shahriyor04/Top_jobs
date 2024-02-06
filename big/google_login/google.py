from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The token is either invalid or has expired"


# {"type": "google",
#  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1ZjRiZjQ2ZTUyYjMxZDliNjI0OWY3MzA5YWQwMzM4NDAwNjgwY2QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMzI5NTkwNzg3MzEtNWtjZjQxcmRmb3Q4Nzh2aXZvZDl2dnRpN2I2NjltbWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIxMzI5NTkwNzg3MzEtNWtjZjQxcmRmb3Q4Nzh2aXZvZDl2dnRpN2I2NjltbWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA1MDM0NzA3NTM4MzMzMTk3MDUiLCJlbWFpbCI6ImJvcm9ub3ZzaGFocml5b3IyMDA0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYmYiOjE2OTkwNzk5NjQsIm5hbWUiOiJTaGFocml5b3IgQm9yb25vdiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLeG1SWWVlWXE1SmxGLXlXQ3FtLWdBUTkzc2h4TzdtMEI1cHllNnZCWkNIZz1zOTYtYyIsImdpdmVuX25hbWUiOiJTaGFocml5b3IiLCJmYW1pbHlfbmFtZSI6IkJvcm9ub3YiLCJsb2NhbGUiOiJydSIsImlhdCI6MTY5OTA4MDI2NCwiZXhwIjoxNjk5MDgzODY0LCJqdGkiOiJhNDE0ZmVjOWYxZTQ2ZGVkOTU0ODc4MTlmMjFiMzA4NzBmMjRjNGFiIn0.gwEEYhyn-VnsKsQP3G-ts5ZTKguYzFe2LTkCPeLAaU3lz3G-Hs6Z6x8rMw59Cp-RZ1xj8Du5SSPjTit0yOBq09o3sNdmdxWDsIvKjrhshV5yxLoKmXqbr_mhXOttHd67K1H-MkKFi_BND1To2pKkoW2TZQHzHV6dHt1kBX9GNf91B7cnA427dQRA-tsM4_U-eie_zJ95EBJxHezBw2VUeJDXIuas7Yaa9DR7zZhhRiXS9cGohMFnlRr8gcjH_4wojPZqGTY0TZt3fHkxfxsJN0QsK009CbJeBnUTRCCOMdgyMf7CpEujKv1vCKOE7v9SixkhMfiFrtT0814oV_izvA",
#  "user_id": "OTQ0Njc2NDM5"}
