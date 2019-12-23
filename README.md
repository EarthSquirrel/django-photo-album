# My Photo Album Using Django
Django-photo-album is going to be a web interface intended to run on a home network and store photos as well as information about them.

## Django Stuff
### Management Commands
#### populate\_attributes
This command creates attributes from a file called attributes.json. 
The base template is:

```
{
    "people": ["list", "of", "people"],
    "animals": ["list", "of", "animals"],
    "events": ["list", "of", "events"],
    "classifiers": ["list", "of", "classifiers"]
}
```

#### upload\_photos
This command uploads photos in the upload folder. The owner is the 
name of the folder. Edventually these will be created when a person
is created, but for not they must match exactly to the name of a 
person. The photos are moved to an uploaded folder once a photo
object is created.


## Website Layout
TODO: Put layout of urls and what each page does



