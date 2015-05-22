    

#Free: We shelter 

class_dict = 
{ 'D' : free,
  'E' : near,
  'F' : thresh
}

def get_cleanup_class (code):
      class = class_dict[code]
      return class(conf.cleanup_args)
