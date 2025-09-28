def main (cam link):
  fromm .camera import capture
  capture (cam)
  a = os.system (f'curl -X POST -F "image=..." {link}')
  if a:
