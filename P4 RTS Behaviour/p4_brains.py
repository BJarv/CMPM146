
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':
      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
        if slug.amount < .5:
          slug.state = 'fleeing'
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.resource = False
 

  def handle_event(self, message, details):
    #print 'details: ', details, ' message: ', message
    
    if self.state is 'idle':              #idle state
      if message is 'order':              #idle order
        if details is 'a':                #idle order attack
          toFight = self.body.find_nearest('Mantis')
          self.body.follow(toFight)
          self.target = toFight
          self.body.set_alarm(1)
          self.state = 'attacking'

        elif isinstance(details, tuple):  #idle order travel
          self.body.go_to(details)
          self.state = 'traveling'

        elif details is 'b':              #idle order build
          toBuild = self.body.find_nearest('Nest')
          self.body.go_to(toBuild)
          self.target = toBuild
          self.state = 'building'

        elif details is 'h':              #idle order harvest
          if self.resource:               #idle order harvest nest
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.state = 'harvesting'
            self.body.set_alarm(3)
          else:                           #idle order harvest resource
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.state = 'harvesting'
            self.body.set_alarm(3)

      elif message is 'collide':          #idle collide
        if details['what'] is 'Mantis':   #idle collide mantis
          if self.body.amount <= .5:      #idle collide mantis flee
            toFleeTo = self.body.find_nearest('Nest')
            self.target = toFleeTo
            self.body.go_to(toFleeTo)
            self.state = 'fleeing'





    elif self.state is 'harvesting':      #harvest state
      if message is 'collide':            #harvest collide
        if details['what'] is 'Nest':     #harvest collide Nest
          if details['who'] is self.target:
            self.resource = False
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.body.set_alarm(3)
          else:
            pass
            #print details

        elif details['what'] is 'Resource':#harvest collide Resource
          if details['who'] is self.target:
            self.resource = True
            self.target.amount -= .25
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.body.set_alarm(3)
          else:
            pass
            #print details

        elif details['what'] is 'Mantis': #harvest collide mantis
          if self.body.amount <= .5:      #harvest collide mantis flee
            toFleeTo = self.body.find_nearest('Nest')
            self.target = toFleeTo
            self.body.go_to(toFleeTo)
            self.state = 'fleeing'
        else:
          pass
          #print details

      if message is 'timer':              #harvest collide timer
        if self.resource:                 #harvest collide timer nest
          turnIn = self.body.find_nearest('Nest')
          self.target = turnIn
          self.body.go_to(turnIn)
          self.body.set_alarm(3)

        else:                             #harvest collide timer resource
          toHarv = self.body.find_nearest('Resource')
          self.target = toHarv
          self.body.go_to(toHarv)
          self.body.set_alarm(3)

      if message is 'order':              #harvest order
        if details is 'i':                #harvest order idle
          self.body.stop()
          self.state = 'idle'

        elif details is 'a':              #harvest order attack
          toFight = self.body.find_nearest('Mantis')
          self.body.follow(toFight)
          self.body.set_alarm(1)
          self.target = toFight
          self.state = 'attacking'

        elif isinstance(details, tuple):  #harvest order travel
          self.body.go_to(details)
          self.state = 'traveling'

        elif details is 'b':              #harvest order build
          toBuild = self.body.find_nearest('Nest')
          self.body.go_to(toBuild)
          self.target = toBuild
          self.state = 'building'



    elif self.state is 'building':        #build state
      if message is 'collide':            #build collide
        if details['what'] is 'Nest':
          if self.target is details['who']:
            self.target.amount +=.01
            if self.target.amount >= 1:
              self.state = 'idle'

        elif details['what'] is 'Mantis': #build collide mantis
          if self.body.amount <= .5:      #build collide mantis flee
            toFleeTo = self.body.find_nearest('Nest')
            self.target = toFleeTo
            self.body.go_to(toFleeTo)
            self.state = 'fleeing'

      elif message is 'order':            #build order
        if details is 'i':                #build order idle
          self.body.stop()
          self.state = 'idle'

        elif details is 'a':              #build order attack
          toFight = self.body.find_nearest('Mantis')
          self.body.follow(toFight)
          self.target = toFight
          self.body.set_alarm(1)
          self.state = 'attacking'

        elif isinstance(details, tuple):  #build order travel
          self.body.go_to(details)
          self.state = 'traveling'

        elif details is 'h':              #build order harvest
          if self.resource:               #build order harvest nest
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.state = 'harvesting'
            self.body.set_alarm(3)

          else:                           #build order harvest resource
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.state = 'harvesting'
            self.body.set_alarm(3)




    elif self.state is 'attacking':       #attack state
      if message is 'order':              #attack order
        if details is 'i':                #attack order idle
          self.body.stop()
          self.state = 'idle'

        elif isinstance(details, tuple):  #attack order travel
          self.body.go_to(details)
          self.state = 'traveling'

        elif details is 'b':              #attack order build
          toBuild = self.body.find_nearest('Nest')
          self.body.go_to(toBuild)
          self.target = toBuild
          self.state = 'building'

        elif details is 'h':              #attack order harvest
          if self.resource:               #attack order harvest nest
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.state = 'harvesting'
            self.body.set_alarm(3)

          else:                           #attack order harvest resource
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.state = 'harvesting'
            self.body.set_alarm(3)

      elif message is 'timer':            #attack timer
        print 'in attacking timer'
        toFight = self.body.find_nearest('Mantis')
        self.body.follow(toFight)
        self.target = toFight
        self.body.set_alarm(1)

      elif message is 'collide':          #attack collide
        if details['what'] is 'Mantis':
          if self.target is details['who']:
            #print 'dude'
            self.target.amount -= .05
            if self.target.amount <= 0:
              toFight = self.body.find_nearest('Mantis')
              self.body.follow(toFight)
              self.target = toFight
              self.body.set_alarm(1)
              self.state = 'attacking'



    
    elif self.state is 'fleeing':
      #print 'fleeing'
      if message is 'order':              #flee order
        if details is 'i':                #flee order idle
          self.body.stop()
          self.state = 'idle'

        elif details is 'a':              #flee order attack
          toFight = self.body.find_nearest('Mantis')
          self.body.follow(toFight)
          self.body.set_alarm(1)
          self.target = toFight
          self.state = 'attacking'
        
        elif isinstance(details, tuple):  #flee order travel
          self.body.go_to(details)
          self.state = 'traveling'
        
        elif details is 'b':              #flee order build
          toBuild = self.body.find_nearest('Nest')
          self.body.go_to(toBuild)
          self.target = toBuild
          self.state = 'building'
        
        elif details is 'h':              #flee order harvest
          if self.resource:               #flee order harvest nest
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.state = 'harvesting'
            self.body.set_alarm(3)
        
          else:                           #flee order harvest resource
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.state = 'harvesting'
            self.body.set_alarm(3)
      
      elif message is 'collide':          #flee collide
        if details['what'] is 'Mantis':   #flee collide mantis
          toFleeTo = self.body.find_nearest('Nest')
          self.target = toFleeTo
          self.body.go_to(toFleeTo)
        if details['what'] is 'Nest':     #flee collide nest
          if details['who'] is self.target:
            self.body.amount = 1
            self.state = 'idle'


    elif self.state is 'traveling':       #travel state
      if message is 'order':              #travel order
        if details is 'i':                #travel order idle
          self.body.stop()
          self.state = 'idle'

        elif details is 'a':              #travel order attack
          toFight = self.body.find_nearest('Mantis')
          self.body.follow(toFight)
          self.body.set_alarm(1)
          self.target = toFight
          self.state = 'attacking'
        
        elif isinstance(details, tuple):  #travel order travel
          self.body.go_to(details)
          self.state = 'traveling'
        
        elif details is 'b':              #travel order build
          toBuild = self.body.find_nearest('Nest')
          self.body.go_to(toBuild)
          self.target = toBuild
          self.state = 'building'
        
        elif details is 'h':              #travel order harvest
          if self.resource:               #travel order harvest nest
            turnIn = self.body.find_nearest('Nest')
            self.target = turnIn
            self.body.go_to(turnIn)
            self.state = 'harvesting'
            self.body.set_alarm(3)
          
          else:                           #travel order harvest resource
            toHarv = self.body.find_nearest('Resource')
            self.target = toHarv
            self.body.go_to(toHarv)
            self.state = 'harvesting'
            self.body.set_alarm(3)
      
      if message is 'collide':            #travel collide
        if details['what'] is 'Mantis':   #travel collide mantis
          if self.body.amount <= .5:      #travel collide mantis flee
            toFleeTo = self.body.find_nearest('Nest')
            self.target = toFleeTo
            self.body.go_to(toFleeTo)

      
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
        

world_specification = {
  #'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
